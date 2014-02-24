# -*- coding: utf-8 -*-

# standard library
from functools import partial

# related
import pytest

# project
from draw_table import Table, SimpleTableError

DUMMY_HEADERS = ['4', '5', '6']

DUMMY_DATA = [{4: 'd',
               5: 'e',
               6: 'f'}]

DUMMY_COLUMN_KEYS = [4, 5, 6]


dummy_table = partial(Table, headers=DUMMY_HEADERS, data=DUMMY_DATA)


def test_error_if_no_data():
    with pytest.raises(SimpleTableError):
        Table(DUMMY_HEADERS, {})


@pytest.mark.parametrize('headers_column_keys', [
    [
        (1, 2, 3), (4, 5, 6), None  # OK
    ],
    [
        (1, 2, 3), (4, 5),    SimpleTableError,  # not same length
    ],
])
def test_headers_column_keys_lenght_mismatch(headers_column_keys):
    headers, column_keys, error = headers_column_keys
    if error is not None:
        with pytest.raises(error) as excinfo:
            Table(headers, DUMMY_DATA, column_keys=column_keys)
    else:
        Table(headers, DUMMY_DATA, column_keys=column_keys)


@pytest.mark.parametrize('arg_name', [
    'row_sep_char',
    'headers_row_sep_char',
    'corner_char',
    'cell_sep_char',
    'cell_fill_char',
])
def test_multi_char_table_param(arg_name):
    kwarg = {arg_name: 'aa'}
    with pytest.raises(SimpleTableError):
        dummy_table(**kwarg)


@pytest.mark.parametrize('data_result', [
    (DUMMY_DATA,                    DUMMY_COLUMN_KEYS,  [['d', 'e', 'f']]),
    (DUMMY_DATA,                    (5, 4, 6),          [['e', 'd', 'f']]),
    ([{'4': 1, '5': 2, '6': 3},
      {'4': 4, '5': 5, '6': 6}],    ('4', '5', '6'),    [[1, 2, 3], [4, 5, 6]]),

])
def test_get_list_of_lists(data_result):
    data, col_keys, expected_result = data_result
    table = Table(DUMMY_HEADERS, data, column_keys=col_keys)
    assert table.data == expected_result, 'data does not match'


@pytest.mark.parametrize('data_result', [
    (DUMMY_DATA,                    DUMMY_COLUMN_KEYS,  [['d', 'e', 'f']]),
    (DUMMY_DATA,                    (5, 4, 1),          [['e', 'd', 'X']]),
    ([{'4': 1, '5': 2, '6': 3},
      {'4': 4, '5': 5, '6': 6}],    ('4', '5', '7'),    [[1, 2, 'X'], [4, 5, 'X']]),
    ([{'4': 1, '6': 3},
      {'4': 4, '5': 5, '6': 6}],    ('4', '5', '6'),    [[1, 'X', 3], [4, 5, 6]]),
])
def test_get_list_of_lists_default_value(data_result):
    data, col_keys, expected_result = data_result
    table = Table(DUMMY_HEADERS, data, column_keys=col_keys, default_value='X')
    assert table.data == expected_result, 'data does not match'


@pytest.mark.parametrize('data', [
    [['a', 'b', 'c']],
    [['a', 'b', 'cc'],
     ['a', 'b', 'c']],
    [['a', 'b', 'c'],
     ['a', 'b', 'cc'],
     ['a', 'b', '']],
    [['a', 'b', 'c'],
     ['a', 'b', 'cc'],
     ['', '', 'zzzzzz']],
    [['a', 'b', 'c'],
     ['a', 'b', 'cc'],
     ['', '', '']],
])
@pytest.mark.parametrize('headers', [
    ('4',   '5',    '6'),
    ('44',  '5',    '6'),
    ('',    '5',    '6'),
    ('',    '',     '')
])
@pytest.mark.parametrize('h_padding', [
    0, 1, 2
])
# TODO test with newline parameter
def test_column_widths_list_data(data, headers, h_padding):
    table = Table(headers, data, min_h_padding=h_padding)
    col_widths = [0] * len(headers)
    for row_list in data:
        for n, value in enumerate(row_list):
            col_widths[n] = max(col_widths[n],
                                len(value) + h_padding*2,
                                len(headers[n]) + h_padding*2)

    assert table._get_column_widths() == col_widths, 'Column widths do not match'


