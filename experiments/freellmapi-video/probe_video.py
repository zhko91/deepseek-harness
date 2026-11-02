#!/usr/bin/env python3
"""Explicit opt-in FreeLLMAPI video test. Never prints tokens."""
import argparse
import os
import sys
import urllib.request
import urllib.error
import urllib.parse

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--prompt", default="A paper kite sways gently in a sunny garden, steady camera")
    p.add_argument("--output", default="test_video.mp4")
    p.add_argument("--duration", type=int, default=3)
    p.add_argument("--generate", action="store_true", help="Explicitly request provider inference")
    a=p.parse_args()
    base=os.getenv("FREELLMAPI_BASE_URL", "http://127.0.0.1:3001").rstrip("/")
    u=urllib.parse.urlparse(base)
    if u.scheme!="http" or u.hostname not in ("localhost","127.0.0.1","::1"):
        sys.exit("Safety stop: only local HTTP FreeLLMAPI is supported in this experiment")
    if not a.generate:
        print("DRY RUN: no video requested. Set up local FreeLLMAPI, confirm zero-cost provider, then use --generate.")
        return
    if not 1<=a.duration<=6:
        sys.exit("Duration must be 1..6 seconds")
    key=os.getenv("FREELLMAPI_API_KEY")
    if not key:
        sys.exit("Missing FREELLMAPI_API_KEY environment variable")
    import json
    data=json.dumps({"model":"auto","prompt":a.prompt,"duration":a.duration}).encode()
    req=urllib.request.Request(base+"/v1/videos/generations",data=data,headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"},method="POST")
    try:
        with urllib.request.urlopen(req,timeout=330) as response:
            content=response.read(75_000_001)
            if len(content)>75_000_000 or not (content[:32].find(b"ftyp")>=0):
                sys.exit("Response is not a valid-sized MP4 container")
            with open(a.output,"wb") as f: f.write(content)
            print("Saved MP4:",a.output,"bytes:",len(content))
    except urllib.error.HTTPError as e:
        print("Provider returned HTTP",e.code,"(response omitted to protect credentials)")
        sys.exit(1)

if __name__=="__main__":
    main()
