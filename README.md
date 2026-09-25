# CS 423 — Computer Architecture — Homework Assignments (Fall 2026)

Bilkent University · Instructor: A. Giray Yağlıkçı

This repository contains the homework handouts and starter code. All
assignments run on the gem5 simulator inside the pinned course Docker image.

## Environment setup (once)

```sh
docker pull s4lbot/cs423-gem5:v25.1.0.1
```

The image contains everything you need — gem5 v25.1.0.1 (prebuilt RISC-V
binary + its exact source tree under /opt/gem5), the riscv64 cross toolchain,
and plotting libraries. **No homework content is inside the image**: you mount
this repository into the container, so `git pull` always gets you the latest
assignment files without re-downloading the image.

If you cannot pull the image, `docker/build.sh` rebuilds it from source
(30–60 min, one time).

## Working on a homework

```sh
git pull                      # get the latest assignment state
cd hw1
docker run --rm -u "$(id -u):$(id -g)" -v "$PWD":/hw -w /hw \
    s4lbot/cs423-gem5:v25.1.0.1 bash scripts/smoke_test.sh
```

Each `hwN/` directory contains `handout.pdf` (read this first) and the
starter files it describes. Results you generate stay on your machine, in
your working copy.

## Policies

See each handout: GenAI policy, late policy (10%/week), individual work —
no partners. Submission is via Moodle.

## Questions

Each homework has a discussion category on the course website's GitHub
Discussions, e.g. HW1: https://github.com/SAL-Research/comparch-fall-2026/discussions/categories/hw1
