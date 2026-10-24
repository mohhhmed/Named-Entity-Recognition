"""
Pipeline NLP automatisé – Fondation Asimov
==========================================
Usage :
    python main.py <fichier_input.txt>

Sorties (dans automate/output/) :
    L.txt        – tous les n-grammes capitalisés + fréquence  (tâche 1)
    LP.txt       – personnages                                  (tâche 2)
    LL.txt       – lieux                                        (tâche 3)
    aliases.json – alias des personnages

Fichiers intermédiaires dans automate/work/ (supprimables).
"""

import argparse
import json
import os
import sys


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ensure(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Pipeline NLP : txt → L / LP / LL / aliases.json"
    )
    parser.add_argument("input_txt", help="Fichier texte d'entrée (UTF-8 ou latin)")
    args = parser.parse_args()

    input_path = os.path.abspath(args.input_txt)
    if not os.path.isfile(input_path):
        sys.exit(f"[ERREUR] Fichier introuvable : {input_path}")

    # Directories
    automate_dir = os.path.dirname(os.path.abspath(__file__))
    ams_dir      = os.path.dirname(automate_dir)          # AMS root (antidictio, verbs.json)
    work_dir     = _ensure(os.path.join(automate_dir, "work"))
    output_dir   = _ensure(os.path.join(automate_dir, "output"))

    # Intermediate file paths
    corpus_clean   = os.path.join(work_dir, "corpus_clean.txt")
    sentences_file = os.path.join(work_dir, "sentences.txt")
    n2_file        = os.path.join(work_dir, "n2_gramme_.txt")
    n3_file        = os.path.join(work_dir, "n3_gramme_.txt")
    n4_file        = os.path.join(work_dir, "n4_gramme_.txt")

    # Output file paths
    L_out       = os.path.join(output_dir, "L.txt")
    LP_out      = os.path.join(output_dir, "LP.txt")
    LL_out      = os.path.join(output_dir, "LL.txt")
    alias_out   = os.path.join(output_dir, "aliases.json")

    print("=" * 60)
    print("PIPELINE NLP - demarrage")
    print(f"  entree  : {input_path}")
    print(f"  travail : {work_dir}")
    print(f"  sorties : {output_dir}")
    print("=" * 60)

    # ------------------------------------------------------------------
    # ÉTAPE 0 – Préparation / nettoyage UTF-8
    # ------------------------------------------------------------------
    from step0_prepare import prepare
    prepare(input_path, corpus_clean)

    # ------------------------------------------------------------------
    # ÉTAPE 1 – Découpage en phrases
    # ------------------------------------------------------------------
    from step1_sentences import split_sentences
    split_sentences(corpus_clean, sentences_file)

    # ------------------------------------------------------------------
    # ÉTAPE 2 – Génération des n-grammes (2 et 3)
    # ------------------------------------------------------------------
    from step2_ngrams import generate_ngrams
    generate_ngrams(sentences_file, n2_file, n3_file, n4_file)

    # ------------------------------------------------------------------
    # ÉTAPE 3 – Construction de L
    # ------------------------------------------------------------------
    from step3_L import build_L
    build_L(corpus_clean, n2_file, n3_file, n4_file, L_out)

    # ------------------------------------------------------------------
    # ÉTAPES 4-6 – LP, LL, aliases  (modules org_old avec chemins adaptés)
    # ------------------------------------------------------------------

    # Configurer les chemins pour les modules org_old
    import config
    config.WORK_DIR     = work_dir
    config.RESOURCE_DIR = ams_dir
    config.CORPUS_FILE  = corpus_clean

    # FICHIERS lus par candidats.py — modification in-place de la liste
    # (from config import FICHIERS dans candidats.py pointe sur le même objet)
    config.FICHIERS[:] = [
        corpus_clean,
        n2_file,
        n3_file,
        n4_file,
    ]

    from ressources    import charger_interdits, charger_verbes
    from corpus        import indexer_corpus
    from candidats     import extraire_candidats
    from classification import classer_candidat
    from alias         import regrouper_alias
    from normalisation import norm

    print("[step4] Chargement des ressources...")
    interdits = charger_interdits()
    verbes    = charger_verbes()

    print("[step4] Indexation du corpus...")
    mots, debut, pos, propres = indexer_corpus()

    print("[step4] Extraction des candidats...")
    personnages, lieux = [], []

    # Seuil adaptatif : corpus court (< 5000 tokens) -> moins strict
    corpus_court = len(mots) < 5000

    for nom in extraire_candidats(interdits, propres):
        mil, pe, li, ar = classer_candidat(nom, mots, debut, pos, verbes)

        # Seuil min d'occurrences mid-phrase :
        #   >= 2 tokens : 1 occurrence suffit (bigramme = forte evidence)
        #   1 token     : 2 occurrences (1 si corpus court)
        seuil = 1 if len(nom) >= 2 else (1 if corpus_court else 2)

        # Seuil de rejet par article :
        #   nom simple   : rejet si > 35% des occurrences precedees d'article
        #   nom compose  : rejet si > 70% (ex: "les Mondes Exterieurs" est valide)
        art_seuil = 0.70 if len(nom) >= 2 else 0.35

        if mil < seuil or ar / max(mil, 1) >= art_seuil:
            continue
        if li >= 1 and li * 2 >= pe:
            lieux.append(nom)
        elif pe >= seuil and pe > li:
            personnages.append(nom)
        elif len(nom) == 1 and li == 0 and norm(nom[0]) in propres:
            personnages.append(nom)

    # ------------------------------------------------------------------
    # Filtrage des artefacts d'encodage
    # (entrees contenant des caracteres non-latins : ǟ, €, ™, etc.)
    # ------------------------------------------------------------------
    import unicodedata

    def est_latin(s):
        """Retourne True si tous les chars sont latins/ponctuation standard."""
        for c in s:
            if c in " '-":
                continue
            cat = unicodedata.category(c)
            # Accepter lettres (L*) et quelques poncts ; rejeter symboles (S*), autres
            if not cat.startswith("L"):
                return False
            name = unicodedata.name(c, "")
            # Rejeter les chars hors Latin extended (ex: U+01DF ǟ)
            if "LATIN" not in name and "DIGIT" not in name:
                return False
        return True

    personnages = [n for n in personnages if all(est_latin(t) for t in n)]
    lieux       = [n for n in lieux       if all(est_latin(t) for t in n)]

    print("[step5] Regroupement des alias...")
    noms, al, canon = regrouper_alias(personnages)

    # ------------------------------------------------------------------
    # Ecriture des sorties
    # ------------------------------------------------------------------
    j = " ".join

    open(LP_out,    "w", encoding="utf-8").write(
        "\n".join(sorted(j(n) for n in noms if canon[n] == n))
    )
    open(LL_out,    "w", encoding="utf-8").write(
        "\n".join(sorted(j(n) for n in lieux))
    )
    json.dump(al, open(alias_out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("=" * 60)
    print("RESULTATS")
    print(f"  L.txt        -> {L_out}")
    print(f"  LP.txt       -> {LP_out}  ({sum(1 for n in noms if canon[n]==n)} personnages)")
    print(f"  LL.txt       -> {LL_out}  ({len(lieux)} lieux)")
    print(f"  aliases.json -> {alias_out}  ({len(al)} alias)")
    print("=" * 60)


if __name__ == "__main__":
    main()
