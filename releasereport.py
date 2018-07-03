#!/usr/bin/env python3

import sys
import requests
import datetime
import os
from collections import defaultdict
from requests.auth import HTTPBasicAuth

import argparse
parser = argparse.ArgumentParser(description="Report generator", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--all', help="Add non-CLARIN projects as well",  action='store_true')
parser.add_argument('--verbose', help="List all software, even if there are no releases, and adds descriptions",  action='store_true')
parser.add_argument('--begin', type=str,help="Begin date (YYYY-MM-DD)", action='store',default="",required=True)
parser.add_argument('--end', type=str,help="End date (YYYY-MM-DD)", action='store',default=datetime.datetime.now().strftime("%Y-%m-%d"),required=False)
args = parser.parse_args()
#args.storeconst, args.dataset, args.num, args.bar


username = os.environ['GITHUB_USER']
pw = os.environ['GITHUB_PASS']

sources = [
    ("CLAM","CLARIAH WP3 T21 [D2.8 (software); D2.9 (doc)]", [
        ("proycon", "clam"),
        ("proycon", "clamservices"),
    ]),
    ("FoLiA","CLARIAH WP3 T71 [D2.5 (libs); D2.6 (docs); D2.7 (tools)]", [
        ("proycon", "folia"),
        ("proycon", "pynlpl"),
        ("LanguageMachines", "libfolia"),
        ("LanguageMachines", "foliautils"),
        ("cltl", "NAFFoLiAPy"),
    ]),
    ("FLAT","CLARIAH WP3 T24 [D2.10 (software); D2.11 (docs)]", [
        ("proycon", "flat"),
        ("proycon", "foliadocserve"),
    ]),
    ("LaMachine","CLARIAH WP3: LaMachine v2 plan in scope of CLARIAH WP3 VRE", [
        ("proycon", "LaMachine"),
        ("proycon", "labirinto"),
        ("proycon", "codemetapy"),
    ]),
    ("Ucto","CLARIAH WP3 T55 [D1.1 (software), D1.2 (docs)]", [
        ("LanguageMachines", "ucto"),
        ("LanguageMachines", "uctodata"),
        ("proycon", "python-ucto"),
    ]),
    ("Frog","CLARIAH WP3 T22 [D2.1 (software); D2.2 (doc)]; T23 [D2.3 (froggen software), D2.4 (froggen docs)]", [
        ("LanguageMachines", "frog"),
        ("LanguageMachines", "frogdata"),
        ("proycon", "python-frog"),
        ("LanguageMachines", "toad"),
    ]),
    ("PICCL & TICCL","CLARIAH WP3 T26 [D1.3 (PICCL software); T1.4 (PICCL docs)]", [
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
    ]),
    ("Software Quality Guidelines","CLARIAH WP2 Task 54.100", [
        ("CLARIAH", "software-quality-guidelines"),
    ]),
]

if args.all:
    sources += [
        ("Gecco & Valkuil", "Implicit Linguisitics, Revisely", [
            ("proycon","gecco"),
            ("proycon","valkuil-gecco"),
            ("proycon","valkuil"),
        ]),
        ("Spreek2Schrijf", "Tweede Kamer der Staten Generaal", [
           ("proycon", "spreek2schrijf"),
        ]),
        ("Colibri", "Colibri PhD project", [
           ("proycon", "colibri-core"),
           ("proycon", "colibri-mt"),
           ("proycon", "colibrita"),
        ]),
        ("Colloquery", "Van Dale", [
            ("proycon","colloquery"),
        ]),
        ("T-Scan", "Utrecht University", [
            ("proycon","tscan"),
        ]),
        ("Oersetter", "Fryske Akademy", [
            ("proycon","oersetter-webservice"),
            ("proycon","oersetter-models"),
        ]),
        ("BabelEnte", "TraMOOC", [
            ("proycon","babelente"),
            ("proycon","babelpy"),
        ]),
        ("Deprecated projects", "(unfunded)", [
            ("LanguageMachine", "LuigiNLP"),
        ]),
        ("Shared-task software", "(unfunded)", [
            ("LanguageMachines" ,"CLIN28_ST_spelling_correction"),
            ("proycon" ,"anavec"),
        ]),
        ("Various support software", "(mostly unfunded)", [
            ("proycon", "lamastats"),
            ("proycon", "parseme-support"),
            ("proycon", "beeldbankvertaler"),
        ]),
    ]


users = set()
for _,_, repos in sorted(sources):
    for user, repo in repos:
        users.add(user)

#Get a list of all repositories for the users
user_repos = defaultdict(dict)
for user in users:
    for repo in requests.get(url=f"https://api.github.com/users/{user}/repos", auth=HTTPBasicAuth(username, pw), headers=headers).json():
        user_repos[user][repo['name'].lower()] = repo

#map github logins to verbose names
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
print("Start date: ", args.begin)
print("End date: ", args.end)
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
    if args.all:
        print("*Project/Task/Funder:* ", references)
    else:
        print("*Official task and deliverable references:* ", references)
    print()
    found = False
    for user, repo in sorted(repos, key= lambda x: x[1]):
        releases = requests.get(url=f"https://api.github.com/repos/{user}/{repo}/releases", auth=HTTPBasicAuth(username, pw), headers=headers).json()
        if args.verbose:
            found = False
            print("### " + repo)
            print()
            print("*Description:* ", user_repos[user][repo.lower()]['description'])
            print()
        for release in releases:
            if release['published_at'][:10] >= args.begin:
                found = True
                if args.verbose:
                    print("#### " + repo + " " + release['tag_name'])
                else:
                    print("### " + repo + " " + release['tag_name'])
                print()
                print(cleanbody(release['body']))
                print()
                print(f"*(Released by " + names[release['author']['login']] + " on " + release['published_at'][:10] + ")*\n"  + f"https://github.com/{user}/{repo}/releases/tag/" + release['tag_name'])
                print()
        if not found and args.verbose:
            print(f"*(no releases this period)*")
            print()
    if not found and not args.verbose:
        print(f"*(no releases this period)*")
        print()
    print()

