"""Ablation 4: Learning rate sweep."""
import os, json, torch, time, math
from config import ModelConfig
from model import MiniGPT
from tokenizer import load_tokenizer
from data import tokenize_corpus, create_dataloaders
from train import get_lr
import wandb

tok = load_tokenizer("tokenizer/bpe_v2000.json")
eos_id = tok.token_to_id("<eos>")
token_ids = tokenize_corpus("data/corpus.txt", tok, eos_id)
text = open("data/corpus.txt").read()
total_bytes = len(text.encode("utf-8"))
bpt = total_bytes / len(token_ids)
device = "cuda"

lr_configs = [
    {"name": "lr_1e-5", "lr": 1e-5, "min_lr": 1e-6},
    {"name": "lr_1e-4", "lr": 1e-4, "min_lr": 1e-5},
    {"name": "lr_3e-4", "lr": 3e-4, "min_lr": 3e-5},
    {"name": "lr_1e-3", "lr": 1e-3, "min_lr": 1e-4},
    {"name": "lr_3e-3", "lr": 3e-3, "min_lr": 3e-4},
]

all_results = []
for cfg in lr_configs:
    name = cfg["name"]
    sep = "=" * 60
    print(f"\n{sep}")
    print(f"ABLATION 4: {name} (peak_lr={cfg['lr']})")
    print(sep)

    model_cfg = ModelConfig(
        vocab_size=2000, context_length=256,
        d_model=256, n_heads=4, n_layers=4, d_ff=1024,
        dropout=0.1, pos_encoding="learned"
    )
    model = MiniGPT(model_cfg).to(device)
    params = sum(p.numel() for p in model.parameters())

    train_loader, val_loader = create_dataloaders(token_ids, 256, 32, 0.05)
    optimizer = torch.optim.AdamW(model.parameters(), lr=cfg["lr"], weight_decay=0.01, betas=(0.9, 0.999))
    torch.manual_seed(42)

    run = wandb.init(project="capstone-project1-minigpt", name=f"abl4_{name}", reinit=True)

    log = []
    step = 0
    train_iter = iter(train_loader)
    model.train()
    t0 = time.time()
    nan_detected = False

    while step < 10000:
        try:
            batch = next(train_iter)
        except StopIteration:
            train_iter = iter(train_loader)
            batch = next(train_iter)
        x, y = batch[0].to(device), batch[1].to(device)
        lr = get_lr(step, 200, 10000, cfg["lr"], cfg["min_lr"])
        for pg in optimizer.param_groups:
            pg["lr"] = lr
        logits = model(x)
        loss = torch.nn.functional.cross_entropy(logits.view(-1, logits.size(-1)), y.view(-1))

        if torch.isnan(loss) or torch.isinf(loss):
            print(f"  NaN/Inf at step {step}! Stopping.")
            log.append({"step": step, "train_loss": float("nan"), "val_loss": float("nan"), "lr": lr, "grad_norm": 0.0})
            nan_detected = True
            break

        optimizer.zero_grad()
        loss.backward()
        grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        step += 1
        if step % 200 == 0:
            model.eval()
            vls = []
            with torch.no_grad():
                for i, vb in enumerate(val_loader):
                    if i >= 10: break
                    vx, vy = vb[0].to(device), vb[1].to(device)
                    vl = torch.nn.functional.cross_entropy(model(vx).view(-1, model_cfg.vocab_size), vy.view(-1))
                    vls.append(vl.item())
            val_loss = sum(vls) / len(vls)
            entry = {"step": step, "train_loss": loss.item(), "val_loss": val_loss, "lr": lr, "grad_norm": grad_norm.item()}
            log.append(entry)
            wandb.log(entry)
            if step % 2000 == 0:
                print(f"  step {step}: val={val_loss:.4f}, grad={grad_norm.item():.2f}")
            model.train()

    elapsed = time.time() - t0
    if log and not nan_detected:
        final_val = log[-1]["val_loss"]
        bits_per_byte = (final_val / math.log(2)) / bpt
    else:
        final_val = float("nan")
        bits_per_byte = float("nan")

    result = {"name": name, "lr": cfg["lr"], "params": params,
              "val_loss": final_val, "bits_per_byte": bits_per_byte,
              "nan": nan_detected, "wall_time": elapsed}
    all_results.append(result)
    print(f"  DONE: val={final_val:.4f}, bpb={bits_per_byte:.4f}, nan={nan_detected}")

    result_dir = f"results/abl4_lr/{name}"
    os.makedirs(result_dir, exist_ok=True)
    with open(os.path.join(result_dir, "train_log.json"), "w") as f:
        json.dump(log, f)

    wandb.finish()

os.makedirs("results/abl4_lr", exist_ok=True)
with open("results/abl4_lr/summary.json", "w") as f:
    json.dump(all_results, f, indent=2)

print("\n\nABLATION 4 SUMMARY")
for r in sorted(all_results, key=lambda x: x.get("val_loss", 999)):
    flag = " [NaN]" if r["nan"] else ""
    print(f"  lr={r['lr']:.0e}: val={r['val_loss']:.4f}, bpb={r['bits_per_byte']:.4f}{flag}")
