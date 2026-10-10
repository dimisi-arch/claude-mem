"""Find public-domain historical images for a video episode in museum open-access collections.

Usage: python3 find_images.py "search terms" [--limit N] [--download DIR] [--json]

Sources (no API key needed): Art Institute of Chicago, The Metropolitan Museum of Art,
Wikimedia Commons. Only items the source marks as public domain / CC0 are returned.
Standard library only, so it runs anywhere Python 3 does.
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = {"User-Agent": "claude-mem historical-images skill (https://github.com/dimisi-arch/claude-mem)"}


def get_json(url, retries=1):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code not in (403, 429) or not retries:
            raise
        # Met answers bursts with 403, Commons with 429: wait once, then try again.
        time.sleep(int(e.headers.get("Retry-After") or 5))
        return get_json(url, retries - 1)


def artic(query, limit):
    fields = "id,title,artist_display,date_display,image_id,is_public_domain"
    url = ("https://api.artic.edu/api/v1/artworks/search?"
           + urllib.parse.urlencode({"q": query, "fields": fields, "limit": limit * 3,
                                     "query[term][is_public_domain]": "true"}))
    out = []
    for a in get_json(url).get("data", []):
        if not (a.get("is_public_domain") and a.get("image_id")):
            continue
        out.append({
            "source": "Art Institute of Chicago",
            "title": a["title"],
            "artist": (a.get("artist_display") or "").split("\n")[0],
            "date": a.get("date_display") or "",
            "image": f"https://www.artic.edu/iiif/2/{a['image_id']}/full/1686,/0/default.jpg",
            "page": f"https://www.artic.edu/artworks/{a['id']}",
            "license": "CC0 (public domain)",
        })
    return out[:limit]


def met(query, limit):
    url = ("https://collectionapi.metmuseum.org/public/collection/v1.1/search?"
           + urllib.parse.urlencode({"q": query, "hasImages": "true", "limit": limit * 3}))
    out = []
    for oid in get_json(url).get("objectIDs") or []:
        time.sleep(0.3)  # one request per object: stay under the Met's burst limit
        o = get_json(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{oid}")
        if not (o.get("isPublicDomain") and o.get("primaryImage")):
            continue
        out.append({
            "source": "The Metropolitan Museum of Art",
            "title": o.get("title", ""),
            "artist": o.get("artistDisplayName") or o.get("culture") or "",
            "date": o.get("objectDate", ""),
            "image": o["primaryImage"],
            "page": o.get("objectURL", ""),
            "license": "CC0 (public domain)",
        })
        if len(out) >= limit:
            break
    return out


def commons(query, limit):
    url = ("https://commons.wikimedia.org/w/api.php?"
           + urllib.parse.urlencode({
               "action": "query", "format": "json", "generator": "search",
               "gsrsearch": f"{query} filetype:bitmap", "gsrnamespace": 6, "gsrlimit": limit * 3,
               "prop": "imageinfo", "iiprop": "url|extmetadata", "iiurlwidth": 1920}))
    out = []
    pages = (get_json(url).get("query") or {}).get("pages", {})
    for p in sorted(pages.values(), key=lambda p: p.get("index", 0)):
        info = (p.get("imageinfo") or [{}])[0]
        meta = info.get("extmetadata", {})
        lic = meta.get("LicenseShortName", {}).get("value", "")
        if not re.search(r"public domain|^pd|cc0", lic, re.I):
            continue
        strip = lambda s: " ".join(re.sub(r"<[^>]+>|date QS:\S+", "", s or "").split())
        out.append({
            "source": "Wikimedia Commons",
            "title": strip(meta.get("ObjectName", {}).get("value")) or p["title"].removeprefix("File:"),
            "artist": strip(meta.get("Artist", {}).get("value"))[:80],
            "date": strip(meta.get("DateTimeOriginal", {}).get("value"))[:40],
            "image": info.get("thumburl") or info.get("url", ""),
            "page": info.get("descriptionurl", ""),
            "license": lic,
        })
        if len(out) >= limit:
            break
    return out


def download(items, folder):
    os.makedirs(folder, exist_ok=True)
    for i, it in enumerate(items, 1):
        name = re.sub(r"[^\w-]+", "_", it["title"])[:60].strip("_") or "bild"
        path = os.path.join(folder, f"{i:02d}_{name}.jpg")
        req = urllib.request.Request(it["image"], headers=UA)
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
        except urllib.error.URLError as e:
            # The Art Institute's image server sits behind a Cloudflare bot check that refuses
            # cloud addresses; the link still opens in a normal browser.
            it["file"] = f"not downloaded ({e}); open the link in a browser"
            continue
        with open(path, "wb") as f:
            f.write(data)
        it["file"] = path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query")
    ap.add_argument("--limit", type=int, default=5, help="results per source (default 5)")
    ap.add_argument("--download", metavar="DIR", help="also save the images into DIR")
    ap.add_argument("--json", action="store_true", help="print JSON instead of a table")
    args = ap.parse_args()

    items = []
    for fn in (artic, met, commons):
        try:
            items += fn(args.query, args.limit)
        except Exception as e:  # one source down must not cost the others
            print(f"note: {fn.__name__} failed: {e}", file=sys.stderr)
    if args.download and items:
        download(items, args.download)

    if args.json:
        print(json.dumps(items, ensure_ascii=False, indent=2))
        return
    if not items:
        print("No public-domain results. Try English terms, the Greek/Latin name, or a broader word.")
        return
    for i, it in enumerate(items, 1):
        print(f"{i}. {it['title']} — {it['artist']} ({it['date']})\n"
              f"   {it['source']}, {it['license']}\n   Bild: {it['image']}\n   Quelle: {it['page']}"
              + (f"\n   Datei: {it['file']}" if it.get("file") else ""))


if __name__ == "__main__":
    main()
