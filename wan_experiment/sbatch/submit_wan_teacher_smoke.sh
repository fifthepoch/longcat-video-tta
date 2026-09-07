#!/bin/bash
# Wan-teacher smoke: leftover Panda n=2 AND MovieGen n=2.
#   wan_notta | wan_always k=4 | wan_gated | wan_nwarp | wan_nwarp_live |
#   wan_pwarp | wan_pwarp_live
# Official Wan2.1-T2V-1.3B. NO self_forcing_dmd.pt. Native 81 frames.
# Cite wan_notta. Do not launch 128. Do not mix leftover with MovieGen dirs.
#
#   cd /scratch/wc3013/longcat-video-tta && git pull --ff-only origin main
#   SMOKE=1 bash wan_experiment/sbatch/submit_wan_teacher_smoke.sh

set -euo pipefail

SCRATCH_BASE="/scratch/${USER}"
PROJECT_ROOT="${PROJECT_ROOT:-${SCRATCH_BASE}/longcat-video-tta}"
ACCOUNT="${ACCOUNT:-torch_pr_36_mren}"
SB="${PROJECT_ROOT}/wan_experiment/sbatch"
PYTHON="${PYTHON:-${SCRATCH_BASE}/conda-envs/self_forcing/bin/python}"
WAN_CODE="${WAN_CODE:-${SCRATCH_BASE}/third_party/Wan2.1}"
WAN_DIR="${WAN_DIR:-${SCRATCH_BASE}/wan-checkpoints/Wan2.1-T2V-1.3B}"

if [[ "${SMOKE:-1}" != "1" ]]; then
    echo "This script is smoke-only. Do not launch 128 from here." >&2
    exit 1
fi

N_VIDEOS="${N_VIDEOS:-2}"
VIDEO_DIR="${VIDEO_DIR:-${PROJECT_ROOT}/datasets/panda_1000_480p}"
PROMPT_FILE="${PROMPT_FILE:-${PROJECT_ROOT}/datasets/moviegen_128_resolved.txt}"
NOTTA_TIME="${NOTTA_TIME:-02:00:00}"
SEARCH_TIME="${SEARCH_TIME:-04:00:00}"
WARP_TIME="${WARP_TIME:-03:00:00}"
VBENCH_WALL="${VBENCH_WALL:-08:00:00}"
COMMON="N_VIDEOS=${N_VIDEOS},SEED=0,SEARCH_K=4,GATE_THRESHOLD=2.0,NWARP_GAMMA=0.5,PWARP_STEP=1,LIVE_MIN=0.012,FRAME_NUM=81,SAMPLING_STEPS=50,NUM_SHARDS=1,WAN_CODE=${WAN_CODE},WAN_DIR=${WAN_DIR}"

if [[ ! -d "${WAN_DIR}" ]]; then
    echo "ERROR: Wan teacher missing: ${WAN_DIR}" >&2
    exit 1
fi
if [[ ! -d "${WAN_CODE}" ]]; then
    echo "ERROR: Wan code missing: ${WAN_CODE}" >&2
    echo "Clone https://github.com/Wan-Video/Wan2.1 into that path, then resubmit." >&2
    exit 1
fi
if [[ ! -f "${VIDEO_DIR}/metadata.csv" ]]; then
    echo "ERROR: leftover metadata.csv missing: ${VIDEO_DIR}" >&2
    exit 1
fi

mkdir -p "${PROJECT_ROOT}/wan_experiment/slurm_log" "${PROJECT_ROOT}/datasets"

if [[ ! -f "${PROMPT_FILE}" ]]; then
    echo "Resolving MovieGen prompts -> ${PROMPT_FILE}"
    SF_ROOT="${SF_ROOT:-${SCRATCH_BASE}/third_party/Self-Forcing}"
    "${PYTHON}" "${PROJECT_ROOT}/wan_experiment/scripts/prepare_t2v_prompts.py" \
        --sf-root "${SF_ROOT}" \
        --vendor "${PROJECT_ROOT}/datasets/moviegen_128.txt" \
        --n "${N_VIDEOS}" \
        --out "${PROMPT_FILE}"
fi

submit_wave() {
    local TASK="$1"
    local SERIES="$2"
    local EXTRA="$3"
    local JOBS=()
    submit_method() {
        local method="$1"
        local k="$2"
        local wall="$3"
        local J
        J=$(sbatch --parsable --account="${ACCOUNT}" --time="${wall}" \
            --export=ALL,TASK="${TASK}",METHOD="${method}",SEARCH_K="${k}",SERIES="${SERIES}",${COMMON},${EXTRA} \
            "${SB}/run_wan_teacher.sbatch")
        echo "TEACHER ${SERIES} ${TASK} ${method} k=${k} job ${J}"
        JOBS+=("${J}")
    }
    submit_method wan_notta 1 "${NOTTA_TIME}"
    submit_method wan_always 4 "${SEARCH_TIME}"
    submit_method wan_gated 4 "${SEARCH_TIME}"
    submit_method wan_nwarp 1 "${WARP_TIME}"
    submit_method wan_nwarp_live 1 "${WARP_TIME}"
    submit_method wan_pwarp 1 "${WARP_TIME}"
    submit_method wan_pwarp_live 1 "${WARP_TIME}"

    local ROOT="${PROJECT_ROOT}/wan_experiment/results/${SERIES}"
    local VIDEO_DIRS=""
    local m
    for m in wan_notta wan_always wan_gated wan_nwarp wan_nwarp_live wan_pwarp wan_pwarp_live; do
        VIDEO_DIRS="${VIDEO_DIRS} ${ROOT}/${m}_h5s_shard0"
    done
    local DEPS
    DEPS=$(IFS=:; echo "${JOBS[*]}")
    local VB
    VB=$(sbatch --parsable --account="${ACCOUNT}" --time="${VBENCH_WALL}" \
        --dependency="afterok:${DEPS}" \
        --export=ALL,SERIES_DIR="${ROOT}",VIDEO_DIRS="${VIDEO_DIRS}",CLIPS=full \
        "${SB}/run_i2v_vbench.sbatch")
    echo "VBench ${SERIES} job ${VB} afterok ${DEPS}"
    echo "  scancel ${JOBS[*]} ${VB}"
}

echo "host=wan_teacher  NO self_forcing_dmd.pt  native 81 frames"
submit_wave leftover wan_teacher_leftover_smoke "VIDEO_DIR=${VIDEO_DIR}"
submit_wave moviegen wan_teacher_moviegen_smoke "PROMPT_FILE=${PROMPT_FILE}"
echo "Submitted leftover + MovieGen smokes. 2-way H200 cap: extras queue."
echo "Cite wan_notta. Sidecar host=wan_teacher source=leftover|t2v_firstseg."
echo "Do not letter n=2. Do not launch 128."
