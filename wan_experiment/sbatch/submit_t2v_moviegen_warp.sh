#!/bin/bash
# Track C smoke: MovieGen T2V 30 s, field baselines + first-chunk nwarp/pwarp.
#   notta | always-BoN k=4 | gated-BoN | sf_nwarp | sf_nwarp_live |
#   sf_pwarp | sf_pwarp_live
# Chunk 0 is ordinary Self Forcing. Flow is measured on that chunk,
# then extras (nwarp) or pred-slide (pwarp) start at chunk 1.
# Do not mix leftover Panda. No TTC. No I2V. No 8-GPU DMD.
# Smoke first. Do not launch full 128 on the first paste.
#
#   cd /scratch/wc3013/longcat-video-tta && git pull --ff-only origin main
#   SMOKE=1 bash wan_experiment/sbatch/submit_t2v_moviegen_warp.sh

set -euo pipefail

SCRATCH_BASE="/scratch/${USER}"
PROJECT_ROOT="${PROJECT_ROOT:-${SCRATCH_BASE}/longcat-video-tta}"
ACCOUNT="${ACCOUNT:-torch_pr_36_mren}"
SB="${PROJECT_ROOT}/wan_experiment/sbatch"
SF_ROOT="${SF_ROOT:-${SCRATCH_BASE}/third_party/Self-Forcing}"
PYTHON="${PYTHON:-${SCRATCH_BASE}/conda-envs/self_forcing/bin/python}"

SMOKE="${SMOKE:-0}"
if [[ "${SMOKE}" == "1" ]]; then
    SERIES="${SERIES:-t2v_moviegen_warp_smoke}"
    N_VIDEOS="${N_VIDEOS:-2}"
    NUM_SHARDS="${NUM_SHARDS:-1}"
    NOTTA_TIME="${NOTTA_TIME:-02:00:00}"
    SEARCH_TIME="${SEARCH_TIME:-02:00:00}"
    WARP_TIME="${WARP_TIME:-02:00:00}"
else
    SERIES="${SERIES:-t2v_moviegen_warp_128v}"
    N_VIDEOS="${N_VIDEOS:-128}"
    NUM_SHARDS="${NUM_SHARDS:-4}"
    NOTTA_TIME="${NOTTA_TIME:-04:00:00}"
    SEARCH_TIME="${SEARCH_TIME:-08:00:00}"
    WARP_TIME="${WARP_TIME:-04:00:00}"
fi

PROMPT_FILE="${PROMPT_FILE:-${PROJECT_ROOT}/datasets/moviegen_128_resolved.txt}"
GATE="GATE_THRESHOLD=2.0,GATE_CH1_THRESHOLD=0.8,GATE_DELTA=0.5,GATE_DELTA_PREV_MIN=0.5"
WARP="NWARP_GAMMA=0.5,PWARP_STEP=1,LIVE_MIN=0.012"
COMMON="HORIZON_S=30,N_VIDEOS=${N_VIDEOS},SEED=0,SEARCH_FROM=1,CHUNK_LATENTS=21,SERIES=${SERIES},NUM_SHARDS=${NUM_SHARDS},PROMPT_FILE=${PROMPT_FILE},${GATE},${WARP}"
VBENCH_WALL="${VBENCH_WALL:-08:00:00}"

mkdir -p "${PROJECT_ROOT}/wan_experiment/slurm_log" \
    "${PROJECT_ROOT}/datasets"

echo "Resolving MovieGen prompts -> ${PROMPT_FILE}"
"${PYTHON}" "${PROJECT_ROOT}/wan_experiment/scripts/prepare_t2v_prompts.py" \
    --sf-root "${SF_ROOT}" \
    --vendor "${PROJECT_ROOT}/datasets/moviegen_128.txt" \
    --n "${N_VIDEOS}" \
    --out "${PROMPT_FILE}"

JOBS=()
METHODS_RUN=()
submit_method() {
    local method="$1"
    local k="$2"
    local wall="$3"
    local shard="$4"
    local J
    J=$(sbatch --parsable --account="${ACCOUNT}" --time="${wall}" \
        --export=ALL,METHOD="${method}",SEARCH_K="${k}",SHARD_ID="${shard}",${COMMON} \
        "${SB}/run_t2v_chunked.sbatch")
    echo "T2V ${SERIES} ${method} k=${k} shard ${shard} job ${J}"
    JOBS+=("${J}")
    METHODS_RUN+=("${method}")
}

for SHARD_ID in $(seq 0 $((NUM_SHARDS - 1))); do
    submit_method notta 1 "${NOTTA_TIME}" "${SHARD_ID}"
    submit_method always_bon 4 "${SEARCH_TIME}" "${SHARD_ID}"
    submit_method gated_bon 4 "${SEARCH_TIME}" "${SHARD_ID}"
    submit_method sf_nwarp 1 "${WARP_TIME}" "${SHARD_ID}"
    submit_method sf_nwarp_live 1 "${WARP_TIME}" "${SHARD_ID}"
    submit_method sf_pwarp 1 "${WARP_TIME}" "${SHARD_ID}"
    submit_method sf_pwarp_live 1 "${WARP_TIME}" "${SHARD_ID}"
done

ROOT="${PROJECT_ROOT}/wan_experiment/results/${SERIES}"
VIDEO_DIRS=""
for SHARD_ID in $(seq 0 $((NUM_SHARDS - 1))); do
    for m in notta always_bon gated_bon sf_nwarp sf_nwarp_live sf_pwarp sf_pwarp_live; do
        VIDEO_DIRS="${VIDEO_DIRS} ${ROOT}/${m}_h30s_shard${SHARD_ID}"
    done
done
DEPS=$(IFS=:; echo "${JOBS[*]}")
VB=$(sbatch --parsable --account="${ACCOUNT}" --time="${VBENCH_WALL}" \
    --dependency="afterok:${DEPS}" \
    --export=ALL,SERIES_DIR="${ROOT}",VIDEO_DIRS="${VIDEO_DIRS}",CLIPS=full \
    "${SB}/run_i2v_vbench.sbatch")
echo "VBench full-clip job ${VB} afterok ${DEPS}"
JOBS+=("${VB}")

echo "Submitted ${#JOBS[@]} jobs. 2-way H200 cap: extras queue."
echo "Chunk 0 is shared do-nothing. Warp starts at chunk 1."
echo "Sidecar must print nwarp/pwarp source=t2v_chunk0. Prompt is MovieGen."
echo "  scancel ${JOBS[*]}"
echo "No leftover Panda. No TTC. No I2V. Smoke first; do not scale 128 tonight."
