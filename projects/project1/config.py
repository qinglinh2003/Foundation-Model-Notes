"""
Project 1: MiniGPT Configuration
---------------------------------
Default hyperparameters. Adjust as needed for your corpus and compute budget.
"""

from dataclasses import dataclass


@dataclass
class ModelConfig:
    vocab_size: int = 2000
    context_length: int = 256
    d_model: int = 256
    n_heads: int = 4
    n_layers: int = 4
    d_ff: int = 1024          # typically 4 * d_model
    dropout: float = 0.1
    pos_encoding: str = "learned"  # "learned" or "rope"


@dataclass
class TrainConfig:
    # Data
    corpus_path: str = "data/corpus.txt"
    tokenizer_path: str = "tokenizer/bpe.json"
    val_fraction: float = 0.05

    # Training
    batch_size: int = 32
    max_steps: int = 10_000
    eval_interval: int = 200
    eval_steps: int = 20

    # Optimizer
    lr: float = 3e-4
    weight_decay: float = 0.01
    betas: tuple = (0.9, 0.999)
    grad_clip: float = 1.0

    # Schedule
    warmup_steps: int = 200
    min_lr: float = 3e-5       # cosine decays to this

    # Checkpoint
    checkpoint_dir: str = "checkpoints"
    save_interval: int = 1000

    # Logging
    use_wandb: bool = True
    wandb_project: str = "capstone-project1-minigpt"
    wandb_run_name: str = "smoke"

    # Generation
    gen_interval: int = 1000
    gen_prompt: str = "The "
    gen_max_tokens: int = 100

    # Reproducibility
    seed: int = 42
