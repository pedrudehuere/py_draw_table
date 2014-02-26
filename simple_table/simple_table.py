"""
This guy draws tables like this one:
+-------------------+-------------------+-----------------------------+
|    Field name     | Required-default  | Description                 |
+===================+===================+=============================+
|    user_name      |    no - 'miao'    | some other description      |
+-------------------+-------------------+-----------------------------+
|    password       |    yes            | some other description      |
|                   |                   | and multiline fields!       |
|                   |                   | (but not multiline headers! |
+-------------------+-------------------+-----------------------------+
"""

# default values are for reStructuredText grid tables (e.g. for sphinx)
HEADERS_ROW_SEP_CHAR = "="
ROW_SEP_CHAR = "-"
CORNER_CHAR = "+"
CELL_FILL_CHAR = " "
CELL_SEP_CHAR = "|"
MIN_H_PADDING = 1   # the minimum horizontal padding on each side of a cell value
DEFAULT_FIELD = "N/a"


def convert_newline(text):
    """Replaces non-unix newlines (\r, \n\r) with \n
    :param text: the string to be converted
    :return: the 'fixed' string
    """
    return text.replace('\r\n', '\n').replace('\r', '\n')


def build_row_sep(column_widths, row_sep_char, corner_char):
    """Builds a row separator
    :param column_widths: a list of integers representing the width of each column (in characters)
    :param row_sep_char: the character that separates rows
    :param corner_char: the corner (intersection of line-separators and row-separators) character
    :returns: a row separator string
    """
    return "{}{}{}\n".format(corner_char,
                             corner_char.join([row_sep_char * min_col_length for min_col_length in column_widths]),
                             corner_char)


def fill_h_cell_padding(cell_value, cell_width, cell_fill_char, min_horizontal_padding):
    """Returns the value with horizontal cell padding filled
    e.g.
    value = "miao", width = 10
    returns " miao     "    # assuming cell_fill_char is a whitespace
    :param cell_value: The value of cell
    :param cell_width: The total length of the cell (in characters)
    :returns: string
    """
    cell_value = str(cell_value)
    assert len(cell_value) <= cell_width - 2
    return "{}{}{}".format(cell_fill_char*min_horizontal_padding,   # left padding
                           cell_value,                              # value
                           cell_fill_char * (cell_width - len(cell_value) - min_horizontal_padding))    # right padding


def build_row(column_widths, row, cell_sep_char, cell_fill_char, min_horizontal_padding):
    """
    Builds a table row string
    :param column_widths: a list of integers representing the width of each column (in characters)
    :param row: a list containing the fields of the table row
    :param cell_sep_char: the cell separator character
    :param cell_fill_char: the cell filling character (used to fill cells - usually with whitespaces)
    :returns: a table row string
    """
    # first we split cell-values in a list of lines in order to support multi-line cell-values
    row = [convert_newline(value).split('\n') for value in row]

    # getting row height first (counting newlines in each cell value)
    row_height = 1
    for value in row:
        row_height = max(row_height, len(value))    # len(value) is the number of lines in the cell-value

    # building each text line for all values
    lines = []  # contains lines (to print) of table row
    for line_index in range(row_height):    # for each line
        line = []
        for column_index, _ in enumerate(_column_keys):
            try:
                value = row[column_index][line_index]
            except IndexError:
                value = ""  # if no value for this line we just add an empty line
            line.append(fill_h_cell_padding(value, column_widths[column_index], cell_fill_char, min_horizontal_padding))    # cell padding

        lines.append("{}{}{}".format(cell_sep_char,             # first |
                                     cell_sep_char.join(line),  # values separated by |
                                     cell_sep_char              # last |
                                     ))
    # joining all lines in row
    return '\n'.join(lines)


def get_column_widths(table_data, headers, min_horizontal_padding):
    """
    Returns a list of column widths (in characters)
    :param table_data: the cell values, either a list of dicts or a list of lists (depends on column_keys)
    :param headers: a list containing the header for each column
    :param min_horizontal_padding: the minimum horizontal padding on each side of cell value
    :return: a list of integers representing the width of each row (in characters)
    """
    # is there any data?
    if len(table_data) == 0:
        # if column_keys is not None:
        #     return [0] * len(column_keys)
        # else:
        raise ValueError("No data received")

    # getting width for table data
    column_widths = [0] * len(table_data[0])  # all zeroes
    for row in table_data:
        for column_index, cell_value in enumerate(row):
            for line in cell_value.split('\n'):
                column_widths[column_index] = max(column_widths[column_index],
                                                  len(str(line)) + min_horizontal_padding*2)

    # updating with width of headers, multi-line headers not supported!
    for col_index, header in enumerate(headers):
        column_widths[col_index] = max(column_widths[col_index], len(header) + min_horizontal_padding*2)

    return column_widths


