#!/usr/bin/env python3
"""
PreToolUse hook: sends filtered Discord notifications when Claude
launches subagents, uses skills, commits, or pushes.

Filtered to avoid spam — only notifies on significant actions.
"""

import json
import sys
import os
import subprocess

# Config
SETTINGS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "claudeclaw", "settings.json")

# Actions to notify about
NOTIFY_TOOLS = {
    "Agent": "🤖",
    "Skill": "⚡",
}

# Bash commands to notify about (matched via prefix)
NOTIFY_BASH_PREFIXES = [
    ("git commit", "📝"),
    ("git push", "🚀"),
    ("gh pr create", "🔗"),
    ("pnpm test", "🧪"),
    ("pnpm build", "🏗️"),
    ("npm test", "🧪"),
    ("npm run build", "🏗️"),
]


def load_discord_config():
    try:
        with open(SETTINGS_PATH, "r") as f:
            settings = json.load(f)
        dc = settings.get("discord", {})
        token = dc.get("token")
        channels = dc.get("listenChannels", [])
        channel_id = channels[0] if channels else None
        return token, channel_id
    except Exception:
        return None, None


def send_discord(token, channel_id, text):
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    data = json.dumps({"content": text})
    try:
        subprocess.run(
            [
                "curl", "-s", "-X", "POST", url,
                "-H", f"Authorization: Bot {token}",
                "-H", "Content-Type: application/json",
                "-d", data,
            ],
            timeout=4,
            capture_output=True,
        )
    except Exception:
        pass


def main():
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            print("{}")
            return

        event = json.loads(raw)
        tool_name = event.get("tool_name", "")
        tool_input = event.get("tool_input", {})

        token, channel_id = load_discord_config()
        if not token or not channel_id:
            print("{}")
            return

        message = None

        # Check if it's a tracked tool
        if tool_name in NOTIFY_TOOLS:
            emoji = NOTIFY_TOOLS[tool_name]
            if tool_name == "Agent":
                desc = tool_input.get("description", "subagent")
                agent_type = tool_input.get("subagent_type", "general")
                bg = " (bg)" if tool_input.get("run_in_background") else ""
                message = f"{emoji} Agent [{agent_type}]: {desc}{bg}"
            elif tool_name == "Skill":
                skill = tool_input.get("skill", "unknown")
                message = f"{emoji} Skill: /{skill}"

        # Check bash commands
        elif tool_name == "Bash":
            cmd = tool_input.get("command", "")
            for prefix, emoji in NOTIFY_BASH_PREFIXES:
                if cmd.strip().startswith(prefix):
                    short_cmd = cmd[:80] + ("..." if len(cmd) > 80 else "")
                    message = f"{emoji} {short_cmd}"
                    break

        if message:
            send_discord(token, channel_id, message)

    except Exception:
        pass

    print("{}")


if __name__ == "__main__":
    main()
