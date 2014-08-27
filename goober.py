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
    enableOpt = "goober"
    activate = "--goober"

    def __init__(self):
        super(Goober, self).__init__()
        
    def options(self, parser, env):
        parser.add_option('--goober',
                          default=False,
                          help="print failed test paths: %s" %
                          (self.help()))

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
        print "nosetests -v " + ' '.join(problems)
        