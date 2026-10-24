# Pipeline d'Extraction d'Entites Nommees (Corpus Fondation - Isaac Asimov)

Ce projet fournit une chaine de traitement automatique du langage naturel (TALN / NLP) dediee a l'identification, la classification et la resolution d'entites nommees (personnages, lieux et variantes d'alias) au sein de textes litteraires.

---

## 1. Description du Pipeline

A partir d'un fichier texte brut (`.txt`), le pipeline execute successivement les etapes suivantes :

1. **Pretraitement et segmentation** :
   - Normalisation de l'encodage (UTF-8) et des caracteres specifiques.
   - Decoupage en unites phrastiques.
   - Generation des n-grammes (2, 3 et 4-grammes).

2. **Extraction et classification** :
   - `L.txt` : ensemble des n-grammes capitalises avec leur frequence d'apparition.
   - `LP.txt` : liste des entites filtrees et classees comme personnages (Liste Personnages).
   - `LL.txt` : liste des entites filtrees et classees comme lieux (Liste Lieux).

3. **Resolution des alias** :
   - `aliases.json` : dictionnaire associant chaque forme canonique de personnage a ses variantes detectees dans le texte.

---

## 2. Instructions d'Execution

### Execution unitaire (sur un fichier texte unique)

Pour executer le pipeline sur un unique fichier texte :

```bash
cd automate
py main.py "chemin/vers/fichier.txt"
```

Les fichiers de sortie sont generes dans le repertoire `automate/output/` :
- `automate/output/L.txt`
- `automate/output/LP.txt`
- `automate/output/LL.txt`
- `automate/output/aliases.json`

---

### Execution par lot (sur l'ensemble du corpus)

Pour lancer le traitement automatise sur l'ensemble des chapitres du dossier `reseaux-de-personnages-de-fondation-session-4` :

```bash
py get_result.py
```

**Fonctionnement du script `get_result.py` :**
- Parcourt les sous-dossiers de chaque roman et identifie l'ensemble des fichiers chapitres.
- Appelle le module `automate` de maniere isolee pour chaque fichier.
- Archive l'integralite des sorties dans l'arborescence cible `results/` :

```text
results/
├── <nom_du_roman>/
│   ├── <nom_du_chapitre>/
│   │   ├── L.txt
│   │   ├── LP.txt
│   │   ├── LL.txt
│   │   └── aliases.json
```
