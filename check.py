#!/usr/bin/env python3
"""Bulk URL health checker."""
import sys, urllib.request, urllib.error, time
from concurrent.futures import ThreadPoolExecutor

def check(url):
    url = url.strip()
    if not url or url.startswith('#'): return None
    t0 = time.time()
    try:
        req = urllib.request.Request(url, headers={'User-Agent':'URLChecker/1.0'})
        with urllib.request.urlopen(req, timeout=10) as r:
            code = r.status
        ms = int((time.time()-t0)*1000)
        ok = "✅" if code < 400 else "⚠️"
        return f"{ok} {code} {ms:>5}ms  {url}"
    except urllib.error.HTTPError as e:
        ms = int((time.time()-t0)*1000)
        return f"⚠️  {e.code} {ms:>5}ms  {url}"
    except Exception as e:
        ms = int((time.time()-t0)*1000)
        return f"❌  ---  {ms:>5}ms  {url}  ({type(e).__name__})"

if len(sys.argv) < 2: print("Usage: check.py <file.txt|->"); sys.exit(1)
src = sys.stdin if sys.argv[1]=='-' else open(sys.argv[1])
urls = [l.strip() for l in src if l.strip() and not l.startswith('#')]
print(f"Checking {len(urls)} URLs...\n")
with ThreadPoolExecutor(max_workers=10) as ex:
    for r in ex.map(check, urls):
        if r: print(r)
