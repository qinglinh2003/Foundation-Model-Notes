"""
Project 1: Training Loop
--------------------------
Implements the full training loop: forward, loss, backward, optimize, log, checkpoint.

Requirements:
    - AdamW optimizer with decoupled weight decay
    - Learning rate schedule: linear warmup + cosine decay
    - Gradient clipping (max norm)
    - Periodic validation evaluation
    - Periodic checkpoint saving (full state)
    - Logging: train loss, val loss, learning rate, gradient norm per eval step
"""

import math
import time
import json
import random
from dataclasses import asdict, is_dataclass
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F


def get_lr(step: int, warmup_steps: int, max_steps: int, max_lr: float, min_lr: float) -> float:
    """
    Compute learning rate for a given step using warmup + cosine decay.

    Args:
        step:         Current training step (0-indexed).
        warmup_steps: Number of linear warmup steps.
        max_steps:    Total training steps.
        max_lr:       Peak learning rate (reached at end of warmup).
        min_lr:       Minimum learning rate (at end of cosine decay).

    Returns:
        The learning rate for this step.

    Schedule:
        - Steps [0, warmup_steps): linear from 0 to max_lr
        - Steps [warmup_steps, max_steps]: cosine from max_lr to min_lr
    """
    if max_steps <= 0:
        raise ValueError("max_steps must be positive")
    if warmup_steps > 0 and step < warmup_steps:
        return max_lr * (step + 1) / warmup_steps
    if step >= max_steps:
        return min_lr

    decay_steps = max(1, max_steps - warmup_steps)
    progress = min(1.0, max(0.0, (step - warmup_steps) / decay_steps))
    coeff = 0.5 * (1.0 + math.cos(math.pi * progress))
    return min_lr + coeff * (max_lr - min_lr)


def _config_to_dict(config) -> dict:
    if is_dataclass(config):
        return asdict(config)
    if isinstance(config, dict):
        return dict(config)
    return dict(vars(config))


def _rng_state() -> dict:
    state = {
        "python": random.getstate(),
        "torch": torch.get_rng_state(),
    }
    if torch.cuda.is_available():
        state["cuda"] = torch.cuda.get_rng_state_all()
    return state


def _restore_rng_state(state: dict) -> None:
    if not state:
        return
    if "python" in state:
        random.setstate(state["python"])
    if "torch" in state:
        torch.set_rng_state(state["torch"])
    if "cuda" in state and torch.cuda.is_available():
        torch.cuda.set_rng_state_all(state["cuda"])


