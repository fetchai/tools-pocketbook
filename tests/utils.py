import os
import shutil
import tempfile

SAMPLE_ADDRESS = '2w9uqXLFvCve9TjfoRb2nuztuTx54E1S3AjuB9hWCMMGX5kp4W'
SUPER_SECURE_PASSWORD = 'Fetch!Ai-ToTh3M00n!'


class TemporaryPocketBookRoot:
    def __init__(self):
        self._root = None

    @property
    def root(self):
        return self._root

    def __enter__(self):
        self._root = tempfile.mkdtemp(prefix='pocketbook_', suffix='_root')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if os.path.isdir(self._root):
            shutil.rmtree(self._root)
