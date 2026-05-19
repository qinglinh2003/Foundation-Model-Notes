"""
Project 1: Checkpoint/Resume Verification
-----------------------------------------
Resume from a mid-run checkpoint and compare the resulting loss curve against
an uninterrupted reference run.

This is not part of the minimal training path. It is a diagnostic script for
checking whether checkpoint state is complete enough for reliable continuation.
"""

import json
from pathlib import Path

import torch

from config import ModelConfig, TrainConfig
from data import create_dataloaders, tokenize_corpus
from evaluate import plot_ablation
from model import MiniGPT
from tokenizer import load_tokenizer
from train import train


def _load_reference_log(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _closest_record(log: list[dict], step: int) -> dict:
    return min(log, key=lambda r: abs(int(r["step"]) - step))


def main() -> None:
    model_cfg = ModelConfig()
    train_cfg = TrainConfig()
    train_cfg.wandb_run_name = "cp8_resume_from_5000"
    train_cfg.checkpoint_dir = "checkpoints/cp8_resume"

    resume_path = Path("checkpoints/step_5000.pt")
    reference_log_path = Path("checkpoints/train_log.json")
    if not resume_path.exists():
        raise FileNotFoundError(f"Missing resume checkpoint: {resume_path}")
    if not reference_log_path.exists():
        raise FileNotFoundError(f"Missing reference log: {reference_log_path}")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    tok = load_tokenizer(train_cfg.tokenizer_path)
    eos_id = tok.token_to_id("<eos>")
    token_ids = tokenize_corpus(train_cfg.corpus_path, tok, eos_id=eos_id)
    train_loader, val_loader = create_dataloaders(
        token_ids,
        model_cfg.context_length,
        train_cfg.batch_size,
        train_cfg.val_fraction,
    )

    model = MiniGPT(model_cfg).to(device)
    resumed_log = train(
        model,
        train_loader,
        val_loader,
        train_cfg,
        device=device,
        resume_path=str(resume_path),
    )

    reference_log = _load_reference_log(str(reference_log_path))
    final_resume = resumed_log[-1]
    final_reference = reference_log[-1]
    mid_reference = _closest_record(reference_log, 5000)

    summary = {
        "resume_checkpoint": str(resume_path),
        "reference_log": str(reference_log_path),
        "mid_reference": mid_reference,
        "final_reference": final_reference,
        "final_resume": final_resume,
        "final_val_delta": final_resume["val_loss"] - final_reference["val_loss"],
        "note": (
            "This script restores model, optimizer, step, log, and RNG state. "
            "It does not restore the exact DataLoader iterator position, so "
            "bitwise-identical continuation is not expected."
        ),
    }

    out_dir = Path("results/cp8_resume")
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    plot_ablation(
        {"uninterrupted": reference_log, "resume_from_5000": resumed_log},
        metric="val_loss",
        save_path="figures/cp8_resume_val_loss.png",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
