"""
Step 2 - Generation des n-grammes (2, 3 et 4)
Fenetre glissante sur chaque phrase, sans traverser les fins de phrase.
Seuls les n-grammes dont le premier token commence par une majuscule sont retenus.

Logique extraite de 2ngramme.py (bigrammes), 3ngramme.py (trigrammes)
et 4ngramme.py (quadrigrammes).
"""


def generate_ngrams(
    sentences_path: str,
    n2_path: str,
    n3_path: str,
    n4_path: str,
) -> None:
    with open(sentences_path, "r", encoding="utf-8") as f:
        lignes = f.readlines()

    # --- Bigrammes (logique de 2ngramme.py) ---
    with open(n2_path, "w", encoding="utf-8") as f:
        for ligne in lignes:
            mots = ligne.split()
            for i in range(len(mots) - 1):
                if mots[i] and mots[i][0].isupper():
                    f.write(mots[i] + " " + mots[i + 1] + "\n")

    # --- Trigrammes (logique de 3ngramme.py, sans dependance nltk) ---
    with open(n3_path, "w", encoding="utf-8") as f:
        for ligne in lignes:
            mots = ligne.split()
            for i in range(len(mots) - 2):
                if mots[i] and mots[i][0].isupper():
                    f.write(mots[i] + " " + mots[i + 1] + " " + mots[i + 2] + "\n")

    # --- Quadrigrammes (logique de 4ngramme.py) ---
    with open(n4_path, "w", encoding="utf-8") as f:
        for ligne in lignes:
            mots = ligne.split()
            for i in range(len(mots) - 3):
                if mots[i] and mots[i][0].isupper():
                    f.write(
                        mots[i] + " " + mots[i + 1] + " "
                        + mots[i + 2] + " " + mots[i + 3] + "\n"
                    )

    print(f"[step2] N-grammes -> {n2_path}, {n3_path}, {n4_path}")
