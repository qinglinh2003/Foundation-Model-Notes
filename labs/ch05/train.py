"""
Lab 5 -- Reusable training loop
================================
A configurable training function that all three experiments call.
Supports different LR schedules, gradient clipping, checkpointing,
and metric logging.

This is the *given* training loop -- Lab 5 students diagnose how
different configurations change the outcome, not write the loop.
"""

import math
import time
import torch
import torch.nn.functional as F
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Callable


@dataclass
class TrainConfig:
    # Optimization
    lr: float = 3e-4
    weight_decay: float = 0.01
    betas: tuple = (0.9, 0.999)
    grad_clip: float = 1.0
    # Schedule: "cosine", "constant", "none"
    schedule: str = "cosine"
    warmup_steps: int = 100
    # Training budget
    max_steps: int = 2000
    eval_interval: int = 100
    log_interval: int = 50
    # Checkpoint
    checkpoint_dir: Optional[str] = None
    checkpoint_interval: int = 500
    resume_from: Optional[str] = None
    resume_mode: str = "full"  # "full", "model_only", "no_scheduler"
    # Misc
    seed: int = 42
    device: str = "cuda" if torch.cuda.is_available() else "cpu"


def _get_lr(step: int, cfg: TrainConfig) -> float:
    """Compute learning rate at a given step."""
    if cfg.schedule == "none":
        return cfg.lr
    # Warmup phase
    if step < cfg.warmup_steps:
        return cfg.lr * (step + 1) / cfg.warmup_steps
    # After warmup
    if cfg.schedule == "constant":
        return cfg.lr
    # Cosine decay
    progress = (step - cfg.warmup_steps) / max(1, cfg.max_steps - cfg.warmup_steps)
    progress = min(progress, 1.0)
    return cfg.lr * 0.5 * (1.0 + math.cos(math.pi * progress))


