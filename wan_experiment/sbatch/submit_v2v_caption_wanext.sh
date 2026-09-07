#!/bin/bash
# Caption N=8 Wan official prompt-extend, Self Forcing do-nothing.
# Separate from pwarp. Same leftover videos, new T5 string only.
# Cite vs caption-32 notta (original metadata.csv).
# Do not remake cite-128. No TTC. No I2V. No 8-GPU DMD.
#
#   cd /scratch/wc3013/longcat-video-tta && git pull --ff-only origin main
#   python3 -u wan_experiment/scripts/prepare_wanext_captions.py --n 2   # smoke texts
#   SMOKE=1 bash wan_experiment/sbatch/submit_v2v_caption_wanext.sh
#   python3 -u wan_experiment/scripts/prepare_wanext_captions.py --n 8
#   bash wan_experiment/sbatch/submit_v2v_caption_wanext.sh

set -euo pipefail

SCRATCH_BASE="/scratch/${USER}"
PROJECT_ROOT="${PROJECT_ROOT:-${SCRATCH_BASE}/longcat-video-tta}"
ACCOUNT="${ACCOUNT:-torch_pr_36_mren}"
SB="${PROJECT_ROOT}/wan_experiment/sbatch"
VIDEO_DIR="${VIDEO_DIR:-${PROJECT_ROOT}/datasets/panda_wanext_8}"
SERIES="${SERIES:-v2v_panda_caption_wanext_8v}"
N_VIDEOS="${N_VIDEOS:-8}"
if [[ "${SMOKE:-0}" == "1" ]]; then
    N_VIDEOS=2
    SERIES="${SERIES}_smoke"
    VIDEO_DIR="${PROJECT_ROOT}/datasets/panda_wanext_2"
fi
GEN_WALL="${GEN_WALL:-04:00:00}"
VBENCH_WALL="${VBENCH_WALL:-08:00:00}"
SF_CAP="${SF_CAP:-${PROJECT_ROOT}/wan_experiment/results/v2v_panda_caption_32v/notta_h30s_shard0}"

cd "${PROJECT_ROOT}"
mkdir -p "${PROJECT_ROOT}/wan_experiment/slurm_log"

if [[ ! -d "${VIDEO_DIR}" ]]; then
    echo "ERROR: ${VIDEO_DIR} missing. Run prepare_wanext_captions.py first." >&2
    exit 1
fi
if [[ ! -f "${VIDEO_DIR}/captions.json" && ! -f "${VIDEO_DIR}/metadata.csv" ]]; then
    echo "ERROR: extended captions missing under ${VIDEO_DIR}" >&2
    exit 1
fi
if [[ ! -f /scratch/${USER}/wan-checkpoints/self_forcing_dmd.pt ]]; then
    echo "ERROR: Self Forcing ckpt missing." >&2
    exit 1
fi

echo "---- wanext preflight (must not be stem) ----"
python3 - <<PY
from pathlib import Path
import json, sys
d = Path("${VIDEO_DIR}")
caps = {}
if (d / "captions.json").is_file():
    caps = json.loads((d / "captions.json").read_text())
print("dir", d, "n_caps", len(caps))
for k, v in list(caps.items())[:2]:
    print(k, "len", len(v))
    print(" ", v[:160])
    if v.replace("_", " ").lower().startswith("panda "):
        raise SystemExit("stem prompt")
if len(caps) < ${N_VIDEOS}:
    raise SystemExit("not enough extended captions")
PY

COMMON="HORIZON_S=30,N_VIDEOS=${N_VIDEOS},SEED=0,SEARCH_FROM=0,PREFIX_LATENTS=9,CHUNK_LATENTS=21,SERIES=${SERIES},NUM_SHARDS=1,VIDEO_DIR=${VIDEO_DIR},VIDEO_WORKERS=1"

J=$(sbatch --parsable --account="${ACCOUNT}" --time="${GEN_WALL}" \
    --export=ALL,METHOD=notta,SEARCH_K=1,${COMMON} \
    "${SB}/run_v2v_chunked.sbatch")
echo "V2V ${SERIES} notta (wan-extended captions) n=${N_VIDEOS} job ${J}"

ROOT="${PROJECT_ROOT}/wan_experiment/results/${SERIES}"
VB=$(sbatch --parsable --account="${ACCOUNT}" --time="${VBENCH_WALL}" \
    --dependency="afterok:${J}" \
    --export=ALL,SERIES_DIR="${ROOT}",VIDEO_DIRS="${ROOT}/notta_h30s_shard0 ${SF_CAP}",CLIPS=full \
    "${SB}/run_i2v_vbench.sbatch")
echo "VBench full-clip job ${VB} afterok ${J}"
echo "Cite vs caption Self Forcing first-8 (original metadata.csv)."
echo "Sidecar prompt_source must not be stem."
echo "  scancel ${J} ${VB}"
echo "No pwarp on this wave. No TTC. No I2V."
