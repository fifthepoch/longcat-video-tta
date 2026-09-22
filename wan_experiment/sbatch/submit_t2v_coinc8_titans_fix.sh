#!/bin/bash
# Resubmit ONLY sf_titans after the residual-eta broadcast fix,
# then VBench on all six first-8 dirs. Do not remake the five
# COMPLETED generate arms. Do not letter n=2. Do not launch 128.
#
#   cd /scratch/wc3013/longcat-video-tta && git pull --ff-only origin main
#   bash wan_experiment/sbatch/submit_t2v_coinc8_titans_fix.sh

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

mkdir -p "${PROJECT_ROOT}/wan_experiment/slurm_log"

if [[ ! -f "${PROMPT_FILE}" ]]; then
    echo "Resolving MovieGen prompts -> ${PROMPT_FILE} (first ${N_VIDEOS})"
    "${PYTHON}" "${PROJECT_ROOT}/wan_experiment/scripts/prepare_t2v_prompts.py" \
        --sf-root "${SF_ROOT}" \
        --vendor "${PROJECT_ROOT}/datasets/moviegen_128.txt" \
        --n "${N_VIDEOS}" \
        --out "${PROMPT_FILE}"
fi

J=$(sbatch --parsable --account="${ACCOUNT}" --time="${WALL}" \
    --export=ALL,METHOD=sf_titans,SEARCH_K=1,SHARD_ID=0,${COMMON} \
    "${SB}/run_t2v_chunked.sbatch")
echo "T2V ${SERIES} sf_titans rerun job ${J}"

ROOT="${PROJECT_ROOT}/wan_experiment/results/${SERIES}"
VIDEO_DIRS=""
for m in notta sf_window sf_coinc sf_writeevery sf_titans sf_meandelta; do
    VIDEO_DIRS="${VIDEO_DIRS} ${ROOT}/${m}_h30s_shard0"
done
VB=$(sbatch --parsable --account="${ACCOUNT}" --time="${VBENCH_WALL}" \
    --dependency="afterok:${J}" \
    --export=ALL,SERIES_DIR="${ROOT}",VIDEO_DIRS="${VIDEO_DIRS}",CLIPS=full \
    "${SB}/run_i2v_vbench.sbatch")
echo "VBench full-clip job ${VB} afterok ${J}"
echo "Do not remake notta / window / coinc / writeevery / meandelta."
echo "  scancel ${J} ${VB}"
echo "Do not launch 128. Do not letter n=2. No TTC. No I2V."
