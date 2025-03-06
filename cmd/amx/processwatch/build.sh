#!/bin/bash
# Copyright (C) 2022 Intel Corporation
# SPDX-License-Identifier: GPL-2.0-only

###################################################################
#                           BUILD.SH
# This is the main build script for Process Watch. It first uses
# `build_deps.sh` to build the dependencies in the `deps` directory,
# then builds the BPF and userspace programs.
###################################################################
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ARCH=$(uname -m)
export ARCH

# USER-CHANGEABLE OPTIONS
export CLANG="${CLANG:-clang}"
export CLANGXX="${CLANGXX:-clang++}"
export LLVM_STRIP="${LLVM_STRIP:-llvm-strip}"
export LLVM_CONFIG="${LLVM_CONFIG:-llvm-config}"
export PW_CC="${CLANG}"
export PW_CXX="${CLANGXX}"
export BPFTOOL="${BPFTOOL:-bpftool}"
export CMAKE="${CMAKE:-cmake}"

if ! command -v ${CMAKE} &> /dev/null; then
  export CMAKE="cmake3"
  if ! command -v ${CMAKE} &> /dev/null; then
    echo "Could not find CMake. I tried 'cmake' and 'cmake3'."
    exit 1
  fi
fi

die () {
    echo "ERROR: $*. Aborting." >&2
    exit 1
}

# Command-line arguments
export DEBUG=false
export LEGACY=false
export BUILD_DEPS=true
usage() { echo "Usage: $0 [-l] [-t] [-b] [-d]" 1>&2; exit 1; }
while getopts ":ltbd" arg; do
  case $arg in
    l) [ "$ARCH" == "aarch64" ] && die "Legacy unsupported on Arm"
      LEGACY=true
      ;;
    b)
      BUILD_DEPS=false
      ;;
    d)
      DEBUG=true
      ;;
  esac
done

# These are used to compile the dependencies
DEPS_DIR="${DIR}/deps"

# We export these because they're used by src/build.sh
export PREFIX="${DEPS_DIR}/install"

export PW_LDFLAGS="-Wl,-z,now"
export PW_CFLAGS="-O2 -Wall -D_FORTIFY_SOURCE=2"
export CFLAGS="-O2 -Wall"
export BPF_CFLAGS="-O2 -Wall -g"

if [ "${DEBUG}" = true ]; then
  export PW_CFLAGS="${PW_CFLAGS} -g -fsanitize=address -static-libsan"
  export PW_LDFLAGS="${PW_LDFLAGS} -g -fsanitize=address -static-libsan"
  export CFLAGS="${CFLAGS} -g"
fi

if [ "${LEGACY}" = true ]; then
  export BPF_CFLAGS="${BPF_CFLAGS} -DINSNPROF_LEGACY_PERF_BUFFER"
  export PW_CFLAGS="${PW_CFLAGS} -DINSNPROF_LEGACY_PERF_BUFFER"
fi

if [ "${ARCH}" == "x86_64" ]; then
    export BPF_CFLAGS="${BPF_CFLAGS} -D__TARGET_ARCH_x86"
    export PW_CFLAGS="${PW_CFLAGS}"
else
    export BPF_CFLAGS="${BPF_CFLAGS} -D__TARGET_ARCH_arm"
    export PW_CFLAGS="${PW_CFLAGS}"
fi

# Prepare the dependency-building logs
if [ "${BUILD_DEPS}" = true ]; then
  BUILD_LOGS=${DEPS_DIR}/build_logs
  rm -rf ${BUILD_LOGS} || true
  mkdir -p ${BUILD_LOGS} || true
fi

cd ${DIR}
git submodule update --init --recursive

###################################################################
#                            deps
###################################################################
if [ "${BUILD_DEPS}" = true ]; then
  echo "Compiling dependencies..."
  source ${DIR}/deps/build_deps.sh
fi

export PATH="${PREFIX}/bin:${PATH}"

# libbpf
export PW_LDFLAGS="${PW_LDFLAGS} ${PREFIX}/lib/libbpf.a"

if [ "${ARCH}" == "x86_64" ]; then
  # Disassembler, Zydis
  if [ -f "${PREFIX}/lib/libZydis.a" ]; then
    export ZYDIS_STATIC_LIB="${PREFIX}/lib/libZydis.a"
  else
    export ZYDIS_STATIC_LIB="${PREFIX}/lib64/libZydis.a"
  fi
  export PW_LDFLAGS="${PW_LDFLAGS} ${ZYDIS_STATIC_LIB}"
else
  # Disassembler, Capstone
  export PW_LDFLAGS="${PW_LDFLAGS} ${PREFIX}/lib/libcapstone.a"
fi

###################################################################
#                     Process Watch itself
###################################################################
export CC="${PW_CC}"
export CXX="${PW_CXX}"
${DIR}/src/build.sh
cp ${DIR}/src/processwatch ${DIR}
