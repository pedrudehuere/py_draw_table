"""
This guy draws tables like this one
+-------------------+-------------------+-----------------------------+
|    Field name     | Required-default  | Description                 |
+===================+===================+=============================+
|    user_name      |    no - 'miao'    | some other description      |
+-------------------+-------------------+-----------------------------+
|    password       |    yes            | some other description      |
|                   |                   | and multiline fields!       |
|                   |                   | (but not multiline headers! |
+-------------------+-------------------+-----------------------------+

TODO
support multiple lines
"""

row_sep_char = "-"
corner_char = "+"
cell_fill_char = " "
cell_sep_char = "|"
DEFAULT_FIELD = "N/a"


def convert_newline(text):
    """Replaces non-unix newlines (\r, \n\r) with \n
    :param text: the string to be converted
    :return: the 'fixed' string
    """
    return text.replace('\r\n', '\n').replace('\r', '\n')


def build_row_sep(columns_min_widht, char=None):
    """Builds a row separator
    :returns: string
    """
    the_char = char or row_sep_char
    return "+{}+\n".format(corner_char.join([the_char * min_col_length for min_col_length in columns_min_widht]))


def fill_h_cell_padding(value, width):
    """Returns the value with horizontal cell padding filled
    e.g.
    value = "miao", width = 10
    returns " miao     "    # assuming cell_fill_char is a whitespace
    :param value: The value of cell
    :param width: The total length of the cell (in characters)
    :returns: string
    """
    value = str(value)
    assert len(value) <= width - 2
    return " {}{}".format(value, cell_fill_char * (width-len(value)-1))


def build_row(columns, column_widths, row_dict):
    """Builds a table row in sphinx source code,
    supports multi-line fields
    """
    # getting a list of lines (for each cell) with newline converted to '\n'
    row = [convert_newline(value).split('\n') for value in [row_dict.get(column, DEFAULT_FIELD) for column in columns]]

    # getting row height first (counting newlines)
    row_height = 1
    for value in row:
        row_height = max(row_height, len(value))

    # building each text line for all values
    lines = []
    for line_index in range(row_height):
        line = []
        for column_index, column in enumerate(columns):
            try:
                value = row[column_index][line_index]
            except IndexError:
                value = ""  # adding vertical padding line
            line.append(fill_h_cell_padding(value, column_widths[column_index]))

        lines.append("{}{}{}".format(cell_sep_char,             # first |
                                     cell_sep_char.join(line),  # values separated by |
                                     cell_sep_char              # last |
                                     ))
    # joining all lines in row
    return '\n'.join(lines)


def draw_table(headers, columns, data):
    """Draws a table in restructured text (ResT)
    :param headers: a list containing the headers of the table
    :param columns: the keys of each row in data
    :param data: a dicitonary containing the keys in columns
    :returns: a string containing the table (ready to be printed/written)
    """
    if len(headers) != len(columns):
        raise ValueError("headers and columns must have same size!")
    # getting minimum width (in characters)
    columns_min_width = [0] * len(columns)
    # minimum width of data
    for row in data:    # each row in table
        for col_index, col_name in enumerate(columns):  # each field in row
            for line in row.get(col_name, DEFAULT_FIELD).split('\n'):    # for line in field
                columns_min_width[col_index] = max(columns_min_width[col_index], len(str(line))+2)


    # and minimum width of headers, milti-line headers not supported!
    for col_index, value in enumerate(headers):
        columns_min_width[col_index] = max(columns_min_width[col_index], len(value)+2)

    return "{}{}\n{}{}{}".format(build_row_sep(columns_min_width),                # upper border
                                 build_row(columns, columns_min_width, dict(zip(columns, headers))),  # headers
                                 build_row_sep(columns_min_width, char="="),      # header underline - row separation
                                 build_row_sep(columns_min_width).join(["{}\n".format(build_row(columns, columns_min_width, row)) for row in data]), # rows
                                 build_row_sep(columns_min_width))                # lower border


#### test zone ########################################################################################################
if __name__ == '__main__':

  headers = ["First name", "Last name", "Address"]
  columns = ['first_name', 'last_name', 'address']
  data = [
    {'first_name': "Rick", 'last_name': "Nash", 'address': "IceHockey Road\n7260 Davos"},
    {'first_name': "Grumpy", 'last_name': "Cat", 'address': "Reddit\nThe frontpage of\nthe internet"},
  ]

  table_str = draw_table(headers, columns, data)
  print(table_str)
