"""Download multi-file ONNX models to real local files for ONNX Runtime."""
from pathlib import Path

FP32_REPO = "istupakov/gigaam-multilingual-large-ctc-onnx"
FP32_FILES = (
    "config.json",
    "multilingual_vocab.txt",
    "multilingual_large_ctc.onnx",
    "multilingual_large_ctc.onnx.data",
)

def prepare_fp32_model_dir(model_dir: Path) -> Path:
    """Ensure the FP32 model and its external weights share one real directory."""
    missing = [name for name in FP32_FILES if not (model_dir / name).is_file()]
    if missing:
        from huggingface_hub import snapshot_download
        snapshot_download(
            repo_id=FP32_REPO,
            local_dir=str(model_dir),
            allow_patterns=list(FP32_FILES),
        )
        missing = [name for name in FP32_FILES if not (model_dir / name).is_file()]
        if missing:
            raise RuntimeError(f"Incomplete FP32 model download: {', '.join(missing)}")
    return model_dir
