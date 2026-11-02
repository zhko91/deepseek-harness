#!/usr/bin/env python3
"""Direct Pollinations video client. Dry-run by default. Never logs secrets."""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

API = "https://gen.pollinations.ai/v1/videos/generations"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True, help="Exact video model ID from current catalog")
    p.add_argument("--prompt", default="A colorful paper kite sways in the wind, cinematic shot")
    p.add_argument("--duration", type=int, default=3)
    p.add_argument("--output", default="sample.mp4")
    p.add_argument("--generate", action="store_true")
    a = p.parse_args()
    if not 1 <= a.duration <= 5:
        sys.exit("Duration must be between 1 and 5 seconds")
    if not a.generate:
        print("DRY RUN ONLY: no API request, no Pollen spent.")
        print("Endpoint:", API, "model:", a.model, "duration:", a.duration)
        return
    key = os.environ.get("POLLINATIONS_API_KEY", "")
    if not key.startswith("sk_"):
        sys.exit("Missing secret key: set POLLINATIONS_API_KEY (sk_...) privately")
    if os.environ.get("CONFIRM_POLLEN_SPEND") != "YES":
        sys.exit("Safety stop: CONFIRM_POLLEN_SPEND must equal YES")
    payload = json.dumps({"model": a.model, "prompt": a.prompt, "duration": a.duration}).encode()
    request = urllib.request.Request(API, data=payload, headers={
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json",
        "Accept": "video/mp4",
    }, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=360) as response:
            data = response.read(75_000_001)
            if len(data) > 75_000_000 or b"ftyp" not in data[:32]:
                sys.exit("Unexpected response (not MP4 or too large); file not saved")
            with open(a.output, "wb") as output:
                output.write(data)
            print("Video saved:", a.output, "bytes:", len(data))
    except urllib.error.HTTPError as exc:
        print("API returned HTTP", exc.code, "(body omitted)")
        sys.exit(1)

if __name__ == "__main__":
    main()
