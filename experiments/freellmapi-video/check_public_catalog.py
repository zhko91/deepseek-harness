#!/usr/bin/env python3
"""Read public Pollinations model catalog without credentials or generation."""
import json
import urllib.request

url="https://gen.pollinations.ai/v1/models"
req=urllib.request.Request(url,headers={"User-Agent":"freellmapi-video-catalog-probe/0.1"})
with urllib.request.urlopen(req,timeout=25) as response:
    obj=json.load(response)
models=obj.get("data",[]) if isinstance(obj,dict) else obj
print("Catalog entries:",len(models))
found=0
for model in models:
    if not isinstance(model,dict): continue
    mid=str(model.get("id",""))
    modalities=model.get("output_modalities",[])
    if "video" in modalities or any(x in mid.lower() for x in ("wan","veo","seedance","video")):
        print(json.dumps({"id":mid,"output_modalities":modalities,"pricing":model.get("pricing"),"paid_only":model.get("paid_only")},ensure_ascii=False))
        found+=1
print("Potential video models:",found)
print("Listing is informational; availability and zero-cost access NOT verified.")
