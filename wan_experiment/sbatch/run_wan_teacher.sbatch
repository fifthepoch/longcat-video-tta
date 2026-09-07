#!/bin/bash
#SBATCH --job-name=wan_teacher
#SBATCH --account=torch_pr_36_mren
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=256G
#SBATCH --gres=gpu:h200:1
#SBATCH --time=04:00:00
#SBATCH --output=/scratch/%u/longcat-video-tta/wan_experiment/slurm_log/wan_teacher_%j.out
#SBATCH --error=/scratch/%u/longcat-video-tta/wan_experiment/slurm_log/wan_teacher_%j.err
#SBATCH --comment="preemption=yes;requeue=true"

# Official Wan2.1-T2V-1.3B teacher. NO self_forcing_dmd.pt.
#   METHOD=wan_notta|wan_always|wan_gated|wan_nwarp|wan_nwarp_live|
#          wan_pwarp|wan_pwarp_live
#   TASK=leftover|moviegen

set -euo pipefail
export PYTHONNOUSERSITE=1

SCRATCH_BASE="/scratch/${USER}"
PROJECT_ROOT="${SCRATCH_BASE}/longcat-video-tta"
CONDA_ENV="${CONDA_ENV:-${SCRATCH_BASE}/conda-envs/self_forcing}"
WAN_CODE="${WAN_CODE:-${SCRATCH_BASE}/third_party/Wan2.1}"
WAN_DIR="${WAN_DIR:-${SCRATCH_BASE}/wan-checkpoints/Wan2.1-T2V-1.3B}"

TASK="${TASK:-moviegen}"
METHOD="${METHOD:-wan_notta}"
N_VIDEOS="${N_VIDEOS:-2}"
SEED="${SEED:-0}"
SEARCH_K="${SEARCH_K:-4}"
GATE_THRESHOLD="${GATE_THRESHOLD:-2.0}"
NWARP_GAMMA="${NWARP_GAMMA:-0.5}"
PWARP_STEP="${PWARP_STEP:-1}"
LIVE_MIN="${LIVE_MIN:-0.012}"
FRAME_NUM="${FRAME_NUM:-81}"
SAMPLING_STEPS="${SAMPLING_STEPS:-50}"
SERIES="${SERIES:-wan_teacher_smoke}"
SHARD_ID="${SHARD_ID:-0}"
NUM_SHARDS="${NUM_SHARDS:-1}"
VIDEO_DIR="${VIDEO_DIR:-${PROJECT_ROOT}/datasets/panda_1000_480p}"
PROMPT_FILE="${PROMPT_FILE:-${PROJECT_ROOT}/datasets/moviegen_128_resolved.txt}"
OUT_DIR="${OUT_DIR:-${PROJECT_ROOT}/wan_experiment/results/${SERIES}/${METHOD}_h5s_shard${SHARD_ID}}"

if [[ -f "${SCRATCH_BASE}/wan-checkpoints/self_forcing_dmd.pt" ]]; then
    echo "NOTE: Self Forcing ckpt exists on disk but this job will not load it."
fi
if [[ ! -d "${WAN_DIR}" ]]; then
    echo "ERROR: Wan teacher missing: ${WAN_DIR}" >&2
    exit 1
fi
if [[ ! -d "${WAN_CODE}" ]]; then
    echo "ERROR: Wan code missing: ${WAN_CODE}" >&2
    echo "Clone https://github.com/Wan-Video/Wan2.1 to ${WAN_CODE}" >&2
    exit 1
fi

export PYTHONHASHSEED="${SEED}"
export CUBLAS_WORKSPACE_CONFIG=":4096:8"
export TMPDIR="${SCRATCH_BASE}/tmp"
export HF_HOME="${SCRATCH_BASE}/.cache/huggingface"
export TRANSFORMERS_CACHE="${HF_HOME}"
export TORCH_HOME="${SCRATCH_BASE}/.cache/torch"
mkdir -p "$TMPDIR" "$HF_HOME" "$TORCH_HOME" "$OUT_DIR" \
    "${PROJECT_ROOT}/wan_experiment/slurm_log"

echo "=============================================================================="
echo "Wan TEACHER ${METHOD} task=${TASK}"
echo "  job     : ${SLURM_JOB_ID:-local}  node=$(hostname)  $(date)"
echo "  host    : wan_teacher  NO self_forcing_dmd.pt"
echo "  n=${N_VIDEOS} seed=${SEED} k=${SEARCH_K} frames=${FRAME_NUM} steps=${SAMPLING_STEPS}"
echo "  series  : ${SERIES}  shard=${SHARD_ID}/${NUM_SHARDS}"
echo "  out     : ${OUT_DIR}"
echo "=============================================================================="

module purge
module load anaconda3/2025.06
source /share/apps/anaconda3/2025.06/etc/profile.d/conda.sh
conda activate "${CONDA_ENV}"
unset PYTHONHOME
unset PYTHONPATH
export PATH="${CONDA_ENV}/bin:${PATH}"
export LD_LIBRARY_PATH="${CONDA_ENV}/lib:${LD_LIBRARY_PATH:-}"
PYTHON="${CONDA_ENV}/bin/python"

"${PYTHON}" -c "import torch; print('torch', torch.__version__, 'cuda', torch.cuda.is_available())" || {
    echo "ERROR: env cannot import torch" >&2
    exit 1
}

cd "${PROJECT_ROOT}"
EXTRA=()
if [[ "${TASK}" == "leftover" ]]; then
    EXTRA+=(--video-dir "${VIDEO_DIR}")
else
    EXTRA+=(--prompt-file "${PROMPT_FILE}")
fi

"${PYTHON}" wan_experiment/scripts/run_wan_teacher.py \
    --task "${TASK}" \
    --method "${METHOD}" \
    --wan-code "${WAN_CODE}" \
    --wan-dir "${WAN_DIR}" \
    --out-dir "${OUT_DIR}" \
    --n "${N_VIDEOS}" \
    --seed "${SEED}" \
    --search-k "${SEARCH_K}" \
    --gate-threshold "${GATE_THRESHOLD}" \
    --nwarp-gamma "${NWARP_GAMMA}" \
    --pwarp-step "${PWARP_STEP}" \
    --live-min "${LIVE_MIN}" \
    --frame-num "${FRAME_NUM}" \
    --sampling-steps "${SAMPLING_STEPS}" \
    --shard-id "${SHARD_ID}" \
    --num-shards "${NUM_SHARDS}" \
    "${EXTRA[@]}"

echo "=============================================================================="
echo "Wrote ${OUT_DIR}/summary.json  $(date)"
echo "=============================================================================="
