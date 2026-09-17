#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bascule le tag Amazon Partenaires sur tout le blog.
Usage : python switch_tag_amazon.py NOUVEAUTAG       (ex : affilmax-21)
        python switch_tag_amazon.py NOUVEAUTAG --push  (commit + push auto)
"""
import os, re, sys, subprocess, glob

NEW = sys.argv[1] if len(sys.argv) > 1 else ""
PUSH = "--push" in sys.argv
OLD = "confortbure07-21"
if not re.fullmatch(r"[a-zA-Z0-9-]{3,30}", NEW):
    sys.exit("Tag invalide. Exemple : python switch_tag_amazon.py affilmax-21")

os.chdir(os.path.dirname(os.path.abspath(__file__)))
changed = files = 0
for path in glob.glob("posts/*.html") + ["index.html"]:
    if not os.path.isfile(path): continue
    html = open(path, encoding="utf-8", errors="replace").read()
    n = html.count(OLD)
    if n:
        open(path, "w", encoding="utf-8").write(html.replace(OLD, NEW))
        changed += n; files += 1
print(f"OK : {changed} liens bascules dans {files} fichiers -> tag {NEW}")

# sitemap : rien a changer (pas de tag dedans)
if PUSH and changed:
    subprocess.run(["git", "add", "posts", "index.html"], check=True)
    subprocess.run(["git", "commit", "-m", f"Tag Amazon -> {NEW}"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("Pushe et en ligne dans ~1 min (GitHub Pages).")
elif changed:
    print("(sans --push : rien commite. Relance avec --push pour publier.)")