def draw_table(headers, table_data, row_sep_char=None, headers_row_sep_char=None, corner_char=None,
               cell_sep_char=None, cell_fill_char=None, min_horizontal_padding=None, column_keys=None):
    """
    Builds a string containing a printable table
    :param headers: A list of table headers
    :param table_data: A list of lists or list of dicts (see column keys)
    :param row_sep_char: The character that separates rows
    :param headers_row_sep_char: The character that separates headers row with the next row
    :param corner_char: The corner (where row_sep_char and cell_sep_char intersect) character
    :param cell_sep_char: The character which separates cell
    :param cell_fill_char: The character used for cell padding (usually a white space)
    :param min_horizontal_padding: The minimum horizontal padding on each side of the cell value
    :param column_keys: The keys of the table_data row dictionaries
                        (if not given table data is supposed to be a list of lists)
    :return: a string containing a printable table
    """
    # if we got a list of dictionaries: make list of lists
    if column_keys is not None:
        if len(headers) != len(_column_keys):
            raise ValueError("headers and columns must have same length!")
        table_data = [[row_dict[column_key] for column_key in column_keys] for row_dict in table_data]

    # getting table parameters
    row_sep_char = row_sep_char or ROW_SEP_CHAR
    headers_row_sep_char = headers_row_sep_char or HEADERS_ROW_SEP_CHAR
    corner_char = corner_char or CORNER_CHAR
    cell_sep_char = cell_sep_char or CELL_SEP_CHAR
    cell_fill_char = cell_fill_char or CELL_FILL_CHAR
    min_horizontal_padding = min_horizontal_padding or MIN_H_PADDING

    if any([len(char) > 1 for char in (row_sep_char, headers_row_sep_char, corner_char,
                                       cell_sep_char, cell_fill_char)]):
        raise ValueError("Multi-char table parameters are not supported!")


    # getting column widths
    column_widths = get_column_widths(table_data, headers, min_horizontal_padding)

    # building the table string
    return "{}{}\n{}{}{}".format(build_row_sep(column_widths, row_sep_char, corner_char),
                                 build_row(column_widths, headers, cell_sep_char, cell_fill_char, min_horizontal_padding),
                                 build_row_sep(column_widths, headers_row_sep_char, corner_char),
                                 build_row_sep(column_widths, row_sep_char, corner_char).join(["{}\n".format(
                                 build_row(column_widths, row, cell_sep_char, cell_fill_char, min_horizontal_padding)) for row in table_data]),
                                 build_row_sep(column_widths, row_sep_char, corner_char))

#### test zone ########################################################################################################
if __name__ == '__main__':

    #### with dictionaries ###################################################
    _headers = ["First name", "Last name", "Address"]
    _column_keys = ['first_name', 'last_name', 'address']
    _table_data = [
        {'first_name': "Rick", 'last_name': "Nash", 'address': "IceHockey Road\n7260 Davos"},
        {'first_name': "Grumpy", 'last_name': "Cat", 'address': "Reddit\nThe frontpage of\nthe internet"},
    ]

    table_str_dict = draw_table(_headers,
                                _table_data,
                                column_keys=_column_keys)
    print(table_str_dict)

    #### with lists (and custom characters) ##################################
    # just choose some fancy characters (or use default ones)
    _row_sep_char = "'"
    _headers_row_sep_char = "`"
    _corner_char = "°"
    _cell_sep_char = ":"
    _cell_fill_char = " "
    _min_h_padding = 3


    _headers = ["First name", "Last name", "Address"]
    _table_data = [
        ["Rick", "Nash", "IceHockey Road\n7260 Davos"],
        ["Grumpy","Cat", "Reddit\nThe frontpage of\nthe internet"],
    ]

    table_str_lists = draw_table(_headers,
                                 _table_data,
                                 _row_sep_char,
                                 _headers_row_sep_char,
                                 _corner_char,
                                 _cell_sep_char,
                                 _cell_fill_char,
                                 _min_h_padding)
    print(table_str_lists)