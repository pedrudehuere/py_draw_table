py_simple_table
===============

Simple ASCII table in Python


example usage:

  import py_simple_table as table

  headers = ["First name", "Last name", "Address"]
  columns = ['first_name', 'last_name', 'address']
  data = [
      {'first_name': "Rick", 'last_name': "Nash", 'address': "IceHockey Road\n7260 Davos"},
      {'first_name': "Grumpy", 'last_name': "Cat", 'address': "Reddit\nThe frontpage of\nthe internet"},
  ]

  table_str = table.draw_table(headers, columns, data)
  print(table_str)

will give:

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
