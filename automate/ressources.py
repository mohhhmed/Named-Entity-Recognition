import json
import os
import config
from config import MOT
from normalisation import norm

AUX = set("est etait fut sera sont etaient a avait eut ont avaient etre avoir ete et ne y en".split())

def charger_interdits():
    path = os.path.join(config.RESOURCE_DIR, "antidictio.txt")
    return {norm(t) for l in open(path, encoding="utf-8") for t in MOT.findall(l)}

def _parcourir(x):
    if isinstance(x, str):
        w = MOT.findall(x.lower())
        if w: yield norm(w[-1])
    elif isinstance(x, dict):
        for k, v in x.items(): yield from _parcourir(k); yield from _parcourir(v)
    elif isinstance(x, list):
        for v in x: yield from _parcourir(v)

def charger_verbes():
    path = os.path.join(config.RESOURCE_DIR, "verbs.json")
    data = json.load(open(path, encoding="utf-8"))
    return {v for v in _parcourir(data) if len(v) > 2} - AUX
