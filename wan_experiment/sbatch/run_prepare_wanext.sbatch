#!/bin/bash
#SBATCH --job-name=wan_wanext_prep
#SBATCH --account=torch_pr_36_mren
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --gres=gpu:h200:1
#SBATCH --time=01:00:00
#SBATCH --output=/scratch/%u/longcat-video-tta/wan_experiment/slurm_log/wan_wanext_prep_%j.out
#SBATCH --error=/scratch/%u/longcat-video-tta/wan_experiment/slurm_log/wan_wanext_prep_%j.err
#SBATCH --comment="preemption=yes;requeue=true;gpu_mps=yes"

# Qwen2.5-7B Wan official prompt-extend. Writes datasets/panda_wanext_${N}.
# Login base python3 has no torch. Do not invent captions if this fails.

set -euo pipefail
export PYTHONNOUSERSITE=1

SCRATCH_BASE="/scratch/${USER}"
PROJECT_ROOT="${PROJECT_ROOT:-${SCRATCH_BASE}/longcat-video-tta}"
CONDA_ENV="${CONDA_ENV:-${SCRATCH_BASE}/conda-envs/self_forcing}"
N_VIDEOS="${N_VIDEOS:-8}"
DEST="${DEST:-${PROJECT_ROOT}/datasets/panda_wanext_${N_VIDEOS}}"

export TMPDIR="${SCRATCH_BASE}/tmp"
export HF_HOME="${SCRATCH_BASE}/.cache/huggingface"
export TRANSFORMERS_CACHE="${HF_HOME}"
export TORCH_HOME="${SCRATCH_BASE}/.cache/torch"
mkdir -p "$TMPDIR" "$HF_HOME" "$TORCH_HOME" \
    "${PROJECT_ROOT}/wan_experiment/slurm_log"

echo "=============================================================================="
echo "Wan prompt-extend prepare n=${N_VIDEOS}"
echo "  job  : ${SLURM_JOB_ID:-local}  node=$(hostname)  $(date)"
echo "  dest : ${DEST}"
echo "=============================================================================="
nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv,noheader || true

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
    echo "ERROR: self_forcing env cannot import torch" >&2
    exit 1
}

"${PYTHON}" -u "${PROJECT_ROOT}/wan_experiment/scripts/prepare_wanext_captions.py" \
    --n "${N_VIDEOS}" --dest "${DEST}"
echo "prepare done $(date)"
