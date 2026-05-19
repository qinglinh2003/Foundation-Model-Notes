"""
One-time data preparation for Lab 2.

Reads the raw UniMorph English file and produces a filtered, deduplicated,
class-balanced TSV ready for training. The output file is committed to the
repository so students do not need to re-run this script; it is included
for reproducibility.

Source: https://github.com/unimorph/eng (CC BY-SA 3.0)

Balancing strategy: keep ALL irregular pairs in every class (they are
pedagogically essential and rare), then random-sample regulars to bring
each class to a target count. Random balancing alone would drop classic
irregulars like mouse->mice from PLURAL, where the regular vocabulary
dominates 1000:1.
"""

import random
from pathlib import Path

RAW = Path(__file__).parent / "unimorph_eng_raw.tsv"
OUT = Path(__file__).parent / "unimorph_eng_filtered.tsv"

TAG_MAP = {
    "V;PST":        "PAST",
    "V;V.PTCP;PRS": "GERUND",
    "V;PRS;3;SG":   "3SG",
    "N;PL":         "PLURAL",
}

MAX_LEMMA_LEN = 10
MAX_INFLECTED_LEN = 12
MIN_LEN = 2

# UniMorph occasionally encodes morphological features (e.g. "countable",
# "uncountable") in the inflected-form column for nouns that resist
# pluralization. These are not actual word forms and must be dropped.
FEATURE_JUNK = {
    "countable", "uncountable", "mass", "defective",
    "invariable", "none", "no", "n/a", "na",
}

# Classic English irregulars missing from UniMorph English. These are the
# textbook examples linguists use to motivate why memorization (not just
# rules) is part of morphology, so we patch them in.
SUPPLEMENTARY = [
    # PLURAL irregulars
    ("child",  "children", "PLURAL"),
    ("foot",   "feet",     "PLURAL"),
    ("tooth",  "teeth",    "PLURAL"),
    ("goose",  "geese",    "PLURAL"),
    ("woman",  "women",    "PLURAL"),
    ("person", "people",   "PLURAL"),
    ("ox",     "oxen",     "PLURAL"),
    ("die",    "dice",     "PLURAL"),
    # Zero-plural nouns
    ("sheep",  "sheep",    "PLURAL"),
    ("deer",   "deer",     "PLURAL"),
    ("fish",   "fish",     "PLURAL"),
    ("series", "series",   "PLURAL"),
    # Common 3SG irregulars
    ("be",     "is",       "3SG"),
    ("have",   "has",      "3SG"),
    ("do",     "does",     "3SG"),
]

# Per-class target count after balancing. The min across raw verb classes
# is ~19k (GERUND); we cap PLURAL to roughly the same after preserving
# irregulars.
TARGET_PER_CLASS = 19000


def is_clean_ascii_alpha(s: str) -> bool:
    return s.isascii() and s.isalpha() and len(s) >= MIN_LEN


def is_regular(lemma: str, inflected: str, tag: str) -> bool:
    """
    Lightweight regular/irregular classifier used only for stratified
    sampling. The full version with three-way categorization
    (pure_regular / phonological / irregular) lives in utils.classify_form.
    """
    L, I = lemma, inflected

    if tag == "PAST":
        # add -ed | drop e + -ed | y->ied | doubled consonant + -ed
        if I == L + "ed": return True
        if L.endswith("e") and I == L + "d": return True
        if L.endswith("y") and len(L) >= 2 and L[-2] not in "aeiou" and I == L[:-1] + "ied": return True
        if len(L) >= 2 and L[-1] == L[-2] == L[-1] and I == L + L[-1] + "ed": return True
        # double consonant rule: hop -> hopped
        if len(L) >= 3 and L[-1] not in "aeiouy" and L[-2] in "aeiou" and L[-3] not in "aeiouy" \
                and I == L + L[-1] + "ed":
            return True
        return False

    if tag == "GERUND":
        # add -ing | drop e + -ing | doubled consonant + -ing
        if I == L + "ing": return True
        if L.endswith("e") and not L.endswith("ee") and I == L[:-1] + "ing": return True
        if len(L) >= 3 and L[-1] not in "aeiouy" and L[-2] in "aeiou" and L[-3] not in "aeiouy" \
                and I == L + L[-1] + "ing":
            return True
        return False

    if tag == "3SG":
        # add -s | add -es | y->ies
        if I == L + "s": return True
        if I == L + "es": return True
        if L.endswith("y") and len(L) >= 2 and L[-2] not in "aeiou" and I == L[:-1] + "ies":
            return True
        return False

    if tag == "PLURAL":
        if I == L + "s": return True
        if I == L + "es": return True
        if L.endswith("y") and len(L) >= 2 and L[-2] not in "aeiou" and I == L[:-1] + "ies":
            return True
        if L.endswith("f") and I == L[:-1] + "ves": return True
        if L.endswith("fe") and I == L[:-2] + "ves": return True
        return False

    return False  # unknown tag treated as irregular (won't happen here)


def main():
    if not RAW.exists():
        raise SystemExit(
            f"Raw file not found at {RAW}. Download it first:\n"
            "  curl -sL https://raw.githubusercontent.com/unimorph/eng/master/eng \\\n"
            f"      -o {RAW}"
        )

    seen: set[tuple[str, str]] = set()
    by_tag: dict[str, list[tuple[str, str, str]]] = {}

    with open(RAW) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) != 3:
                continue
            lemma, inflected, raw_tag = parts
            if raw_tag not in TAG_MAP:
                continue
            lemma = lemma.lower().strip()
            inflected = inflected.lower().strip()
            if not (is_clean_ascii_alpha(lemma) and is_clean_ascii_alpha(inflected)):
                continue
            if inflected in FEATURE_JUNK:
                continue
            if len(lemma) > MAX_LEMMA_LEN or len(inflected) > MAX_INFLECTED_LEN:
                continue
            tag = TAG_MAP[raw_tag]
            key = (lemma, tag)
            if key in seen:
                continue
            seen.add(key)
            by_tag.setdefault(tag, []).append((lemma, inflected, tag))

    # Merge supplementary classic irregulars (UniMorph English is thin on
    # English-native nominal irregulars and a few high-frequency suppletive
    # verb forms).
    for lemma, inflected, tag in SUPPLEMENTARY:
        key = (lemma, tag)
        if key in seen:
            continue
        seen.add(key)
        by_tag.setdefault(tag, []).append((lemma, inflected, tag))

    print("Raw filtered counts (after supplementary patches):")
    for tag, recs in by_tag.items():
        print(f"  {tag}: {len(recs)}")

    rng = random.Random(42)
    balanced: list[tuple[str, str, str]] = []

    print(f"\nBalancing each class around {TARGET_PER_CLASS} samples (irregulars kept verbatim):")
    for tag, recs in by_tag.items():
        regs = [r for r in recs if is_regular(*r)]
        irrs = [r for r in recs if not is_regular(*r)]
        rng.shuffle(regs)
        keep_regs = regs[: max(0, TARGET_PER_CLASS - len(irrs))]
        kept = irrs + keep_regs
        print(f"  {tag}: {len(irrs)} irregular + {len(keep_regs)} regular = {len(kept)}")
        balanced.extend(kept)

    rng.shuffle(balanced)
    with open(OUT, "w") as f:
        for lemma, inflected, tag in balanced:
            f.write(f"{lemma}\t{inflected}\t{tag}\n")

    print(f"\nWrote {len(balanced)} records to {OUT}")


if __name__ == "__main__":
    main()
