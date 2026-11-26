#!/usr/bin/env python3
"""Rebuild words.json: the guess dictionary is the union of every source list below plus assets/extra-words.txt.
Answer lists (common words the game picks from) are kept from the existing words.json.

Sources (download into a folder and pass it as the first argument):
  an-array-of-english-words@2.0.0   npm pack, extract to package/
  word-list@4.1.0                   npm pack, extract to x-word-list/
  wordlist-english@1.2.1            npm pack, extract to x-wordlist-english/
  ENABLE                            enable1.txt (public domain)
  SCOWL 2020.12.07, all levels      https://downloads.sourceforge.net/project/wordlist/SCOWL/2020.12.07/scowl-2020.12.07.tar.gz
"""
import glob, json, os, re, sys
src_dir = sys.argv[1]
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
p = lambda *a: os.path.join(src_dir, *a)
ok = re.compile('^[a-z]+$')
words = set()
words |= set(json.load(open(p('package/index.json'))))
words |= set(open(p('x-word-list/package/words.txt')).read().split())
for f in glob.glob(p('x-wordlist-english/package/*-words-*.json')): words |= set(json.load(open(f)))
words |= set(open(p('enable1.txt')).read().split())
for f in glob.glob(p('scowl-2020.12.07/final/*-words.*')): words |= set(open(f, encoding='latin-1').read().split())
words |= {l.strip() for l in open(os.path.join(root, 'assets/extra-words.txt')) if l.strip() and not l.startswith('#')}
words = {w for w in words if ok.match(w)}
wj = os.path.join(root, 'words.json')
old = json.load(open(wj))
out = {'answers': old['answers'], 'defs': old.get('defs', {}), 'valid': {str(n): sorted(w for w in words if len(w) == n) for n in (4, 5, 6)}}
json.dump(out, open(wj, 'w'), separators=(',', ':'))
print({n: len(v) for n, v in out['valid'].items()})