def save_checkpoint(
    path: str,
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    step: int,
    config: dict,
    train_log: list,
) -> None:
    """
    Save a complete training checkpoint.

    Must include:
        - model state_dict
        - optimizer state_dict
        - current step
        - config
        - training log so far
        - (optional) RNG states for exact reproducibility
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "model": model.state_dict(),
        "optimizer": optimizer.state_dict(),
        "step": step,
        "config": config,
        "train_log": train_log,
        "rng_state": _rng_state(),
    }
    torch.save(payload, path)


def load_checkpoint(
    path: str,
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
) -> tuple[int, list]:
    """
    Load a checkpoint and restore training state.

    Returns:
        (step, train_log) — the step to resume from and the log so far.
    """
    ckpt = torch.load(path, map_location="cpu", weights_only=False)
    model.load_state_dict(ckpt["model"])
    optimizer.load_state_dict(ckpt["optimizer"])
    _restore_rng_state(ckpt.get("rng_state", {}))
    return int(ckpt.get("step", 0)), list(ckpt.get("train_log", []))


@torch.no_grad()
def evaluate(model: nn.Module, val_loader, device: str) -> float:
    """
    Compute average cross-entropy loss on the validation set.

    Args:
        model:      The model in eval mode.
        val_loader: Validation DataLoader.
        device:     "cuda" or "cpu".

    Returns:
        Average validation loss (float).
    """
    model.eval()
    losses: list[float] = []
    for inputs, targets in val_loader:
        inputs = inputs.to(device, non_blocking=True)
        targets = targets.to(device, non_blocking=True)
        logits = model(inputs)
        loss = F.cross_entropy(logits.view(-1, logits.size(-1)), targets.reshape(-1))
        losses.append(float(loss.item()))
    model.train()
    return sum(losses) / max(1, len(losses))


def _cycle(loader):
    while True:
        for batch in loader:
            yield batch


def _maybe_init_wandb(config, model: nn.Module):
    if not getattr(config, "use_wandb", False):
        return None
    try:
        import wandb
    except ImportError:
        print("wandb not installed; continuing without wandb logging.")
        return None

    run = wandb.init(
        project=getattr(config, "wandb_project", "capstone-project1-minigpt"),
        name=getattr(config, "wandb_run_name", None),
        config=_config_to_dict(config),
        reinit=True,
    )
    wandb.watch(model, log=None)
    return wandb


def train(
    model: nn.Module,
    train_loader,
    val_loader,
    config,
    device: str = "cuda",
    resume_path: str = None,
) -> list:
    """
    Full training loop.

    Pseudocode (from Chapter 5):
        for step in range(max_steps):
            batch = next(train_iterator)
            logits = model(batch.input)
            loss = cross_entropy(logits, batch.target)
            loss.backward()
            clip_grad_norm_(model.parameters(), max_norm)
            optimizer.step()
            scheduler.step()   # or manual LR set
            optimizer.zero_grad()

    Must also:
        - Log train loss, val loss, LR, grad norm at eval_interval
        - Save checkpoint at save_interval
        - Print progress

    Args:
        model:       The MiniGPT model.
        train_loader: Training DataLoader.
        val_loader:   Validation DataLoader.
        config:       TrainConfig instance.
        device:       "cuda" or "cpu".
        resume_path:  Path to checkpoint to resume from (or None).

    Returns:
        train_log: List of dicts with logged metrics.
    """
    torch.manual_seed(config.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(config.seed)

    model.to(device)
    model.train()

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=config.lr,
        betas=config.betas,
        weight_decay=config.weight_decay,
    )

    start_step = 0
    train_log: list[dict] = []
    if resume_path is not None:
        start_step, train_log = load_checkpoint(resume_path, model, optimizer)
        print(f"Resumed from {resume_path} at step {start_step}")

    wandb = _maybe_init_wandb(config, model)
    train_iter = _cycle(train_loader)
    checkpoint_dir = Path(config.checkpoint_dir)
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    last_time = time.time()
    for step in range(start_step, config.max_steps):
        lr = get_lr(step, config.warmup_steps, config.max_steps, config.lr, config.min_lr)
        for group in optimizer.param_groups:
            group["lr"] = lr

        inputs, targets = next(train_iter)
        inputs = inputs.to(device, non_blocking=True)
        targets = targets.to(device, non_blocking=True)

        logits = model(inputs)
        loss = F.cross_entropy(logits.view(-1, logits.size(-1)), targets.reshape(-1))
        if not torch.isfinite(loss):
            raise FloatingPointError(f"Non-finite loss at step {step}: {loss.item()}")

        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), config.grad_clip)
        optimizer.step()

        should_eval = (step == 0) or ((step + 1) % config.eval_interval == 0) or (step + 1 == config.max_steps)
        if should_eval:
            val_loss = evaluate(model, val_loader, device)
            now = time.time()
            elapsed = now - last_time
            last_time = now
            record = {
                "step": step + 1,
                "train_loss": float(loss.item()),
                "val_loss": float(val_loss),
                "lr": float(lr),
                "grad_norm": float(grad_norm),
                "seconds_since_last_log": float(elapsed),
            }
            train_log.append(record)
            print(
                f"step {step + 1:6d}/{config.max_steps} "
                f"train {record['train_loss']:.4f} "
                f"val {record['val_loss']:.4f} "
                f"lr {lr:.2e} "
                f"grad {record['grad_norm']:.2f}"
            )
            if wandb is not None:
                wandb.log(record, step=step + 1)

        should_save = ((step + 1) % config.save_interval == 0) or (step + 1 == config.max_steps)
        if should_save:
            ckpt_path = checkpoint_dir / f"step_{step + 1}.pt"
            save_checkpoint(
                ckpt_path,
                model,
                optimizer,
                step + 1,
                _config_to_dict(config),
                train_log,
            )

    log_path = checkpoint_dir / "train_log.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(train_log, f, indent=2)
    if wandb is not None:
        wandb.finish()
    return train_log


# ---------------------------------------------------------------------------
# Quick test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Test LR schedule
    warmup, total, max_lr, min_lr = 100, 1000, 3e-4, 3e-5
    lrs = [get_lr(s, warmup, total, max_lr, min_lr) for s in range(total)]
    print(f"LR at step 0:    {lrs[0]:.6f} (should be ~0)")
    print(f"LR at step 100:  {lrs[100]:.6f} (should be ~{max_lr})")
    print(f"LR at step 999:  {lrs[999]:.6f} (should be ~{min_lr})")
    print("LR schedule OK.")
