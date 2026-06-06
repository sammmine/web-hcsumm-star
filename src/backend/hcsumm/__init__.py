"""HCSumm* pipeline package.

Pure, importable pipeline lifted from
``research/notebooks/hcsumm_star_NPD_final.ipynb``. No Jupyter/display side effects.

Entry point: :func:`hcsumm.pipeline.run_full_pipeline`.
"""

from .config import PipelineConfig, EmbeddingMode, BehaviourFeature

__all__ = ["PipelineConfig", "EmbeddingMode", "BehaviourFeature"]
