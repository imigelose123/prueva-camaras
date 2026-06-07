# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Simple Python script to list all cameras connected to the PC (webcams, virtual cameras, IP camera sources). Uses OpenCV for camera detection and FFmpeg for retrieving device names.

## Development Commands

```bash
# Install/restore dependencies
uv sync
uv pip install opencv-python

# Run the camera listing script
uv run listar_camaras.py
```

## Architecture

**listar_camaras.py** - Main script that:
1. Calls FFmpeg via subprocess to get camera device names (DirectShow on Windows)
2. Scans indices 0-15 using OpenCV VideoCapture to detect available cameras
3. Maps FFmpeg names to OpenCV indices and displays results

**FFmpeg Integration**: The script uses `ffmpeg -list_devices true -f dshow -i dummy` and parses stderr with regex to extract camera names. FFmpeg must be installed on the system.

**Dependencies**:
- opencv-python: Camera capture
- pywin32: Windows API (installed but not currently used)
