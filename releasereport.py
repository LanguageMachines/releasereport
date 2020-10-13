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
    ("CLAM","CLARIAH-PLUS WP3 T142", "https://github.com/LanguageMachines/clariah-plus-tasks/raw/master/di.huc/CLAM.T142.pdf", [
        ("proycon", "clam", "T142D1" ),
        ("proycon", "clamservices",""),
    ]),
    ("FoLiA","CLARIAH-PLUS WP3 T108", "https://github.com/LanguageMachines/clariah-plus-tasks/raw/master/di.huc/FoLiA.T108.pdf", [
        ("proycon", "folia", "T108D1"),
        ("proycon", "foliapy", "T108D3"),
        ("LanguageMachines", "libfolia", "T108D4"),
        ("proycon", "folia-rust", "T108D5"),
        ("proycon", "foliatools", "T108D6"),
        ("LanguageMachines", "foliautils", "T108D7"),
        ("proycon", "piereling", "T108D9"),
        ("cltl", "NAFFoLiAPy",""),
    ]),
    ("FLAT","CLARIAH-PLUS WP3 T062","https://github.com/LanguageMachines/clariah-plus-tasks/raw/master/di.huc/FLAT.T062.pdf", [
        ("proycon", "flat", "T062D1"),
        ("proycon", "foliadocserve", "T062D2"),
    ]),
    ("LaMachine","CLARIAH-PLUS WP3 T098", "https://github.com/LanguageMachines/clariah-plus-tasks/raw/master/di.huc/LaMachine.T098.pdf", [
        ("proycon", "LaMachine", "T098D1"),
        ("proycon", "labirinto","T098D2"),
        ("fbkarsdorp", "lamachine-homebrew","T098D3"),
        ("proycon", "codemetapy","T098D4"),
        ("proycon", "lamastats","T098D6"),
    ]),
    ("Frog, Ucto & DeepFrog","CLARIAH-PLUS WP3 T139", "https://github.com/LanguageMachines/clariah-plus-tasks/raw/master/di.huc/Frog.T139.pdf",  [
        ("LanguageMachines", "frog","T139aD1"),
        ("LanguageMachines", "frogdata","T139aD1.2"),
        ("proycon", "python-frog","T139aD1.3"),
        ("LanguageMachines", "toad",""),
        ("LanguageMachines", "ucto","T139aD2"),
        ("LanguageMachines", "uctodata","T139aD2.2"),
        ("proycon", "python-ucto","T139aD2.3"),
        ("proycon", "deepfrog","T139bD1"),
    ]),
    ("PICCL & TICCL","CLARIAH-PLUS WP3 ???","", [
        ("LanguageMachines", "PICCL",""),
        ("LanguageMachines", "ticcltools",""),
    ]),
    ("Nederlab","Nederlab","", [
        ("proycon", "nederlab-pipeline",""),
        ("proycon", "colibri-utils",""),
    ]),
    ("Timbl & Mbt","Pre-CLARIN","", [
        ("LanguageMachines", "timbl",""),
        ("LanguageMachines", "timblserver",""),
        ("LanguageMachines", "mbt",""),
        ("LanguageMachines", "mbtserver",""),
        ("proycon", "python-timbl",""),
    ]),
    ("Miscellaneous","Dependencies/wrappers and or unforeseen tools (related to CLARIAH projects)","", [
        ("LanguageMachines", "ticcutils",""),
        ("proycon", "aNtiLoPe",""),
        ("proycon", "wikiente",""),
    ]),
    ("Software Quality Guidelines","CLARIAH-CORE WP2 Task 54.100","", [
        ("CLARIAH", "software-quality-guidelines",""),
    ]),
]

