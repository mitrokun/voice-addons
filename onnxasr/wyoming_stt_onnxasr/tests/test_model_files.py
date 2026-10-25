"""Unit tests for the FP32 model file preparation helper."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sys
from types import SimpleNamespace

from wyoming_onnxasr.model_files import FP32_FILES, FP32_REPO, prepare_fp32_model_dir


class PrepareFp32ModelDirTests(unittest.TestCase):
    def test_skips_download_when_complete(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in FP32_FILES:
                (root / name).touch()
            with patch.dict(sys.modules, {"huggingface_hub": SimpleNamespace(snapshot_download=lambda **kw: self.fail("unexpected download"))}):
                self.assertEqual(prepare_fp32_model_dir(root), root)

    def test_retries_missing_files_in_partial_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "config.json").touch()
            def download(**kwargs):
                self.assertEqual(kwargs["repo_id"], FP32_REPO)
                self.assertEqual(kwargs["local_dir"], str(root))
                for name in FP32_FILES:
                    (root / name).touch()
            with patch.dict(sys.modules, {"huggingface_hub": SimpleNamespace(snapshot_download=download)}):
                self.assertEqual(prepare_fp32_model_dir(root), root)

    def test_rejects_incomplete_download(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            with patch.dict(sys.modules, {"huggingface_hub": SimpleNamespace(snapshot_download=lambda **kw: None)}):
                with self.assertRaisesRegex(RuntimeError, "Incomplete FP32 model download"):
                    prepare_fp32_model_dir(root)


if __name__ == "__main__":
    unittest.main()
