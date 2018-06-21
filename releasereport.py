#!/usr/bin/env python3

import sys
import requests

repos = [
    ("proycon", "clam"),
    ("proycon", "clamservices"),
    ("proycon", "pynlpl"),
    ("proycon", "folia"),
    ("proycon", "flat"),
    ("proycon", "foliadocserve"),
    ("proycon", "LaMachine"),
    ("proycon", "labirinto"),
    ("proycon", "python-ucto"),
    ("proycon", "python-frog"),
    ("proycon", "python-timbl"),
    ("proycon", "codemetapy"),
    ("LanguageMachines", "ticcutils"),
    ("LanguageMachines", "libfolia"),
    ("LanguageMachines", "ucto"),
    ("LanguageMachines", "frog"),
    ("LanguageMachines", "uctodata"),
    ("LanguageMachines", "frogdata"),
    ("LanguageMachines", "timbl"),
    ("LanguageMachines", "timblserver"),
    ("LanguageMachines", "mbt"),
    ("LanguageMachines", "mbtserver"),
    ("LanguageMachines", "foliautils"),
    ("LanguageMachines", "PICCL"),
    ("LanguageMachines", "ticcltools")
]



for user, repo in repos:
    r = requests.get(url=f"https://api.github.com/repos/{user}/{repo}/releases")
    data = r.json()
    print(data,file=sys.stderr)



