#!/usr/bin/env bash
set -x
SRC_CORE=app

autopep8 -i -r $SRC_CORE
pylint $SRC_CORE
flake8 --max-complexity 10 $SRC_CORE