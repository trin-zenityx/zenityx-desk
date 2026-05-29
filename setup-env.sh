#!/usr/bin/env bash
# RustDesk (ZenityX fork) build env — keeps all heavy toolchains on the SSD.
# Usage:  source setup-env.sh   (run before any cargo/flutter/build.py command)

SSD_TOOLS="/Volumes/Studio/toolchains"

# --- Rust ---
export RUSTUP_HOME="$SSD_TOOLS/rustup"
export CARGO_HOME="$SSD_TOOLS/cargo"

# --- Flutter / Dart ---
export FLUTTER_ROOT="$SSD_TOOLS/flutter"
export PUB_CACHE="$SSD_TOOLS/pub-cache"

# --- vcpkg (C/C++ deps) ---
export VCPKG_ROOT="$SSD_TOOLS/vcpkg"

# --- PATH ---
export PATH="$CARGO_HOME/bin:$FLUTTER_ROOT/bin:$VCPKG_ROOT:$PATH"

echo "ZenityX RustDesk env loaded:"
echo "  RUSTUP_HOME=$RUSTUP_HOME"
echo "  CARGO_HOME=$CARGO_HOME"
echo "  FLUTTER_ROOT=$FLUTTER_ROOT"
echo "  VCPKG_ROOT=$VCPKG_ROOT"
