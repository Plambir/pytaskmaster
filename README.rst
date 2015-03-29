PyTaskmaster
============

Simple way to create build script on python. Use `pytaskmaster.Config` for load
or save project configs in json format. Use `pytaskmaster.generator` for
substitution placeholder (powered by string.Template) in input file like
`config.in.h` to `config.h`. Use `pytaskmaster.shell` shortcut for launch
console commands. Use `pytaskmaster.bench` for benchmarking tasks.

Install
-------

Uses `pip`:

.. code:: shell

          pip install pytaskmaster

Usage
-----

Create `master.py` in project folder or use `master -t` for create template
`master.py`.

See `master -h` for more information.
