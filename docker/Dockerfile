# CS 423 course gem5 image — Fall 2026
# gem5 v25.1.0.1 (RISCV, gem5.opt) + riscv64 cross toolchain + plotting deps.
#
# Prebuilt image:  s4lbot/cs423-gem5:v25.1.0.1   (Docker Hub)
# Fallback build:  ./build.sh   (30-60 min one-time compile)
#
# Base image is the official gem5 dependency image (multi-arch: amd64 + arm64),
# pinned to the v25-1 line. Never switch to `latest`.

# ---- stage 1: compile gem5 --------------------------------------------------
FROM ghcr.io/gem5/ubuntu-24.04_all-dependencies:v25-1 AS build

ARG GEM5_TAG=v25.1.0.1
RUN git clone --depth 1 --branch ${GEM5_TAG} \
        https://github.com/gem5/gem5.git /opt/gem5
WORKDIR /opt/gem5
# ~30-60 min depending on host. gem5.opt = optimized build with stats/tracing.
RUN scons build/RISCV/gem5.opt -j"$(nproc)"

# ---- stage 1b: source tree without build artifacts --------------------------
# The image ships the exact gem5 source its binary was built from (reference
# reading + BSD-3 attribution); the ~10 GB build tree and .git are discarded.
FROM build AS src
RUN rm -rf /opt/gem5/build /opt/gem5/.git \
    && echo "${GEM5_TAG:-v25.1.0.1}" > /opt/gem5/GEM5_VERSION

# ---- stage 2: runtime image -------------------------------------------------
FROM ghcr.io/gem5/ubuntu-24.04_all-dependencies:v25-1

RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc-riscv64-linux-gnu \
        libc6-dev-riscv64-cross \
        python3-matplotlib \
        python3-numpy \
    && rm -rf /var/lib/apt/lists/*

# Source tree (build artifacts stripped), then the simulator binary on top.
# Homework content is NEVER baked in: /hw is an empty mount point for the
# course homework git repo (docker run -v <repo>/hwN:/hw).
COPY --from=src /opt/gem5 /opt/gem5
COPY --from=build /opt/gem5/build/RISCV/gem5.opt /opt/gem5/build/RISCV/gem5.opt

ENV PATH="/opt/gem5/build/RISCV:${PATH}"
WORKDIR /hw
CMD ["/bin/bash"]
