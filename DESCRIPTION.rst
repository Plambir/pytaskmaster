PyTaskmaster
============

Simple way to create build script on python.

Features
--------

  - CLI tool for launch task
  - Config manager on JSON files
  - Generator for configuration headers

Usage
-----

Create `master.py` in project folder or use `master -t` for create template
`master.py`.

See `master -h` for more information.

For zsh users
-------------

.. code:: shell

          _master() {
          typeset -A opt_args

          _arguments '(-h --help)'{-h,--help}'[show this help message and exit]' \
                     '(-s --show-tasks)'{-s,--show-tasks}'[show all tasks from master file]' \
                     '(-f --file)'{-f,--file}'[use custom FILE for run tasks]:file:_files' \
                     '(-t --template)'{-t,--template}'[create `master.py` from template]'
          }

          compdef _master master

Source code
-----------

You can access the source code at: https://github.com/Plambir/pytaskmaster

Release History
---------------

1.1.0 (2015-0?-??)
------------------

  - Add CLI script
  - Refactoring `pytaskmaster` module

1.0.0 (2015-03-15)
------------------

First working version
