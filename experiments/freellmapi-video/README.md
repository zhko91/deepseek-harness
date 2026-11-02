# FreeLLMAPI — video capability probe (isolated)

This experiment does **not** assume that FreeLLMAPI supports video generation. It only inspects the OpenAI-compatible `/models` endpoint if a user-provided base URL is configured.

No credentials or photos are committed. No paid endpoints are invoked. Do not use a private token in workflow inputs; configure secrets separately if later required.

## Result interpretation
- Model listing alone does not prove video-generation capability.
- A provider-specific documented video endpoint and a successful short generation are required before claiming support.
- Standard GitHub Actions runners do not provide the GPU needed for large local video diffusion models.

## Next steps
1. Confirm FreeLLMAPI's official base URL and supported endpoints (not yet verified).
2. Test an authenticated model listing using a masked secret, never printing the key.
3. If video generation is supported, test a short clip with a non-personal synthetic image and confirm cost before sending a request.
4. Keep the original deepseek-harness build and workflows unchanged.

Status: **research and isolation only; video generation NOT RUN**.
