#!/usr/bin/env python3

import sys
import requests
import datetime
import os
from requests.auth import HTTPBasicAuth


try:
    begindate = sys.argv[1]
except:
    print("Enter a begin date (YYYY-MM-DD!)",file=sys.stderr)
    sys.exit(2)
try:
    enddate = sys.argv[2]
except:
    enddate = datetime.datetime.now().strftime("%Y-%m-%d")

username = os.environ['GITHUB_USER']
pw = os.environ['GITHUB_PASS']

sources = [
    ("CLAM","CLARIAH T21 [D2.8 (software); D2.9 (doc)]", [
        ("proycon", "clam"),
        ("proycon", "clamservices"),
    ]),
    ("FoLiA","CLARIAH T71 [D2.5 (libs); D2.6 (docs); D2.7 (tools)]", [
        ("proycon", "folia"),
        ("proycon", "pynlpl"),
        ("LanguageMachines", "libfolia"),
        ("LanguageMachines", "foliautils"),
    ]),
    ("FLAT","CLARIAH T24 [D2.10 (software); D2.11 (docs)]", [
        ("proycon", "flat"),
        ("proycon", "foliadocserve"),
    ]),
    ("LaMachine","CLARIAH: LaMachine v2 plan in scope of CLARIAH WP3 VRE", [
        ("proycon", "LaMachine"),
        ("proycon", "labirinto"),
        ("proycon", "codemetapy"),
    ]),
    ("Ucto","CLARIAH T55 [D1.1 (software), D1.2 (docs)]", [
        ("LanguageMachines", "ucto"),
        ("LanguageMachines", "uctodata"),
        ("proycon", "python-ucto"),
    ]),
    ("Frog","CLARIAH T22 [D2.1 (software); D2.2 (doc)]; T23 [D2.3 (froggen software), D2.4 (froggen docs)]", [
        ("LanguageMachines", "frog"),
        ("LanguageMachines", "frogdata"),
        ("proycon", "python-frog"),
        ("LanguageMachines", "toad"),
    ]),
    ("PICCL & TICCL","CLARIAH T26 [D1.3 (PICCL software); T1.4 (PICCL docs)]", [
        ("LanguageMachines", "PICCL"),
        ("LanguageMachines", "ticcltools"),
    ]),
    ("Timbl & Mbt","Pre-CLARIN", [
        ("LanguageMachines", "timbl"),
        ("LanguageMachines", "timblserver"),
        ("LanguageMachines", "mbt"),
        ("LanguageMachines", "mbtserver"),
        ("proycon", "python-timbl"),
    ]),
    ("Miscellaneous","Dependants of others", [
        ("LanguageMachines", "ticcutils"),
    ])
]

#map github logins to full names
names = {
    'proycon': "Maarten van Gompel",
    'kosloot': "Ko van der Sloot",
}

def cleanbody(s):
    out = ""
    for line in s.split('\n'):
        if all([c in ('-','*','=') for c in line.strip()]):
            continue
        if line.strip("\r\n") and line.strip("\r\n")[0] == "[" and line.strip("\r\n")[-1] == "]":
            out += "> \n" #extra newline
        out  += "> " + line.strip("\r\n") + "\n"
        if line.strip("\r\n") and line.strip("\r\n")[0] == "[" and line.strip("\r\n")[-1] == "]":
            out += "> \n" #extra newline
    return out


print("# Software Release and Progress Report\n")
print("Start date: ", begindate)
print("End date: ", enddate)
print()
print("## Short Summary\n")
print("(TODO: add manually)")
print()

headers = {
    'User-Agent': 'proycon/releasereport'
}

for group, references, repos in sorted(sources):
    print(f"## {group}")
    print()
    print("*Official task and deliverable references:* ", references)
    print()
    found = False
    for user, repo in sorted(repos, key= lambda x: x[1]):
        releases = requests.get(url=f"https://api.github.com/repos/{user}/{repo}/releases", auth=HTTPBasicAuth(username, pw), headers=headers).json()
        for release in releases:
            if release['published_at'][:10] >= begindate:
                found = True
                print("### " + repo + " " + release['tag_name'])
                print()
                print(cleanbody(release['body']))
                print()
                print(f"*(Released by " + names[release['author']['login']] + " on " + release['published_at'][:10] + ")*\n"  + f"https://github.com/{user}/{repo}/releases/tag/" + release['tag_name'])
                print()
    if not found:
        print(f"*(no releases since {begindate})*")
        print()
    print()

