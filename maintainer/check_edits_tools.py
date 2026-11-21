#!/usr/bin/env python3
"""Compare the live Edits for Mac MCP tool list with the committed snapshot.

Usage:
  python3 maintainer/check_edits_tools.py            # diff live vs snapshot
  python3 maintainer/check_edits_tools.py --update   # rewrite the snapshot

Edits must be open with the automation server enabled. The server URL and bearer
token are read from the Claude Code MCP entry in ~/.claude.json (any server whose URL
points at 127.0.0.1:19501), or from EDITS_MCP_URL / EDITS_MCP_TOKEN. The token is
never printed. Only read-only calls are made (initialize, tools/list, appState,
getCapabilities).

For maintainers only — the skills don't need this script.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

DEFAULT_URL = "http://127.0.0.1:19501/mcp"
SNAPSHOT = Path(__file__).with_name("edits-tools-snapshot.json")
PROTOCOL_VERSION = "2025-06-18"


@dataclass(frozen=True)
class ServerConfig:
    url: str
    token: str


@dataclass(frozen=True)
class Snapshot:
    schema_version: str
    screen: str
    tools: tuple[str, ...]


class ConfigError(Exception):
    pass


class ServerError(Exception):
    pass


def config_from_env() -> ServerConfig | None:
    token = os.environ.get("EDITS_MCP_TOKEN")
    if not token:
        return None
    return ServerConfig(os.environ.get("EDITS_MCP_URL", DEFAULT_URL), token)


def config_from_claude() -> ServerConfig | None:
    path = Path.home() / ".claude.json"
    if not path.is_file():
        return None
    servers = json.loads(path.read_text()).get("mcpServers", {})
    for entry in servers.values():
        if "127.0.0.1:19501" not in str(entry.get("url", "")):
            continue
        auth = entry.get("headers", {}).get("Authorization", "")
        if not auth.startswith("Bearer "):
            continue
        return ServerConfig(entry["url"], auth.removeprefix("Bearer "))
    return None


def load_config() -> ServerConfig:
    config = config_from_env() or config_from_claude()
    if config is None:
        raise ConfigError("no Edits MCP config: set EDITS_MCP_TOKEN or add the server to Claude Code")
    return config


class EditsClient:
    def __init__(self, config: ServerConfig) -> None:
        self._config = config
        self._session: str | None = None

    def _post(self, payload: dict) -> dict:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Authorization": f"Bearer {self._config.token}",
        }
        if self._session:
            headers["Mcp-Session-Id"] = self._session
        request = urllib.request.Request(self._config.url, json.dumps(payload).encode(), headers)
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                self._session = response.headers.get("Mcp-Session-Id") or self._session
                body = response.read().decode()
        except urllib.error.URLError as error:
            raise ServerError(f"cannot reach Edits ({error.reason}); is Edits open with automation on?") from error
        return parse_body(body)

    def initialize(self) -> None:
        self._post({
            "jsonrpc": "2.0", "id": 0, "method": "initialize",
            "params": {"protocolVersion": PROTOCOL_VERSION, "capabilities": {},
                       "clientInfo": {"name": "edits-skills-maintainer", "version": "1"}},
        })
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def tool_names(self) -> tuple[str, ...]:
        result = self._post({"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}})
        return tuple(sorted(tool["name"] for tool in result.get("result", {}).get("tools", [])))

    def call_json(self, tool: str) -> dict:
        result = self._post({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                             "params": {"name": tool, "arguments": {}}})
        content = result.get("result", {}).get("content", [])
        if not content:
            raise ServerError(f"{tool} returned no content")
        return json.loads(content[0].get("text", "{}"))


def parse_body(body: str) -> dict:
    if not body.strip():
        return {}
    if not body.lstrip().startswith(("event:", "data:")):
        return json.loads(body)
    data_lines = [line[5:].strip() for line in body.splitlines() if line.startswith("data:")]
    return json.loads(data_lines[-1]) if data_lines else {}


def read_live(client: EditsClient) -> Snapshot:
    client.initialize()
    screen = str(client.call_json("appState").get("screen", "?"))
    schema = str(client.call_json("getCapabilities").get("schemaVersion", "?"))
    return Snapshot(schema, screen, client.tool_names())


def read_snapshot() -> dict[str, Snapshot]:
    if not SNAPSHOT.is_file():
        return {}
    raw = json.loads(SNAPSHOT.read_text())
    return {screen: Snapshot(v["schemaVersion"], screen, tuple(v["tools"])) for screen, v in raw.items()}


def write_snapshot(snapshots: dict[str, Snapshot]) -> None:
    data = {s.screen: {"schemaVersion": s.schema_version, "tools": list(s.tools)} for s in snapshots.values()}
    SNAPSHOT.write_text(json.dumps(data, indent=1) + "\n")


def report(live: Snapshot, saved: Snapshot | None) -> int:
    print(f"screen={live.screen} schema={live.schema_version} tools={len(live.tools)}")
    if saved is None:
        print("no snapshot for this screen yet; run with --update")
        return 1
    added = sorted(set(live.tools) - set(saved.tools))
    removed = sorted(set(saved.tools) - set(live.tools))
    if saved.schema_version != live.schema_version:
        print(f"schema changed: {saved.schema_version} -> {live.schema_version}")
    for name in added:
        print(f"+ {name}")
    for name in removed:
        print(f"- {name}  (check every skill that mentions it)")
    unchanged = not added and not removed and saved.schema_version == live.schema_version
    print("no changes" if unchanged else "changes found: update skills, CHANGELOG and the README test date")
    return 0 if unchanged else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Diff the live Edits MCP tool list against the snapshot.")
    parser.add_argument("--update", action="store_true", help="write the live list into the snapshot")
    args = parser.parse_args(argv)

    try:
        live = read_live(EditsClient(load_config()))
    except (ConfigError, ServerError) as error:
        print(f"error: {error}")
        return 2

    snapshots = read_snapshot()
    if args.update:
        snapshots[live.screen] = live
        write_snapshot(snapshots)
        print(f"snapshot updated for screen={live.screen} ({len(live.tools)} tools)")
        return 0
    return report(live, snapshots.get(live.screen))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
