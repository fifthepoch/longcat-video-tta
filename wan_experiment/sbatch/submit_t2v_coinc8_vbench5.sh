#!/bin/bash
# Full-clip VBench on the five COMPLETED coinc first-8 arms.
# Does not wait for sf_titans. Does not remake generate.
# Leave 18257633 in the queue — it will fill titans later
# and skip dirs that already have joined.json.
# Do not letter n=2. Do not launch 128.
#
#   cd /scratch/wc3013/longcat-video-tta && git pull --ff-only origin main
#   bash wan_experiment/sbatch/submit_t2v_coinc8_vbench5.sh

set -euo pipefail

SCRATCH_BASE="/scratch/${USER}"
PROJECT_ROOT="${PROJECT_ROOT:-${SCRATCH_BASE}/longcat-video-tta}"
ACCOUNT="${ACCOUNT:-torch_pr_36_mren}"
SB="${PROJECT_ROOT}/wan_experiment/sbatch"
SERIES="${SERIES:-t2v_moviegen_coinc_8v}"
VBENCH_WALL="${VBENCH_WALL:-08:00:00}"

ROOT="${PROJECT_ROOT}/wan_experiment/results/${SERIES}"
VIDEO_DIRS=""
for m in notta sf_window sf_coinc sf_writeevery sf_meandelta; do
    d="${ROOT}/${m}_h30s_shard0"
    if [[ ! -d "${d}" ]]; then
        echo "ERROR: missing ${d}" >&2
        exit 2
    fi
    VIDEO_DIRS="${VIDEO_DIRS} ${d}"
done

VB=$(sbatch --parsable --account="${ACCOUNT}" --time="${VBENCH_WALL}" \
    --export=ALL,SERIES_DIR="${ROOT}",VIDEO_DIRS="${VIDEO_DIRS}",CLIPS=full \
    "${SB}/run_i2v_vbench.sbatch")
echo "VBench full-clip (five finished arms) job ${VB}"
echo "  scancel ${VB}"
echo "Do not wait for titans 18257632. Do not launch 128. Do not letter n=2."
