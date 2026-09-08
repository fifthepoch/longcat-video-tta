#!/bin/bash
# Leftover n=2 pwarp amplify smoke on official Wan teacher.
# A ramp / B persist-ramp / C step 2,4,8 / D early / E mag-gate
# + live twins where the idea is gated. Cite wan_notta.
# Do not launch 128. Do not mix MovieGen. No nwarp.
#
#   cd /scratch/wc3013/longcat-video-tta && git pull --ff-only origin main
#   SMOKE=1 bash wan_experiment/sbatch/submit_wan_teacher_pwarp_amp.sh

set -euo pipefail

SCRATCH_BASE="/scratch/${USER}"
PROJECT_ROOT="${PROJECT_ROOT:-${SCRATCH_BASE}/longcat-video-tta}"
ACCOUNT="${ACCOUNT:-torch_pr_36_mren}"
SB="${PROJECT_ROOT}/wan_experiment/sbatch"
WAN_CODE="${WAN_CODE:-${SCRATCH_BASE}/third_party/Wan2.1}"
WAN_DIR="${WAN_DIR:-${SCRATCH_BASE}/wan-checkpoints/Wan2.1-T2V-1.3B}"

if [[ "${SMOKE:-1}" != "1" ]]; then
    echo "This script is smoke-only. Do not launch 128 from here." >&2
    exit 1
fi

N_VIDEOS="${N_VIDEOS:-2}"
VIDEO_DIR="${VIDEO_DIR:-${PROJECT_ROOT}/datasets/panda_1000_480p}"
SERIES="${SERIES:-wan_teacher_pwarp_amp_smoke}"
NOTTA_TIME="${NOTTA_TIME:-02:00:00}"
WARP_TIME="${WARP_TIME:-03:00:00}"
PERSIST_TIME="${PERSIST_TIME:-04:00:00}"
VBENCH_WALL="${VBENCH_WALL:-08:00:00}"
COMMON="N_VIDEOS=${N_VIDEOS},SEED=0,SEARCH_K=1,GATE_THRESHOLD=2.0,NWARP_GAMMA=0.5,PWARP_STEP=1,LIVE_MIN=0.012,FRAME_NUM=81,SAMPLING_STEPS=50,NUM_SHARDS=1,WAN_CODE=${WAN_CODE},WAN_DIR=${WAN_DIR}"

if [[ ! -d "${WAN_DIR}" ]]; then
    echo "ERROR: Wan teacher missing: ${WAN_DIR}" >&2
    exit 1
fi
if [[ ! -f "${WAN_CODE}/wan/text2video.py" ]]; then
    echo "ERROR: official Wan2.1 missing: ${WAN_CODE}" >&2
    exit 1
fi
if [[ ! -f "${VIDEO_DIR}/metadata.csv" ]]; then
    echo "ERROR: leftover metadata.csv missing: ${VIDEO_DIR}" >&2
    exit 1
fi

mkdir -p "${PROJECT_ROOT}/wan_experiment/slurm_log"

JOBS=()
submit_method() {
    local method="$1"
    local wall="$2"
    local J
    J=$(sbatch --parsable --account="${ACCOUNT}" --time="${wall}" \
        --export=ALL,TASK=leftover,METHOD="${method}",SERIES="${SERIES}",${COMMON},VIDEO_DIR="${VIDEO_DIR}" \
        "${SB}/run_wan_teacher.sbatch")
    echo "AMP leftover ${method} job ${J}"
    JOBS+=("${J}")
}

echo "host=wan_teacher  pwarp amplify leftover n=2  cite wan_notta"
submit_method wan_notta "${NOTTA_TIME}"
submit_method wan_pwarp "${WARP_TIME}"
submit_method wan_pwarp_ramp "${WARP_TIME}"
submit_method wan_pwarp_ramp_live "${WARP_TIME}"
submit_method wan_pwarp_persist "${PERSIST_TIME}"
submit_method wan_pwarp_persist_live "${PERSIST_TIME}"
submit_method wan_pwarp_s2 "${WARP_TIME}"
submit_method wan_pwarp_s4 "${WARP_TIME}"
submit_method wan_pwarp_s8 "${WARP_TIME}"
submit_method wan_pwarp_early "${WARP_TIME}"
submit_method wan_pwarp_early_live "${WARP_TIME}"
submit_method wan_pwarp_mag "${WARP_TIME}"
submit_method wan_pwarp_mag_live "${WARP_TIME}"

ROOT="${PROJECT_ROOT}/wan_experiment/results/${SERIES}"
VIDEO_DIRS=""
for m in wan_notta wan_pwarp wan_pwarp_ramp wan_pwarp_ramp_live \
    wan_pwarp_persist wan_pwarp_persist_live \
    wan_pwarp_s2 wan_pwarp_s4 wan_pwarp_s8 \
    wan_pwarp_early wan_pwarp_early_live \
    wan_pwarp_mag wan_pwarp_mag_live; do
    VIDEO_DIRS="${VIDEO_DIRS} ${ROOT}/${m}_h5s_shard0"
done
DEPS=$(IFS=:; echo "${JOBS[*]}")
VB=$(sbatch --parsable --account="${ACCOUNT}" --time="${VBENCH_WALL}" \
    --dependency="afterok:${DEPS}" \
    --export=ALL,SERIES_DIR="${ROOT}",VIDEO_DIRS="${VIDEO_DIRS}",CLIPS=full \
    "${SB}/run_i2v_vbench.sbatch")
echo "VBench ${SERIES} job ${VB} afterok ${DEPS}"
echo "  scancel ${JOBS[*]} ${VB}"
echo "Cite wan_notta. Sidecar dx0/dx_last/n_shifts. Do not letter n=2. Do not launch 128."
