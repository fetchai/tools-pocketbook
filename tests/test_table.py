import unittest
from io import StringIO
from unittest.mock import patch

from pocketbook.table import Table


class TableTests(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_empty(self, mock_print):
        table = Table(['foo'])
        table.display()

        self.assertEqual(mock_print.getvalue(), '\x1b[38;5;255mFoo \x1b[0m\n')

    @patch('sys.stdout', new_callable=StringIO)
    def test_columns(self, mock_print):
        table = Table(['foo', 'bar'])
        table.add_row(foo=1, bar=2)
        table.display()

        self.assertEqual(mock_print.getvalue(),
                         '\x1b[38;5;255mFoo Bar \x1b[0m\n\x1b[38;5;253m\x1b[48;5;238m1   2   \x1b[0m\n')

    @patch('sys.stdout', new_callable=StringIO)
    def test_multiple_rows(self, mock_print):
        table = Table(['foo'])
        table.add_row(foo=1)
        table.add_row(foo=2)
        table.add_row(foo=3)
        table.display()

        self.assertEqual(mock_print.getvalue(),
                         '\x1b[38;5;255mFoo \x1b[0m\n\x1b[38;5;253m\x1b[48;5;238m1   \x1b[0m\n\x1b[38;5;251m\x1b[48;5;235m2   \x1b[0m\n\x1b[38;5;253m\x1b[48;5;238m3   \x1b[0m\n')

    def test_invalid_padding_case(self):
        truncated = Table._pad_value('LongWords', 5)
        self.assertEqual(truncated, 'LongW')
