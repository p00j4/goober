goober
======

Look what just came out of my nose(tests)

The nosetest multiprocess plugin is great because it lets you run tests in parallel (that is, fast).
The nosetest TestId plugin is great because it lets you run failed tests on subsequent runs (with --failed).
Multiprocess and TestId don't work well together. So, how do we know which tests to re-run after a quick multiprocess run?

This plugin prints out 'nosetests -v' plus the paths to those failing tests. The idea is to make it as easy as possible to just run the troublesome tests from a multiprocess test run.

Usage:

```nosetests --goober --processes=-1 path/to/tests```
