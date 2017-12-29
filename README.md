# py_simple_table

Simple ASCII table drawing for Python 3

Creates customizable ASCII (and unicode) tables, 
by default creates reStructuredText grid tables.

Features:
  - unicode support
  - multiline cells
  - default values for missing cells
  - customisable table structure characters
  - customisable cell padding
  - support for common newline styles (LF, CRLF, CR)
  - data can be lists or dicts


## example usage

```python
from draw_table import draw_table

# ### with dictionaries ##################################################
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

print(draw_table(headers,
                 table_data,
                 column_keys=column_keys,
                 default_value='n/A'))

```

will give:

```
+------------+---------------+------------------+
| First name | Last name     | Address          |
+============+===============+==================+
| Rick       | Nash          | IceHockey Road   |
|            |               | 7260 Davos       |
+------------+---------------+------------------+
| Grumpy     | Cat           | Reddit           |
|            |               | The frontpage of |
|            |               | the internet     |
+------------+---------------+------------------+
| Lady       | And the Tramp | n/A              |
+------------+---------------+------------------+
```

```python
from draw_table import draw_table

# ### with lists (and custom characters) #################################
# just choose some fancy characters (or use default ones)
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

print(draw_table(headers,
                 table_data,
                 **table_structure))
```

will give:

```
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

## FaQ

Q: isn't it a bit over-tested?

A: yes, I did it as an exercise
