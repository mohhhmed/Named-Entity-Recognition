"""
kaggle.py
=========
Batch runner for the NLP pipeline over the Kaggle session-4 dataset.

FIX: files are UTF-8, not cp1252. Auto-detect encoding before passing to pipeline.
"""

import os
import shutil
import subprocess
import sys
import tempfile

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

AMS_DIR       = os.path.dirname(os.path.abspath(__file__))
KAGGLE_DIR    = os.path.join(
    AMS_DIR,
    "reseaux-de-personnages-de-fondation-session-4",
)
AUTOMATE_DIR  = os.path.join(AMS_DIR, "automate")
AUTO_OUTPUT   = os.path.join(AUTOMATE_DIR, "output")
RESULTS_DIR   = os.path.join(AMS_DIR, "results")

OUTPUT_FILES  = ["L.txt", "LP.txt", "LL.txt", "aliases.json"]


# ---------------------------------------------------------------------------
# Encoding detection
# ---------------------------------------------------------------------------

def to_utf8_tempfile(src_path: str) -> str:
    """
    Read src_path with automatic encoding detection and write a clean UTF-8
    temporary .txt file. Returns the path of the temp file (caller must delete).
    """
    text = None

    # Try encodings in order: UTF-8 variants first, then cp1252/latin-1 fallback
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            with open(src_path, "r", encoding=enc) as f:
                text = f.read()
            break
        except (UnicodeDecodeError, LookupError):
            continue

    if text is None:
        # latin-1 never raises — if we got here something is very wrong
        with open(src_path, "rb") as f:
            text = f.read().decode("latin-1", errors="replace")

    tmp = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        suffix=".txt",
        delete=False,
    )
    tmp.write(text)
    tmp.close()
    return tmp.name


# ---------------------------------------------------------------------------
# Pipeline runner
# ---------------------------------------------------------------------------

def run_pipeline(input_path: str, dest_folder: str) -> bool:
    os.makedirs(dest_folder, exist_ok=True)

    result = subprocess.run(
        ["py", "main.py", input_path],
        cwd=AUTOMATE_DIR,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("FAILED")
        print(f"    stderr: {result.stderr.strip()[:300]}")
        return False

    for fname in OUTPUT_FILES:
        src = os.path.join(AUTO_OUTPUT, fname)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(dest_folder, fname))
        else:
            print(f"    [WARN] {fname} not found in automate/output/")

    print("OK")
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if not os.path.isdir(KAGGLE_DIR):
        sys.exit(f"[ERREUR] Dataset introuvable : {KAGGLE_DIR}")

    os.makedirs(RESULTS_DIR, exist_ok=True)

    romans = sorted(
        d for d in os.listdir(KAGGLE_DIR)
        if os.path.isdir(os.path.join(KAGGLE_DIR, d))
    )

    total_ok = total_fail = 0

    for roman in romans:
        roman_path   = os.path.join(KAGGLE_DIR, roman)
        roman_result = os.path.join(RESULTS_DIR, roman)
        os.makedirs(roman_result, exist_ok=True)

        chapters = sorted(
            f for f in os.listdir(roman_path)
            if os.path.isfile(os.path.join(roman_path, f))
        )

        print(f"\n{'='*60}")
        print(f"  Roman : {roman}  ({len(chapters)} chapitres)")
        print(f"{'='*60}")

        for chapter in chapters:
            chapter_src  = os.path.join(roman_path, chapter)
            chapter_dest = os.path.join(roman_result, chapter)

            print(f"  [{chapter}] ", end="", flush=True)

            tmp_path = to_utf8_tempfile(chapter_src)

            try:
                ok = run_pipeline(tmp_path, chapter_dest)
            finally:
                os.remove(tmp_path)

            if ok:
                total_ok += 1
            else:
                total_fail += 1

    print(f"\n{'='*60}")
    print(f"  Termine : {total_ok} OK,  {total_fail} echec(s)")
    print(f"  Resultats : {RESULTS_DIR}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
