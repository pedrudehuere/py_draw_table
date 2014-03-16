py_simple_table
===============

Simple ASCII table in Python
(tested on Python3.3 only)

Creates customizable ASCII tables, by default creates reStructuredText grid tables.

Customizable values are:
 * table structure characters 
 * horizontal cell padding


example usage
-------------

```python
#### with dictionaries ###################################################

# with deafult table format values: creates a reStructuredText grid table

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
```

will give:

```
  +------------+-----------+------------------+
  | First name | Last name | Address          |
  +============+===========+==================+
  | Rick       | Nash      | IceHockey Road   |
  |            |           | 7260 Davos       |
  +------------+-----------+------------------+
  | Grumpy     | Cat       | Reddit           |
  |            |           | The frontpage of |
  |            |           | the internet     |
  +------------+-----------+------------------+

  °''''''''''''''''°'''''''''''''''°''''''''''''''''''''''°
  :   First name   :   Last name   :   Address            :
  °````````````````°```````````````°``````````````````````°
  :   Rick         :   Nash        :   IceHockey Road     :
  :                :               :   7260 Davos         :
  °''''''''''''''''°'''''''''''''''°''''''''''''''''''''''°
  :   Grumpy       :   Cat         :   Reddit             :
  :                :               :   The frontpage of   :
  :                :               :   the internet       :
  °''''''''''''''''°'''''''''''''''°''''''''''''''''''''''°
```

