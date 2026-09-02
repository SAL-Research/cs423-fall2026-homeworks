#!/usr/bin/env bash
# Build the CS 423 course gem5 image locally (fallback if you cannot pull the
# prebuilt image). One-time cost: ~30-60 min of compilation.
#
# Usage:  ./build.sh
set -euo pipefail
cd "$(dirname "$0")"

IMAGE="${CS423_IMAGE:-s4lbot/cs423-gem5:v25.1.0.1}"

docker build -t "$IMAGE" .
echo
echo "Built $IMAGE for your native architecture."
docker run --rm "$IMAGE" cat /opt/gem5/GEM5_VERSION