class TestFillHCellPadding:
    """Testing full_h_cell_padding() function"""

    DEF_CF_CHAR = ' '
    DEF_MIN_H_PADDING = 1
    DEF_CELL_WIDTH = 15

    @pytest.mark.parametrize('line_width_padding_error', [
        ('the line',    10,     0,      None),
        ('the line',    10,     1,      None),
        ('the line',    10,     2,      AssertionError),
        ('the line',    9,      0,      None),
        ('the line',    9,      1,      AssertionError),
        ('the line',    0,      0,      AssertionError),
        ('the line',    0,      1,      AssertionError),
        ('the line',    -1,     0,      AssertionError),  # -1 should never happen
        ('the line',    -1,     1,      AssertionError),
        ('',            2,      0,      None),
        ('',            2,      1,      None),
        ('',            2,      2,      AssertionError),
        ('',            1,      0,      None),
        ('',            0,      0,      None),
        ('',            -1,     0,      AssertionError),

    ])
    def test_cell_width_too_small(self, line_width_padding_error):
        """cell_width must be >= len(cell_line) + 2"""
        cell_line, cell_width, min_h_padding, error = line_width_padding_error
        table = dummy_table(min_h_padding=min_h_padding,
                            cell_fill_char=self.DEF_CF_CHAR)
        if error is not None:
            with pytest.raises(error):
                table._fill_h_cell_padding(cell_line, cell_width)
        else:
            table._fill_h_cell_padding(cell_line, cell_width)

    @pytest.mark.parametrize('line_width_expected', [
        ('the line',     10,     ' the line '),
        ('the line',     15,     ' the line      '),
        (' the line',    11,     '  the line '),
        (' the line',    15,     '  the line     '),
        ('the line ',    11,     ' the line  '),
        ('the line ',    15,      ' the line      '),
        ('',             2,      '  '),
        (' ',            3,      '   '),
    ])
    def test_cell_line_cell_width(self, line_width_expected):
        cell_line, cell_width, expected = line_width_expected
        table = dummy_table(min_h_padding=self.DEF_MIN_H_PADDING,
                            cell_fill_char=self.DEF_CF_CHAR)
        res = table._fill_h_cell_padding(cell_line, cell_width)
        assert res == expected, 'H-filled cell line does not match'

    @pytest.mark.parametrize('line_characer_expected', [
        ('the line',        ' ',    ' the line      '),
        ('the line',        '-',    '-the line------'),
        (' the line',       '-',    '- the line-----'),
        ('the line ',       '-',    '-the line -----'),
        ('  the line  ',    '-',    '-  the line  --'),
        (' ',               '-',    '- -------------'),
        ('',                '-',    '---------------')
    ])
    def test_fill_character(self, line_characer_expected):
        line, character, expected = line_characer_expected
        table = dummy_table(min_h_padding=self.DEF_MIN_H_PADDING,
                            cell_fill_char=character)
        res = table._fill_h_cell_padding(line, self.DEF_CELL_WIDTH)
        assert res == expected, 'Cell line filled with character does not match'

    @pytest.mark.parametrize('line_padding_expected', [
        ('the line',        1,      ' the line      '),
        ('the line',        2,      '  the line     '),
        ('the line',        0,      'the line       '),
        ('my fancy line',   1,      ' my fancy line '),
        ('',                0,      '               '),
        ('',                1,      '               '),
        (' ',               7,      '               '),
    ])
    def test_line_padding(self, line_padding_expected):
        cell_line, min_h_padding, expected = line_padding_expected
        table = dummy_table(min_h_padding=min_h_padding)
        res = table._fill_h_cell_padding(cell_line, self.DEF_CELL_WIDTH)
        assert res == expected, 'Padded line does not match'

    @pytest.mark.parametrize('line_width_char_padding_expected', [
        ('the line',    10,     ' ',    0,  'the line  '),
        ('the line',    10,     ' ',    1,  ' the line '),
        ('the line',    12,     ' ',    2,  '  the line  '),
        ('',            10,     ' ',    1,  '          '),
        ('',            10,     '?',    1,  '??????????'),
        (' ',           10,     '*',    1,  '* ********'),
        ('',            0,      '*',    0,  ''),
        (' theline ',   10,     '/',    0,  ' theline /'),
        (' theline',    10,     '/',    1,  '/ theline/'),
    ])
    def test_all(self, line_width_char_padding_expected):
        """This test is not exhaustive"""
        cell_line, cell_width, fill_char, min_h_padding, expected = line_width_char_padding_expected
        table = dummy_table(min_h_padding=min_h_padding,
                            cell_fill_char=fill_char)
        res = table._fill_h_cell_padding(cell_line, cell_width)
        assert res == expected, 'Padded cell line does not match'


