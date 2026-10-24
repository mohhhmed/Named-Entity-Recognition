0. Préparation

Lire le corpus en UTF-8.
Réparer les mots coupés en fin de ligne (césures) et normaliser les espaces, les guillemets « » et les apostrophes ’.
Garder les majuscules et la ponctuation.

1. Découpage en phrases

Couper aux signes . ! ? … (attention aux guillemets de dialogue et aux abréviations comme M.).
Garder pour chaque token sa position (début de phrase ou milieu), car elle servira aux heuristiques.

2. Tokenisation

Séparer les mots et la ponctuation.
Gérer les cas français : l’Empire → l' + Empire, d’Anacréon → d' + Anacréon.
Garder les traits d’union dans les noms (Jean-Pierre).

3. Génération des n-grammes (1, 2, 3)

Fenêtre glissante sur chaque phrase, sans traverser les fins de phrase.
Compter les fréquences avec un dictionnaire : c’est ton modèle de langue.

4. Construction de L (Tâche 1)

Garder les n-grammes dont les tokens commencent par une majuscule.
Écrire candidat<TAB>fréquence en UTF-8, sans filtrage.

5. Construction de LP (Tâche 2)

Retirer les mots courants capitalisés (anti-liste, antidictionnaire).
Garder ceux qui sont capitalisés aussi en milieu de phrase.
Appliquer le seuil de fréquence.
Utiliser le contexte (titres avant, verbes de parole après) et les regexp de noms composés.
Fusionner les variantes (Hari Seldon / Seldon).

6. Construction de LL (Tâche 3)

Partir de L moins LP.
Repérer les prépositions de lieu devant le candidat (à, sur, vers, dans) et les mots-clés (planète, monde, système, université).
Classer en villes, organisations, universités, planètes et trancher les cas ambigus.