if args.all:
    sources += [
        ("Gecco & Valkuil", "Implicit Linguisitics, Revisely","", [
            ("proycon","gecco",""),
            ("proycon","valkuil-gecco",""),
            ("proycon","valkuil",""),
        ]),
        ("Spreek2Schrijf", "Tweede Kamer der Staten Generaal","", [
           ("proycon", "spreek2schrijf",""),
        ]),
        ("Colibri", "Colibri PhD project","", [
           ("proycon", "colibri-core",""),
           ("proycon", "colibri-mt",""),
           ("proycon", "colibrita",""),
        ]),
        ("Colloquery", "Van Dale","", [
            ("proycon","colloquery",""),
        ]),
        ("T-Scan", "Utrecht University","", [
            ("proycon","tscan",""),
        ]),
        ("Oersetter", "Fryske Akademy","", [
            ("proycon","oersetter-webservice",""),
            ("proycon","oersetter-models",""),
        ]),
        ("BabelEnte", "TraMOOC","", [
            ("proycon","babelente",""),
            ("proycon","babelpy",""),
        ]),
        ("Deprecated projects", "(unfunded)","", [
            ("LanguageMachines", "LuigiNLP",""),
        ]),
        ("Shared-task software", "(unfunded)","", [
            ("LanguageMachines" ,"CLIN28_ST_spelling_correction",""),
            ("proycon" ,"anavec",""),
        ]),
        ("Various support software", "(mostly unfunded)","", [
            ("proycon", "parseme-support",""),
            ("proycon", "beeldbankvertaler",""),
        ]),
    ]

headers = {
    'User-Agent': 'proycon/releasereport'
}

users = set()
for _,_,_,repos in sorted(sources):
    for user, repo,_ in repos:
        users.add(user)

#Get a list of all repositories for the users
user_repos = defaultdict(dict)
for user in users:
    first = True
    url = f"https://api.github.com/users/{user}/repos"
    while first or ('next' in response.links and 'url' in response.links['next']):
        first = False
        print("Querying ", url,file=sys.stderr)
        response = requests.get(url=url, auth=HTTPBasicAuth(username, pw), headers=headers)
        for repo in response.json():
            user_repos[user][repo['name'].strip().lower()] = repo
        if 'next' in response.links and 'url' in response.links['next']:
            url = response.links['next']['url']

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


for group, references, tasklink, repos in sorted(sources):
    print(f"## {group}")
    print()
    if tasklink:
        print(f"*Project & Task ID:* [{references}]({tasklink})")
    else:
        print("*Project & Task ID:* ", references)
    print()
    found = False
    if args.verbose:
        print("*Repository details*:")
        print()
        for user, repo, del_id in sorted(repos, key= lambda x: x[1].lower()):
            found = False
            print("* **" + str(user_repos[user][repo.lower()]['name']) + f"** - ``https://github.com/{user}/{repo}``")
            if del_id:
                print("  - *deliverable ID*: " + str(del_id))
            print("  - *description*: " + str(user_repos[user][repo.lower()]['description']))
            if user_repos[user][repo.lower()]['homepage']:
                print("  - *website*: " + str(user_repos[user][repo.lower()]['homepage']))
            try:
                print("  - *license*: " + str(user_repos[user][repo.lower()]['license']['name']))
            except:
                pass
            print("  - *open issues*: " +  str(user_repos[user][repo.lower()]['open_issues']))
            print("  - *community interest*: " +  str(user_repos[user][repo.lower()]['stargazers_count']) + " stars, " + str(user_repos[user][repo.lower()]['watchers']) + " watchers, " + str(user_repos[user][repo.lower()]['forks']) + " forks")
        print()
        print("*Releases:*")
        print()
    for user, repo, del_id in sorted(repos, key= lambda x: x[1].lower()):
        first = True
        url = f"https://api.github.com/repos/{user}/{repo}/releases"
        while first or ('next' in response.links and 'url' in response.links['next']):
            first = False
            print("Querying ", url,file=sys.stderr)
            response = requests.get(url=url, auth=HTTPBasicAuth(username, pw), headers=headers)
            releases = response.json()
            for release in releases:
                if isinstance(release, dict) and 'published_at' in release:
                    if release['published_at'][:10] >= args.begin:
                        found = True
                        print("### " + repo + " " + release['tag_name'])
                        print()
                        print(cleanbody(release['body']))
                        print()
                        try:
                            namelabel = names[release['author']['login']]
                        except KeyError:
                            namelabel = release['author']['login']
                        print(f"*([Released](https://github.com/{user}/{repo}/releases/tag/" + release['tag_name'] + ") by " + namelabel + " on " + release['published_at'][:10] + ")*\n"  + f"https://github.com/{user}/{repo}/releases/tag/" + release['tag_name'])
                        if del_id:
                            print(f"*(deliverable ID: {del_id})*")
                        print()
            if not found and args.verbose:
                print("*(no releases for " + repo + " this period)*")
                print()
            if 'next' in response.links and 'url' in response.links['next']:
                url = response.links['next']['url']
    if not found and not args.verbose:
        print("*(no releases this period)*")
        print()
    print()
