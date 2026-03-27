#!/usr/bin/env python3
"""
Skill Activation Hook — UserPromptSubmit

Reads the user's prompt, matches keywords against skill-rules.json,
and injects a systemMessage suggesting the relevant skill.

Input (stdin): JSON with "userMessage" field
Output (stdout): JSON with optional "systemMessage" field
"""

import json
import os
import re
import sys


def load_rules():
    """Load skill rules from skill-rules.json."""
    rules_path = os.path.join(os.path.dirname(__file__), "skill-rules.json")
    try:
        with open(rules_path) as f:
            return json.load(f)["rules"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return []


def match_skill(prompt: str, rules: list) -> dict | None:
    """Find the best matching skill for a prompt."""
    prompt_lower = prompt.lower()
    best_match = None
    best_score = 0

    for rule in rules:
        # Check exclude keywords first
        exclude = rule.get("excludeKeywords", [])
        if any(kw.lower() in prompt_lower for kw in exclude):
            continue

        # Count keyword matches
        keywords = rule.get("keywords", [])
        score = sum(1 for kw in keywords if kw.lower() in prompt_lower)

        if score == 0:
            continue

        # Check requireContext (at least one must match if specified)
        require_ctx = rule.get("requireContext", [])
        if require_ctx and not any(ctx.lower() in prompt_lower for ctx in require_ctx):
            # Reduce score but don't disqualify entirely
            score *= 0.3

        if score > best_score:
            best_score = score
            best_match = rule

    return best_match if best_score >= 1 else None


def is_skill_invocation(prompt: str) -> bool:
    """Check if the prompt is already a skill invocation."""
    return prompt.strip().startswith("/")


def is_casual_message(prompt: str) -> bool:
    """Check if this is a casual/short message that doesn't need skill activation."""
    casual_patterns = [
        r"^(ok|oui|non|yes|no|merci|thanks|cool|nice|parfait|done|go|salut|hey|yo)\b",
        r"^(telegram|message|msg)\s",
        r"^\[telegram",
        r"^\[.*\]\s*\[telegram",
        r"^continue",
        r"^start the heartbeat",
        r"^continue from where",
    ]
    prompt_stripped = prompt.strip().lower()
    if len(prompt_stripped) < 15:
        return True
    return any(re.match(p, prompt_stripped) for p in casual_patterns)


def main():
    try:
        input_data = json.load(sys.stdin)
        prompt = input_data.get("userMessage", "")

        # Skip if already a skill invocation or casual message
        if is_skill_invocation(prompt) or is_casual_message(prompt):
            print(json.dumps({}))
            sys.exit(0)

        rules = load_rules()
        match = match_skill(prompt, rules)

        if match:
            hint = (
                f"💡 Skill suggestion: Consider using `{match['skill']}` "
                f"for this task ({match['description']}). "
                f"Use it if appropriate, but don't force it if the task is simpler than what the skill handles."
            )
            print(json.dumps({"systemMessage": hint}))
        else:
            print(json.dumps({}))

    except Exception:
        # Never block the user — fail silently
        print(json.dumps({}))

    sys.exit(0)


if __name__ == "__main__":
    main()
