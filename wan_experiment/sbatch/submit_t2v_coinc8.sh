#!/bin/bash
# MovieGen T2V 30 s first-8: coincidence-gated fast weights.
#   notta         — full KV replay, no W_fast
#   sf_window     — last 21 latents; sink_size=0; no W_fast
#   sf_coinc      — window + coincidence write (the method)
#   sf_writeevery — window + every-token DeltaNet (Irie control)
#   sf_titans     — window + residual-sized write (integrator control)
#   sf_meandelta  — window + mean ||Δ|| gate (energy, not coincidence)
# First-8 is the first table. Do not letter n=2. Do not launch 128.
# No I2V. No TTC. No 8-GPU DMD. Cite the SF host.
#
#   cd /scratch/wc3013/longcat-video-tta && git pull --ff-only origin main
#   bash wan_experiment/sbatch/submit_t2v_coinc8.sh

set -euo pipefail

SCRATCH_BASE="/scratch/${USER}"
PROJECT_ROOT="${PROJECT_ROOT:-${SCRATCH_BASE}/longcat-video-tta}"
ACCOUNT="${ACCOUNT:-torch_pr_36_mren}"
SB="${PROJECT_ROOT}/wan_experiment/sbatch"
SF_ROOT="${SF_ROOT:-${SCRATCH_BASE}/third_party/Self-Forcing}"
PYTHON="${PYTHON:-${SCRATCH_BASE}/conda-envs/self_forcing/bin/python}"

SERIES="${SERIES:-t2v_moviegen_coinc_8v}"
N_VIDEOS="${N_VIDEOS:-8}"
NUM_SHARDS="${NUM_SHARDS:-1}"
WALL="${WALL:-05:00:00}"
VBENCH_WALL="${VBENCH_WALL:-08:00:00}"
PROMPT_FILE="${PROMPT_FILE:-${PROJECT_ROOT}/datasets/moviegen_128_resolved.txt}"
PPROT="WINDOW_LATENTS=21,PPROT_TAU_CENTER=2.0,PPROT_TAU_LO=0.4,PPROT_TAU_HI=2.5,PPROT_MAX_SLOTS=3"
COINC="COINC_WINDOW=3,COINC_BETA=0.15,COINC_ETA_MAX=0.3"
COMMON="HORIZON_S=30,N_VIDEOS=${N_VIDEOS},SEED=0,SEARCH_FROM=1,CHUNK_LATENTS=21,SERIES=${SERIES},NUM_SHARDS=${NUM_SHARDS},PROMPT_FILE=${PROMPT_FILE},${PPROT},${COINC}"

mkdir -p "${PROJECT_ROOT}/wan_experiment/slurm_log" \
    "${PROJECT_ROOT}/datasets"

echo "Resolving MovieGen prompts -> ${PROMPT_FILE} (first ${N_VIDEOS})"
"${PYTHON}" "${PROJECT_ROOT}/wan_experiment/scripts/prepare_t2v_prompts.py" \
    --sf-root "${SF_ROOT}" \
    --vendor "${PROJECT_ROOT}/datasets/moviegen_128.txt" \
    --n "${N_VIDEOS}" \
    --out "${PROMPT_FILE}"

JOBS=()
METHODS_RUN=()
submit_method() {
    local method="$1"
    local J
    J=$(sbatch --parsable --account="${ACCOUNT}" --time="${WALL}" \
        --export=ALL,METHOD="${method}",SEARCH_K=1,SHARD_ID=0,${COMMON} \
        "${SB}/run_t2v_chunked.sbatch")
    echo "T2V ${SERIES} ${method} job ${J}"
    JOBS+=("${J}")
    METHODS_RUN+=("${method}")
}

submit_method notta
submit_method sf_window
submit_method sf_coinc
submit_method sf_writeevery
submit_method sf_titans
submit_method sf_meandelta

ROOT="${PROJECT_ROOT}/wan_experiment/results/${SERIES}"
VIDEO_DIRS=""
for m in notta sf_window sf_coinc sf_writeevery sf_titans sf_meandelta; do
    VIDEO_DIRS="${VIDEO_DIRS} ${ROOT}/${m}_h30s_shard0"
done
DEPS=$(IFS=:; echo "${JOBS[*]}")
VB=$(sbatch --parsable --account="${ACCOUNT}" --time="${VBENCH_WALL}" \
    --dependency="afterok:${DEPS}" \
    --export=ALL,SERIES_DIR="${ROOT}",VIDEO_DIRS="${VIDEO_DIRS}",CLIPS=full \
    "${SB}/run_i2v_vbench.sbatch")
echo "VBench full-clip job ${VB} afterok ${DEPS}"
JOBS+=("${VB}")

echo "Submitted ${#JOBS[@]} jobs. 2-way H200 cap: extras queue."
echo "First-8 MovieGen 30 s. sink_size=0 on window/fw. Coincidence write on last 8 blocks."
echo "Sidecar must print coinc C/theta/wrote and prefix_kept=false from chunk 2."
echo "  scancel ${JOBS[*]}"
echo "Do not launch 128. Do not letter n=2. No TTC. No I2V."
