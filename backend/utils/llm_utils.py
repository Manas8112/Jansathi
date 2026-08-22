"""
Central utility to strip <think> tags from LLM responses.
Qwen and other reasoning models output internal chain-of-thought inside
<think>...</think> blocks. This strips them before showing the user.
"""
import re

def strip_think(text: str) -> str:
    """Remove <think>...</think> blocks from model output."""
    if not text:
        return text
    # Remove think blocks (including multi-line)
    cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    # Also strip any orphaned opening/closing tags
    cleaned = re.sub(r'</?think>', '', cleaned)
    return cleaned.strip()
