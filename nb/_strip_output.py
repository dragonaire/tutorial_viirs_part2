#!/usr/bin/env python
"""
Strip outputs from an IPython Notebook

Opens a notebook, strips its output, and writes the outputless version to the
original file. Useful for version control if you don't want to track output.

This does mostly the same thing as the `Clear All Output` command in the
notebook UI.

see
http://stackoverflow.com/questions/18734739/using-ipython-notebooks-under-version-control
"""
import sys

try:
    from nbformat import v4
except ImportError:
    raise Exception(
        "Failed to import the latest IPython while trying to strip output "
        "from your notebooks.  Either run venv/bin/activate to enter your "
        "virtual env, or update the IPython version on your machine "
        "(sudo pip install -U ipython)")


def strip_output(nb):
    """strip the outputs from a notebook object"""
    for cell in nb.cells:
        if 'outputs' in cell:
            cell['outputs'] = []
        if 'execution_count' in cell:
            cell['execution_count'] = 0
    return nb

if __name__ == '__main__':
    nb = v4.reads(sys.stdin.read())
    nb = strip_output(nb)
    sys.stdout.write(v4.writes(nb))
