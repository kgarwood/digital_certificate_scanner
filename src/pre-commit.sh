#!/bin/bash

result="$(pycodestyle --first .)"
echo "${result}"
# python -m py_compile *.py


# result="$(export PYTHONPATH=. pytest)"
# echo "${result}"
export PYTHONPATH=.
result="$(pytest)"
echo "${result}"
# pytest --cov .
