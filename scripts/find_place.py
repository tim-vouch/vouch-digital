#!/usr/bin/env python3
"""List Google places matching a search, with their Place IDs, ratings and review counts.
Run from GitHub: Actions > Find Place ID > Run workflow."""
import json, os, sys, urllib.request

key, query = os.environ.get("GOOGLE_PLACES_API_KEY"), os.environ.get("QUERY")
if not key or not query:
    sys.exit("GOOGLE_PLACES_API_KEY or QUERY is not set")
req = urllib.request.Request(
    "https://places.googleapis.com/v1/places:searchText",
    data=json.dumps({"textQuery": query, "regionCode": "GB", "includePureServiceAreaBusinesses": True}).encode(),
    headers={"Content-Type": "application/json", "X-Goog-Api-Key": key,
             "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.rating,places.userRatingCount"})
places = json.load(urllib.request.urlopen(req, timeout=30)).get("places", [])
if not places:
    print("No matches")
for p in places:
    print(f'{p["displayName"]["text"]} | {p.get("formattedAddress", "no address")} | '
          f'{p.get("rating", "-")} from {p.get("userRatingCount", 0)} reviews | PLACE ID: {p["id"]}')