@pytest.mark.parametrize('column_widths_sep_char_expected', [
    ([0],       None,   '++'),
    ([0, 0],    None,   '+++'),
    ([1],       None,   '+-+'),
    ([1, 0],    None,   '+-++'),
    ([1, 0, 1], None,   '+-++-+'),
    ([0],       '*',    '++'),
    ([0, 0],    '*',    '+++'),
    ([1],       '*',    '+*+'),
    ([1, 0],    '*',    '+*++'),
    ([1, 0, 1], '*',    '+*++*+'),
])
@pytest.mark.parametrize('corner_char', ['+'])
def test_build_row_sep(column_widths_sep_char_expected, corner_char):
    column_widths, sep_char, expected = column_widths_sep_char_expected
    table = dummy_table(corner_char=corner_char)
    table.column_widths = column_widths
    sep_row = table._build_row_sep(row_sep_char=sep_char)
    assert sep_row == expected, 'Separator row does not match'


@pytest.mark.parametrize('newline', [
    '\n',
    '\r',
    '\r\n'
])
@pytest.mark.parametrize('cell_value', [
    '',
    ' ',
    '\n',
    '\r',
    '\r\n',
    'the_value',
    'the\nvalue',
    'the\rvalue',
    'the\r\nvalue',
    0,
])
def test_split_cell_value(cell_value, newline):
    table = dummy_table(newline=newline)
    lines = table._split_cell_value(cell_value)
    expected = str(cell_value).split(newline)
    assert lines == expected, 'Split cell value does not match'


def test_build_row_empty_row():
    table = dummy_table()
    with pytest.raises(AssertionError):
        table._build_row([])


@pytest.mark.parametrize('row_column_widths_expexted', [
    (['a'],             [3],        '| a |'),
    (['a', 'b'],        [3, 4],     '| a | b  |'),
    (['  a  ', 'b'],    [10, 10],   '|   a      | b        |'),
    (['||||||||', ''],  [10, 10],   '| |||||||| |          |'),

])
@pytest.mark.parametrize('min_h_padding', [1])
@pytest.mark.parametrize('cell_sep_char', '|')
def test_build_row(row_column_widths_expexted, min_h_padding, cell_sep_char):
    row, column_widths, expected = row_column_widths_expexted
    table = dummy_table(min_h_padding=min_h_padding,
                        cell_sep_char=cell_sep_char)
    table.column_widths = column_widths
    row_str = table._build_row(row)
    assert row_str == expected, 'Table row does not match'


def test_draw_example1():
    # we test the example code
    headers = ["First name", "Last name", "Address"]
    column_keys = ['first_name', 'last_name', 'address']
    table_data = [
        {'first_name':  "Rick",
         'last_name':   "Nash",
         'address':     "IceHockey Road\n7260 Davos"},
        {'first_name':  "Grumpy",
         'last_name':   "Cat",
         'address':     "Reddit\nThe frontpage of\nthe internet"},
        {'first_name':  "Lady",
         'last_name':   "And the Tramp",
         # No address!
         },
    ]
    table_str = Table(headers, table_data, column_keys=column_keys).draw()
    expected_str = ('+------------+---------------+------------------+\n'
                    '| First name | Last name     | Address          |\n'
                    '+============+===============+==================+\n'
                    '| Rick       | Nash          | IceHockey Road   |\n'
                    '|            |               | 7260 Davos       |\n'
                    '+------------+---------------+------------------+\n'
                    '| Grumpy     | Cat           | Reddit           |\n'
                    '|            |               | The frontpage of |\n'
                    '|            |               | the internet     |\n'
                    '+------------+---------------+------------------+\n'
                    '| Lady       | And the Tramp | -                |\n'
                    '+------------+---------------+------------------+')

    assert table_str == expected_str, 'draw output does not match'


