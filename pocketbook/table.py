from colored import fg, bg, attr


class Table:
    def __init__(self, columns):
        self._rows = []
        self._columns = columns

    def add_row(self, **kwargs):
        self._rows.append(dict(**kwargs))

    def display(self, column_padding=1):

        # Step 1. Determine the column lengths
        column_lengths = [0] * len(self._columns)
        for i, column in enumerate(self._columns):

            # header
            column_lengths[i] = len(column)

            # row contents
            for row in self._rows:
                column_lengths[i] = max(column_lengths[i], len(str(row.get(column, ''))))

            # allow a nice
            column_lengths[i] += column_padding

        # Step 2a. Print the header
        self._start_header()
        for i, column in enumerate(self._columns):
            self._write_header(column, column_lengths[i])
        self._end_header()

        # Step 2b. Print the table contents
        for i, row in enumerate(self._rows):
            self._start_row(i)
            for j, column in enumerate(self._columns):
                self._write_row_value(row.get(column, ''), i, column_lengths[j])
            self._end_row(i)

    @classmethod
    def _start_header(cls):
        print(fg(255), end='')

    @classmethod
    def _write_header(cls, value, length):
        value = cls._pad_value(value, length)

        # capitalise
        value = value[0].upper() + value[1:]
        print(value, end='')

    @classmethod
    def _end_header(cls):
        print(attr(0))

    @classmethod
    def _start_row(cls, row):
        if row & 1:
            foreground = fg(251)
            background = bg(235)
        else:
            foreground = fg(253)
            background = bg(238)

        print(foreground + background, end='')

    @classmethod
    def _write_row_value(cls, value, row, length):
        value = cls._pad_value(value, length)

        print(value, end='')

    @classmethod
    def _end_row(cls, row):
        print(attr(0))

    @classmethod
    def _pad_value(cls, value, length):
        value = str(value)
        in_value = str(value)
        value_len = len(value)

        if value_len > length:
            value = value[:length]
        else:
            padding_len = length - value_len
            value += ' ' * padding_len

        return value
