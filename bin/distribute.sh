#!/bin/bash

set -e

PY_ENV=".pypi_env"

# Remove old builds
rm -rf build dist

# Create wheel package
python3 setup.py sdist bdist_wheel
whl_file=$(ls dist/*.whl)

# Create virtualenv for twine
if [[ ! -d "$PY_ENV" ]]; then
  echo "Creating Python virtual environment for PyPI..."
  python3 -m venv $PY_ENV
  source $PY_ENV/bin/activate
  pip install --upgrade pip
  pip install --no-cache-dir twine
else
  source $PY_ENV/bin/activate
fi

# Upload to Pip
echo
echo -n "Do you want to upload the ${whl_file} file? (y/n): " 
read answer
if [[ "$answer" == "y" ]]; then
    twine upload $whl_file
else
    echo "Aborted"
fi