def train(
    model: torch.nn.Module,
    train_dl: torch.utils.data.DataLoader,
    val_dl: torch.utils.data.DataLoader,
    cfg: TrainConfig,
    decode_fn: Optional[Callable] = None,
    prompt_ids: Optional[torch.Tensor] = None,
) -> dict:
    """
    Train the model and return a log dict with loss curves and metadata.

    Returns
    -------
    dict with keys: train_losses, val_losses, steps, lr_history, samples,
                    wall_time, final_val_loss
    """
    device = cfg.device
    model = model.to(device)

    # Seed before model/optimizer state restoration.  A full checkpoint can
    # overwrite these RNG states after loading.
    torch.manual_seed(cfg.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(cfg.seed)

    # Optimizer
    optimizer = torch.optim.AdamW(
        model.parameters(), lr=cfg.lr,
        betas=cfg.betas, weight_decay=cfg.weight_decay,
    )

    # Manual LR schedule (we use a lambda so we can log it)
    start_step = 0
    scheduler_reset_step = 0

    # Resume
    if cfg.resume_from is not None:
        ckpt = torch.load(cfg.resume_from, map_location=device, weights_only=False)
        model.load_state_dict(ckpt["model"])
        if cfg.resume_mode in ("full", "no_scheduler"):
            optimizer.load_state_dict(ckpt["optimizer"])
        start_step = ckpt.get("step", 0)
        if cfg.resume_mode == "no_scheduler":
            scheduler_reset_step = start_step
        if cfg.resume_mode == "full":
            # Restore RNG state if available
            if "rng_state" in ckpt:
                torch.set_rng_state(ckpt["rng_state"].cpu().to(torch.uint8))
            if "cuda_rng_state" in ckpt and torch.cuda.is_available():
                torch.cuda.set_rng_state(ckpt["cuda_rng_state"].cpu().to(torch.uint8))
        print(f"  Resumed from step {start_step} (mode={cfg.resume_mode})")

    # Logging
    log = {
        "train_losses": [], "val_losses": [], "steps": [],
        "lr_history": [], "samples": [], "wall_time": 0,
    }

    # Training loop
    model.train()
    step = start_step
    t0 = time.time()
    train_iter = iter(train_dl)

    while step < cfg.max_steps:
        # Get batch (cycle through dataloader)
        try:
            x, y = next(train_iter)
        except StopIteration:
            train_iter = iter(train_dl)
            x, y = next(train_iter)

        x, y = x.to(device), y.to(device)

        # Set LR.  In the "no_scheduler" ablation, the model and optimizer
        # resume, but the LR schedule restarts as if this were local step 0.
        schedule_step = step - scheduler_reset_step
        lr = _get_lr(schedule_step, cfg)
        for pg in optimizer.param_groups:
            pg["lr"] = lr

        # Forward
        logits, _ = model(x)
        B, T, V = logits.shape
        loss = F.cross_entropy(
            logits[:, :-1, :].contiguous().view(-1, V),
            y[:, :-1].contiguous().view(-1),
        )

        # Backward
        optimizer.zero_grad()
        loss.backward()
        if cfg.grad_clip > 0:
            torch.nn.utils.clip_grad_norm_(model.parameters(), cfg.grad_clip)
        optimizer.step()

        # NaN detection
        if torch.isnan(loss) or torch.isinf(loss):
            print(f"  step {step:5d} | DIVERGED (loss={loss.item()})")
            log["train_losses"].append(float('nan'))
            log["steps"].append(step)
            log["lr_history"].append(lr)
            log["diverged"] = True
            break

        # Logging
        if step % cfg.log_interval == 0:
            log["train_losses"].append(loss.item())
            log["steps"].append(step)
            log["lr_history"].append(lr)

        # Eval
        if step % cfg.eval_interval == 0:
            val_loss = _evaluate(model, val_dl, device)
            log["val_losses"].append((step, val_loss))
            if step % (cfg.eval_interval * 4) == 0:
                print(f"  step {step:5d} | train {loss.item():.4f} | "
                      f"val {val_loss:.4f} | lr {lr:.2e}")

        # Checkpoint
        if cfg.checkpoint_dir and step > 0 and step % cfg.checkpoint_interval == 0:
            _save_checkpoint(model, optimizer, step, cfg)

        step += 1

    # Final eval
    final_val = _evaluate(model, val_dl, device)
    log["val_losses"].append((step, final_val))
    log["final_val_loss"] = final_val
    log["wall_time"] = time.time() - t0

    # Final sample
    if decode_fn and prompt_ids is not None:
        model.eval()
        gen = model.generate(prompt_ids.to(device), max_new_tokens=200, temperature=0.8)
        log["samples"].append(decode_fn(gen[0].cpu().tolist()))

    # Final checkpoint
    if cfg.checkpoint_dir:
        _save_checkpoint(model, optimizer, step, cfg)

    return log


@torch.no_grad()
def _evaluate(model, val_dl, device, max_batches=20):
    model.eval()
    total_loss, count = 0.0, 0
    for i, (x, y) in enumerate(val_dl):
        if i >= max_batches:
            break
        x, y = x.to(device), y.to(device)
        logits, _ = model(x)
        B, T, V = logits.shape
        loss = F.cross_entropy(
            logits[:, :-1, :].contiguous().view(-1, V),
            y[:, :-1].contiguous().view(-1),
        )
        total_loss += loss.item()
        count += 1
    model.train()
    return total_loss / max(count, 1)


def _save_checkpoint(model, optimizer, step, cfg):
    ckpt_dir = Path(cfg.checkpoint_dir)
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    ckpt = {
        "model": model.state_dict(),
        "optimizer": optimizer.state_dict(),
        "step": step,
        "config": cfg,
        "rng_state": torch.get_rng_state(),
    }
    if torch.cuda.is_available():
        ckpt["cuda_rng_state"] = torch.cuda.get_rng_state()
    path = ckpt_dir / f"ckpt_step{step}.pt"
    torch.save(ckpt, path)
