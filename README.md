# hermes-openrouter-patch
Removes request headers from the installed Hermes agent to bypass 429 rate limits when using free OpenRouter models.

## Apply the patch
'''bash
curl -s https://raw.githubusercontent.com/AlexPurik/hermes-agent-patch/main/patch_openrouter.py | python3
'''