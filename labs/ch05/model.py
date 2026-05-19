"""
Lab 5 -- Model
===============
Re-exports the MiniGPT from Lab 3.  Lab 5 is about training pipeline
diagnostics, not architecture -- we use a known-good model and vary
the pipeline around it.
"""

import importlib.util
from pathlib import Path

# Load Lab 3's model module by file path.  This file is also named
# ``model.py``, so a normal ``from model import ...`` would import this
# wrapper again and create a circular import.
_lab3_model_path = Path(__file__).resolve().parent.parent / "ch03" / "model.py"
_spec = importlib.util.spec_from_file_location("lab3_model", _lab3_model_path)
_lab3_model = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_lab3_model)

GPT = _lab3_model.GPT
GPTConfig = _lab3_model.GPTConfig
shifted_ce_loss = _lab3_model.shifted_ce_loss
