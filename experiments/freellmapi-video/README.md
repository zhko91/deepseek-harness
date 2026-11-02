# FreeLLMAPI video experiment — isolated, no spending

## Confirmed upstream contract

Official documentation: https://github.com/tashfeenahmed/freellmapi/blob/main/docs/en/api/01-rest-api.md

- FreeLLMAPI can expose `POST /v1/videos/generations` through **Pollinations** or **Hugging Face** when video providers are configured and available.
- Request JSON: `prompt`, optional `model` (default `auto`), and provider-specific `duration`, `aspect_ratio`, `image`, `seed`, `audio`.
- Successful response is **binary MP4**; generation may take minutes and upstream has a ~5 minute timeout.
- An endpoint existing does NOT guarantee free credits, availability, supported image-to-video input, or fidelity to a person's face.

## What this branch contains

`probe_video.py` is an isolated Python standard-library client. Default behavior is **dry-run**, without network or paid inference. It only permits localhost HTTP to avoid accidentally sending images or credentials to unknown hosts. The script requires a locally running FreeLLMAPI instance and a unified key provided via environment variable before explicit `--generate`.

### Local dry-run

```powershell
python experiments/freellmapi-video/probe_video.py
```

### Actual generation (ONLY after confirming a free video provider in FreeLLMAPI dashboard)

```powershell
$env:FREELLMAPI_BASE_URL = "http://127.0.0.1:3001"
# Set FREELLMAPI_API_KEY privately in your terminal/session, never commit it
python experiments/freellmapi-video/probe_video.py --generate --duration 3
```

**Do not use real-person photos in the first provider test.** The default prompt uses a synthetic kite scene. No GitHub Actions workflow has been enabled; a GitHub-hosted runner cannot connect to your Windows localhost.

## Outstanding blockers

1. FreeLLMAPI installation and video provider settings have **not been verified** in this account.
2. No video provider free quota or account access has been verified.
3. No authenticated endpoint call or video generation has been executed.
4. The user wants real character movement with reference-image identity preservation; this needs a second, explicit image-to-video test after the synthetic clip works.

No merge into `master` until a real, safe validation succeeds.
