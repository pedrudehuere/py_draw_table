# -*- coding: utf-8 -*-

# standard library
import os.path
import sys

# related
import pytest


if __name__ == '__main__':
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'draw_table'))

    # ['-k', 'func_name']  to run only a particular test
    # ['-s']  do not capture stdout/stderr
    pytest_params = []
    tests = ['table_test.py']
    tests = [os.path.join(os.path.dirname(__file__), test) for test in tests]
    cl_params = sys.argv[1:]

    pytest.main(pytest_params + cl_params + tests)
