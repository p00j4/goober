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
        super(Goober, self).options(parser, env)

    def configure(self, options, conf):
        super(Goober, self).configure(options, conf)
        self.prefix = ''
        if not options.prefix:
            return
        self.env_vars = options.prefix.split(',')
        if self.env_vars:
            self.assemble_prefix()

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

    def finalize(self, result):
        if not result.errors and not result.failures:
           print "ALL GOOD!"
           return

        problems = []
        for error in result.errors:
            problems.append(self.get_output(error[0])) 
        for failure in result.failures:
            problems.append(self.get_output(failure[0])) 

        print "YOU SHOULD RE-RUN:"
        msg = "nosetests -v --goober "
        if self.prefix:
            msg = self.prefix + msg + '--goober-prefix=' + ','.join(self.env_vars) + ' '
        print msg + ' '.join(problems)
        