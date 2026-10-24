import re
import os

MOT    = re.compile(r"[^\W\d_]+(?:-[^\W\d_]+)*")
FIN    = re.compile(r'[.!?…:«—–"\""]')
ROMAIN = re.compile(r"^[IVXLCDM]+$")

# -----------------------------------------------------------------------
# TITRES — ajouts :
#   "r"           : prefixe robot (R. Daneel, R. Sammy, R. Giskard)
#   "robot"       : "Robot Daneel Olivaw" -> strip "Robot" -> (Daneel, Olivaw)
#   "commissaire" : evite "Principal" seul comme candidat personne
#   "inspecteur", "detective", "agent", "sergent", "officier" : titres policiers
# -----------------------------------------------------------------------
TITRES = set(
    "m mme mlle dr docteur professeur maire sire empereur seigneur "
    "monsieur madame mademoiselle commandant capitaine colonel general "
    "roi reine prince princesse lord lady sir commodore marchand "
    "ambassadeur conseiller consul pere maitre maitres "
    "r robot "
    "commissaire inspecteur detective agent sergent officier prefet "
    "ministre president gouverneur directeur chef adjoint sous-chef "
    "principal"   # rang policier : "Commissaire Principal" -> strip les deux
    .split()
)

ARTICLES = set("le la l les un une du des au aux ce cette ces".split())

# -----------------------------------------------------------------------
# PREP — prepositions fiablement indicatrices de lieu
# "a" (à) RETIRE : trop ambigu ("dit a Baley" ≠ lieu)
# "par" AJOUTE : "passer par Spacetown", "envoyé par Trantor" -> lieu fiable
# -----------------------------------------------------------------------
PREP = set("sur vers dans depuis en au aux par".split())

# -----------------------------------------------------------------------
# NLIEU — mots de type lieu (formes normalisees sans accents)
# Ajouts : pluraux (rues, mondes...), institutions, lieux SF et urbains
# -----------------------------------------------------------------------
NLIEU = set(
    # Geographie naturelle
    "planete planetes monde mondes systeme systemes etoile etoiles "
    "galaxie continent ocean mer lac fleuve riviere ile iles montagne "
    "foret desert vallee plaine region regions territoire territoires "
    # Geographie politique/administrative
    "royaume royaumes ville villes capitale capitales province provinces "
    "secteur secteurs quartier quartiers district districts departement "
    "departements arrondissement commune communes prefecture prefecture "
    "municipalite colonie colonies empire empires republique "
    # Lieux urbains
    "cite banlieue couloir galerie tunnel rue rues avenue boulevard "
    "immeuble batiment hotel gare aeroport port station "
    # Institutions / etablissements
    "commissariat bureau bureaux laboratoire universite ecole hopital "
    "eglise palais chateau tribunal mairie ministere parlement senat "
    "assemblee police prefecture usine ferme complexe base camp siege "
    # Asimov SF specifique
    "dome etablissement monde-caverne caveaux cavernes spatioport "
    "vaisseau navire planete-mere monde-robot enclave zone"
    .split()
)

# Set dynamically by main.py before the pipeline runs
WORK_DIR     = ""
RESOURCE_DIR = ""
CORPUS_FILE  = ""
FICHIERS     = []
