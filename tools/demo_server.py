#!/usr/bin/env python3
"""Serve the curriculum preview site plus the Project 1 MiniGPT demo."""

from __future__ import annotations

import dataclasses
import json
import sys
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

import torch


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
PROJECT = ROOT / "projects" / "project1"
CHECKPOINT = PROJECT / "checkpoints" / "step_10000.pt"
TOKENIZER = PROJECT / "tokenizer" / "bpe.json"

sys.path.insert(0, str(PROJECT))
from config import ModelConfig  # noqa: E402
from generate import generate  # noqa: E402
from model import MiniGPT  # noqa: E402
from tokenizer import load_tokenizer  # noqa: E402


MODEL = None
TOKENIZER_OBJ = None
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def load_demo_model() -> tuple[MiniGPT, object]:
    global MODEL, TOKENIZER_OBJ
    if MODEL is not None and TOKENIZER_OBJ is not None:
        return MODEL, TOKENIZER_OBJ
    if not CHECKPOINT.exists():
        raise FileNotFoundError(f"Missing checkpoint: {CHECKPOINT}")
    if not TOKENIZER.exists():
        raise FileNotFoundError(f"Missing tokenizer: {TOKENIZER}")

    checkpoint = torch.load(CHECKPOINT, map_location=DEVICE, weights_only=False)
    config_data = checkpoint.get("config", {})
    valid_fields = {field.name for field in dataclasses.fields(ModelConfig)}
    model_config = ModelConfig(**{key: value for key, value in config_data.items() if key in valid_fields})

    model = MiniGPT(model_config).to(DEVICE)
    model.load_state_dict(checkpoint["model"])
    model.eval()
    torch.set_num_threads(max(1, min(4, torch.get_num_threads())))

    MODEL = model
    TOKENIZER_OBJ = load_tokenizer(str(TOKENIZER))
    return MODEL, TOKENIZER_OBJ


class DemoHandler(SimpleHTTPRequestHandler):
    server_version = "CapstoneDemo/1.0"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIST), **kwargs)

    def log_message(self, fmt: str, *args) -> None:
        print(f"{self.address_string()} - {fmt % args}")

    def do_POST(self) -> None:
        request_path = unquote(self.path.split("?", 1)[0])
        if request_path.startswith("/capstone/"):
            request_path = request_path[len("/capstone") :]
        if request_path != "/api/generate":
            self.send_json({"error": "not found"}, status=404)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            prompt = str(payload.get("prompt", "")).strip()
            if not prompt:
                raise ValueError("Prompt cannot be empty.")
            max_tokens = clamp_int(payload.get("max_tokens", 120), 1, 240)
            top_k = clamp_int(payload.get("top_k", 40), 1, 100)
            temperature = clamp_float(payload.get("temperature", 0.8), 0.1, 1.5)

            model, tokenizer = load_demo_model()
            start = time.perf_counter()
            text = generate(
                model,
                tokenizer,
                prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                top_k=top_k,
                device=DEVICE,
            )
            elapsed = time.perf_counter() - start
            prompt_tokens = len(tokenizer.encode(prompt).ids)
            total_tokens = len(tokenizer.encode(text).ids)
            self.send_json(
                {
                    "text": text,
                    "elapsed_sec": elapsed,
                    "prompt_tokens": prompt_tokens,
                    "generated_tokens": max(0, total_tokens - prompt_tokens),
                    "device": DEVICE,
                }
            )
        except Exception as exc:  # Keep API errors visible in the demo UI.
            self.send_json({"error": str(exc)}, status=500)

    def send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def clamp_int(value: object, low: int, high: int) -> int:
    return max(low, min(high, int(value)))


def clamp_float(value: object, low: float, high: float) -> float:
    return max(low, min(high, float(value)))


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--preload", action="store_true", help="Load the model before accepting requests.")
    args = parser.parse_args()

    if args.preload:
        load_demo_model()
        print(f"Loaded MiniGPT on {DEVICE}: {CHECKPOINT}")

    server = ThreadingHTTPServer((args.host, args.port), DemoHandler)
    print(f"Serving preview + demo on http://{args.host}:{args.port}/")
    print(f"Demo page: http://{args.host}:{args.port}/demo.html")
    server.serve_forever()


if __name__ == "__main__":
    main()
