#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
from nose.plugins.base import Plugin
from nose.case import Test
import logging
import unittest
import os

log = logging.getLogger(__name__)

class Goober(Plugin):
    """
    After a multiprocess test run, print out a one-line command that will rerun all the failed / error'd tests
    """
    name = "goober"
    score = 2
    enableOpt = "goober"
    activate = "--goober"

    def __init__(self):
        super(Goober, self).__init__()
        
    def options(self, parser, env):
        parser.add_option('--goober',
                          action='store_true',
                          help="print failed test paths: %s" %
                          (self.help()))
        parser.add_option('--goober-prefix',
                          action='store',
                          type='string',
                          dest='prefix',
                          help="Environment variables to prepend to goober's output. For example, --goober-prefix='LOCALE' will attach 'LOCALE=<os.environ.get('LOCALE')> to 'nosetests -v --goober'")
        parser.add_option('--goober-extra',
                          action='store',
                          help="append additional nose options to goober's output (give comma separated). For example: --goober-extra=--with-xunit,--with-xcover,--xcoverage-file=coverage.xml")

        super(Goober, self).options(parser, env)

    def configure(self, options, conf):
        super(Goober, self).configure(options, conf)
        self.prefix = ''
        self.extra_options = ''
        if not options.prefix:
            return
        self.env_vars = options.prefix.split(',')
        if self.env_vars:
            self.assemble_prefix()
        if options.goober_extra:
            self.extra_options = str(options.goober_extra).replace(","," ")

    def assemble_prefix(self):
        self.prefix += ' '.join(["%s=%s" % (var, os.environ.get(var)) for var in self.env_vars if os.environ.get(var) is not None]) + ' '

    def get_output(self, test):
        try:
            info = test.test
        except AttributeError:
            info = test._id
        bits = str(info).split('.')
        testname = bits.pop()
        path = "/".join(bits)
        path += ".py:%s" % testname
        return path

    def determine_test_path(self, problem):
        """
        When we receive a multiprocess failure/error object, there is a stacktrace and an id. The id is a string representation of the path to the test that failed. But, no determination is made about whether the test that failed was part of a test class, or a standalone test.

        We will break that id into pieces, splitting on '.' - we will re-assemble that id as a path, from the begnning, and search for it in the stacktrace. The first time we don't find it marks the end of the file path, and the beginning of the name of the test class/specific test. We keep the dots separating that part.
        """
        test, trace = problem
        try:
            test_id = test.id()
        except AttributeError:
            test_id = test._id

        test_bits = str(test_id).split('.')
        path = ''
        while path in trace:
            bit = test_bits.pop(0)
            path += bit + "/"
        path = path.rstrip('/') + '.py'
        path = path + ':' + '.'.join(test_bits)
        return path

    def finalize(self, result):
        if not result.errors and not result.failures:
           print "ALL GOOD!"
           return

        problems = []
        for error in result.errors:
            problems.append(self.determine_test_path(error)) 
        for failure in result.failures:
            problems.append(self.determine_test_path(failure)) 

        print "YOU SHOULD RE-RUN:"
        msg = "nosetests -v --goober "
        if self.prefix:
            msg = self.prefix + msg + '--goober-prefix=' + ','.join(self.env_vars) + ' '
        if self.extra_options:
            msg += str(self.extra_options) + ' '
        
        print msg + ' '.join(problems)
        
