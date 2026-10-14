#!/usr/bin/env python3
"""Fetch Vouch Digital's Google rating, review count and reviews, and save them to src/google_reviews.json.

Runs daily from .github/workflows/update-reviews.yml. Needs two settings on the GitHub repository:
  secret   GOOGLE_PLACES_API_KEY  (Google Cloud key with "Places API (New)" enabled)
  variable GOOGLE_PLACE_ID        (Vouch Digital's Google Maps place ID; find it with the "Find Place ID" workflow)

Google returns up to 5 reviews. Every review it returns is shown (no filtering), with the author's name and date.
"""
import datetime, json, os, pathlib, sys, urllib.request

key, place = os.environ.get("GOOGLE_PLACES_API_KEY"), os.environ.get("GOOGLE_PLACE_ID")
if not key or not place:
    sys.exit("GOOGLE_PLACES_API_KEY or GOOGLE_PLACE_ID is not set")

req = urllib.request.Request(
    f"https://places.googleapis.com/v1/places/{place}?languageCode=en-GB",
    headers={"X-Goog-Api-Key": key, "X-Goog-FieldMask": "displayName,rating,userRatingCount,reviews,googleMapsUri"})
data = json.load(urllib.request.urlopen(req, timeout=30))

name = data.get("displayName", {}).get("text", "")
if "vouch" not in name.lower():
    sys.exit(f"Refusing to update: GOOGLE_PLACE_ID points at '{name}', not Vouch Digital.")


def month(ts):
    try:
        return datetime.datetime.fromisoformat(ts.replace("Z", "+00:00")).strftime("%B %Y")
    except Exception:
        return ""


reviews = []
for r in data.get("reviews", []):
    text = (r.get("originalText") or r.get("text") or {}).get("text", "").strip()
    reviews.append({
        "name": r.get("authorAttribution", {}).get("displayName", "Google user"),
        "stars": int(r.get("rating", 5)),
        "text": text,
        "date": month(r.get("publishTime", "")),
        "published": r.get("publishTime", ""),
    })
reviews.sort(key=lambda r: r["published"], reverse=True)

out = {
    "rating": f'{data.get("rating", 0):.1f}',
    "count": int(data.get("userRatingCount", 0)),
    "maps_url": data.get("googleMapsUri", ""),
    "reviews": [{k: v for k, v in r.items() if k != "published"} for r in reviews],
}
path = pathlib.Path(__file__).resolve().parent.parent / "src" / "google_reviews.json"
old = path.read_text() if path.exists() else ""
new = json.dumps(out, indent=2, ensure_ascii=False) + "\n"
if new == old:
    print(f"No change: {out['rating']} from {out['count']} reviews")
else:
    path.write_text(new)
    print(f"Updated: {out['rating']} from {out['count']} reviews, {len(out['reviews'])} shown")