def test_draw_example1_crlf():
    # we test the example code
    headers = ["First name", "Last name", "Address"]
    column_keys = ['first_name', 'last_name', 'address']
    table_data = [
        {'first_name':  "Rick",
         'last_name':   "Nash",
         'address':     "IceHockey Road\n7260 Davos"},
        {'first_name':  "Grumpy",
         'last_name':   "Cat",
         'address':     "Reddit\r\nThe frontpage of\r\nthe internet"},
        {'first_name':  "Lady",
         'last_name':   "And the Tramp",
         # No address!
         },
    ]
    table_str = Table(headers, table_data, column_keys=column_keys, newline='\r\n').draw()
    expected_str = ('+------------+---------------+---------------------------+\r\n'
                    '| First name | Last name     | Address                   |\r\n'
                    '+============+===============+===========================+\r\n'
                    '| Rick       | Nash          | IceHockey Road\n7260 Davos |\r\n'
                    '+------------+---------------+---------------------------+\r\n'
                    '| Grumpy     | Cat           | Reddit                    |\r\n'
                    '|            |               | The frontpage of          |\r\n'
                    '|            |               | the internet              |\r\n'
                    '+------------+---------------+---------------------------+\r\n'
                    '| Lady       | And the Tramp | -                         |\r\n'
                    '+------------+---------------+---------------------------+')

    assert table_str == expected_str, 'draw output does not match'


def test_draw_example2():
    table_structure = {
        'row_sep_char':         "'",
        'headers_row_sep_char': '`',
        'corner_char':          '°',
        'cell_sep_char':        ':',
        'cell_fill_char':       ' ',
        'min_h_padding':        3,
    }

    headers = ["First name", "Last name", "Address"]
    table_data = [
        ["Rick", "Nash", "IceHockey Road\n7260 Davos"],
        ["Grumpy", "Cat", "Reddit\nThe frontpage of\nthe internet"]
    ]

    table_str = Table(headers, table_data, **table_structure).draw()
    expected_str = ("°''''''''''''''''°'''''''''''''''°''''''''''''''''''''''°\n"
                    ":   First name   :   Last name   :   Address            :\n"
                    "°````````````````°```````````````°``````````````````````°\n"
                    ":   Rick         :   Nash        :   IceHockey Road     :\n"
                    ":                :               :   7260 Davos         :\n"
                    "°''''''''''''''''°'''''''''''''''°''''''''''''''''''''''°\n"
                    ":   Grumpy       :   Cat         :   Reddit             :\n"
                    ":                :               :   The frontpage of   :\n"
                    ":                :               :   the internet       :\n"
                    "°''''''''''''''''°'''''''''''''''°''''''''''''''''''''''°")

    assert table_str == expected_str, 'draw output does not match'


def test_draw_example2_cr():
    table_structure = {
        'row_sep_char':         "'",
        'headers_row_sep_char': '`',
        'corner_char':          '°',
        'cell_sep_char':        ':',
        'cell_fill_char':       ' ',
        'min_h_padding':        3,
        'newline':              '\r'
    }

    headers = ["First name", "Last name", "Address"]
    table_data = [
        ["Rick", "Nash", "IceHockey Road\r7260 Davos"],
        ["Grumpy", "Cat", "Reddit\nThe frontpage of\rthe internet"]
    ]

    table_str = Table(headers, table_data, **table_structure).draw()
    expected_str = ("°''''''''''''''''°'''''''''''''''°'''''''''''''''''''''''''''''°\r"
                    ":   First name   :   Last name   :   Address                   :\r"
                    "°````````````````°```````````````°`````````````````````````````°\r"
                    ":   Rick         :   Nash        :   IceHockey Road            :\r"
                    ":                :               :   7260 Davos                :\r"
                    "°''''''''''''''''°'''''''''''''''°'''''''''''''''''''''''''''''°\r"
                    ":   Grumpy       :   Cat         :   Reddit\nThe frontpage of   :\r"
                    ":                :               :   the internet              :\r"
                    "°''''''''''''''''°'''''''''''''''°'''''''''''''''''''''''''''''°")

    assert table_str == expected_str, 'draw output does not match'
