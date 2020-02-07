import shutil
import unittest
from io import StringIO
from unittest.mock import patch

from pocketbook.disclaimer import display_disclaimer, DISCLAIMER
from .utils import TemporaryPocketBookRoot


class DisclaimerTests(unittest.TestCase):

    def test_display_of_disclaimer(self):
        with TemporaryPocketBookRoot() as ctx:
            shutil.rmtree(ctx.root)  # remove the root - emulate initial startup

            with patch('builtins.input', return_value='\n'):
                with patch('sys.stdout', new_callable=StringIO) as mocked_print:
                    display_disclaimer(ctx.root)
                    self.assertIn(DISCLAIMER, mocked_print.getvalue())

    def test_no_display_of_disclaimer(self):
        with TemporaryPocketBookRoot() as ctx:
            with patch('builtins.input', return_value='\n'):
                with patch('sys.stdout', new_callable=StringIO) as mocked_print:
                    display_disclaimer(ctx.root)
                    self.assertEqual('', mocked_print.getvalue())
