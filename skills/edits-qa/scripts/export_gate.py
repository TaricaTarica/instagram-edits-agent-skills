#!/usr/bin/env python3
"""Validate an exported Reel before it is handed to the creator.

Usage: python3 export_gate.py <video> [--max-seconds 90] [--target-lufs -14] [--lufs-tolerance 2]

Checks: vertical 9:16 >= 1080x1920, video + audio streams, audio not silent,
duration limit, integrated loudness and true peak. Requires ffprobe and ffmpeg on PATH.
Exit code 0 when every blocking check passes.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

MIN_WIDTH = 1080
MIN_HEIGHT = 1920
ASPECT = 9 / 16
ASPECT_TOLERANCE = 0.01
SILENCE_DB = -50.0
MAX_TRUE_PEAK = -1.0


class Status(Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


@dataclass(frozen=True)
class Check:
    name: str
    status: Status
    detail: str


@dataclass(frozen=True)
class StreamInfo:
    width: int
    height: int
    codec: str
    fps: float
    duration: float
    has_audio: bool


@dataclass(frozen=True)
class Loudness:
    integrated_lufs: float
    true_peak_db: float
    mean_volume_db: float


class ProbeError(Exception):
    pass


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def parse_fps(rate: str) -> float:
    if "/" not in rate:
        return float(rate or 0)
    num, den = rate.split("/")
    if float(den) == 0:
        return 0.0
    return float(num) / float(den)


def probe(path: Path) -> StreamInfo:
    proc = run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)])
    if proc.returncode != 0:
        raise ProbeError(proc.stderr.strip() or "ffprobe failed")

    data = json.loads(proc.stdout)
    streams = data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    if video is None:
        raise ProbeError("no video stream")

    return StreamInfo(
        width=int(video.get("width", 0)),
        height=int(video.get("height", 0)),
        codec=str(video.get("codec_name", "?")),
        fps=parse_fps(str(video.get("avg_frame_rate", "0/1"))),
        duration=float(data.get("format", {}).get("duration", 0.0)),
        has_audio=any(s.get("codec_type") == "audio" for s in streams),
    )


def measure_loudness(path: Path) -> Loudness:
    ebur = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"])
    vol = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"])
    integrated = re.findall(r"I:\s+(-?[\d.]+) LUFS", ebur.stderr)
    peak = re.findall(r"Peak:\s+(-?[\d.]+|-inf) dBFS", ebur.stderr)
    mean = re.findall(r"mean_volume:\s+(-?[\d.]+|-inf) dB", vol.stderr)
    if not integrated or not mean:
        raise ProbeError("could not measure loudness")

    return Loudness(
        integrated_lufs=float(integrated[-1]),
        true_peak_db=float(peak[-1]) if peak and peak[-1] != "-inf" else float("-inf"),
        mean_volume_db=float(mean[-1]) if mean[-1] != "-inf" else float("-inf"),
    )


def check_frame(info: StreamInfo) -> Check:
    detail = f"{info.width}x{info.height} {info.codec} {info.fps:.2f} fps"
    if info.height == 0 or abs(info.width / info.height - ASPECT) > ASPECT_TOLERANCE:
        return Check("frame 9:16", Status.FAIL, detail)
    if info.width < MIN_WIDTH or info.height < MIN_HEIGHT:
        return Check("frame 9:16", Status.WARN, f"{detail} (below 1080x1920)")
    return Check("frame 9:16", Status.PASS, detail)


def check_duration(info: StreamInfo, max_seconds: float) -> Check:
    detail = f"{info.duration:.2f}s (limit {max_seconds:.0f}s)"
    if info.duration <= 0:
        return Check("duration", Status.FAIL, detail)
    if info.duration > max_seconds:
        return Check("duration", Status.WARN, detail)
    return Check("duration", Status.PASS, detail)


def check_audio_present(info: StreamInfo) -> Check:
    if not info.has_audio:
        return Check("audio stream", Status.FAIL, "no audio stream")
    return Check("audio stream", Status.PASS, "present")


def check_not_silent(loud: Loudness) -> Check:
    detail = f"mean {loud.mean_volume_db:.1f} dB"
    if loud.mean_volume_db <= SILENCE_DB:
        return Check("audio not silent", Status.FAIL, f"{detail} — licensed music dropped in export?")
    return Check("audio not silent", Status.PASS, detail)


def check_loudness(loud: Loudness, target: float, tolerance: float) -> Check:
    detail = f"{loud.integrated_lufs:.1f} LUFS (target {target:.0f} ±{tolerance:.0f})"
    if abs(loud.integrated_lufs - target) > tolerance:
        return Check("loudness", Status.WARN, detail)
    return Check("loudness", Status.PASS, detail)


def check_peak(loud: Loudness) -> Check:
    detail = f"true peak {loud.true_peak_db:.1f} dBFS (max {MAX_TRUE_PEAK:.0f})"
    if loud.true_peak_db > MAX_TRUE_PEAK:
        return Check("true peak", Status.WARN, detail)
    return Check("true peak", Status.PASS, detail)


def run_checks(path: Path, max_seconds: float, target: float, tolerance: float) -> list[Check]:
    info = probe(path)
    checks = [check_frame(info), check_duration(info, max_seconds), check_audio_present(info)]
    if not info.has_audio:
        return checks

    loud = measure_loudness(path)
    return checks + [check_not_silent(loud), check_loudness(loud, target, tolerance), check_peak(loud)]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate an exported Reel.")
    parser.add_argument("video", type=Path)
    parser.add_argument("--max-seconds", type=float, default=90.0)
    parser.add_argument("--target-lufs", type=float, default=-14.0)
    parser.add_argument("--lufs-tolerance", type=float, default=2.0)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if not args.video.is_file():
        print(f"FAIL  file: not found {args.video}")
        return 1
    if shutil.which("ffprobe") is None or shutil.which("ffmpeg") is None:
        print("FAIL  tools: ffmpeg/ffprobe not on PATH — use probeMedia and loudness in Edits instead")
        return 1

    try:
        checks = run_checks(args.video, args.max_seconds, args.target_lufs, args.lufs_tolerance)
    except ProbeError as error:
        print(f"FAIL  probe: {error}")
        return 1

    for check in checks:
        print(f"{check.status.value:<5} {check.name}: {check.detail}")
    return 1 if any(c.status is Status.FAIL for c in checks) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
