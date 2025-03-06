#!/bin/bash
# Copyright (C) 2022 Intel Corporation
# SPDX-License-Identifier: GPL-2.0-only

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Get the git commit hash
cd ${DIR}
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
GIT_COMMIT_HASH=$(git rev-parse HEAD)

# Compile the appropriate BPF program
if [ "${TMA}" = true ]; then
  ${DIR}/bpf/tma/build.sh
  ${CLANG} \
    ${PW_CFLAGS} -I${DIR}/bpf/tma -I${PREFIX}/include \
    -DGIT_COMMIT_HASH="\"${GIT_COMMIT_HASH}\"" \
    -c ${DIR}/processwatch.c -o ${DIR}/processwatch.o
else
  ${DIR}/bpf/insn/build.sh
  ${CLANG} \
    ${PW_CFLAGS} -I${DIR}/bpf/insn -I${PREFIX}/include \
    -DGIT_COMMIT_HASH="\"${GIT_COMMIT_HASH}\"" \
    -c ${DIR}/processwatch.c -o ${DIR}/processwatch.o
fi

###################################################################
#                       USERSPACE PROGRAM
###################################################################
echo "Linking the main Process Watch binary..."
${CLANG} ${PW_CFLAGS} ${DIR}/processwatch.o \
  -o ${DIR}/processwatch -lrt -lpthread -lm ${PW_LDFLAGS} -lelf -lz
