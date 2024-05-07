#!/usr/bin/env python
# coding: utf-8

import os
import re
import sys

class Check():
    """Documentation for a class.
 
    More details.
    """
    def __init__(self, argv):
        """The constructor."""
        # A dictionary of regular expression settings for each command
        self.commands = {'--!'    : {'name': '--!',     'enabled': True, 'regex': r'\--!.*'},
                        '@file'   : {'name': '@file',   'enabled': True, 'regex': r'\--!\s+@file\s+.*'},
                        '@author' : {'name': '@author', 'enabled': True, 'regex': r'\--!\s+@author\s+.*'},
                        '@brief'  : {'name': '@brief',  'enabled': True, 'regex': r'\--!\s+@brief\s+.*'},}
        
        # A dictionary of regular expression settings for each block
        self.elements = {'library'     : {'name': 'library',      'enabled': True, 'regex': r'(?i)\s*(library\s+\S+\s*;)'},
                        'use'          : {'name': 'use',          'enabled': True, 'regex': r'(?i)\s*(use\s+\S+[.]\S+\s*;)'},
                        'entity'       : {'name': 'entity',       'enabled': True, 'regex': r'(?im)^\s*(entity\s+(?P<id>\S+)\s+is[\S\s]+?end(\s+entity)?(\s+(?P=id))?\s*;)'},
                        'architecture' : {'name': 'architecture', 'enabled': True, 'regex': r'(?im)^\s*(architecture\s+(?P<id>\S+)\s+of\s+\S+\s+is[\S\s]+?end(\s+architecture)?(\s+(?P=id))?\s*;)'},
                        'generic'      : {'name': 'generic',      'enabled': True, 'regex': 'parentheses'},
                        'port'         : {'name': 'port',         'enabled': True, 'regex': 'parentheses'},
                        'port map'     : {'name': 'port map',     'enabled': True, 'regex': 'parentheses'},
                        'generate'     : {'name': 'generate',     'enabled': True, 'regex': r'(?im)^\s*((?P<id>\S+)\s*:\s*(for\s+[\S\s]+?\sin\s+[\S\s]+?\s|if\s+[\S\s]+?\s+)generate\s+[\S\s]+?end\s+generate(\s+(?P=id))?\s*;)'},
                        'instance'     : {'name': 'instance',     'enabled': True, 'regex': r'(?im)begin[\S\s]*?^\s*(\w+\s*:(?!\s*if\s+)(\s*component|\s*entity|\s*configuration)?\s+[\S\s]*?;)'}}
        
        # 'generic'      : {'name': 'generic',      'enabled': True, 'regex': r'(?im)^\s*(generic\s*\([\S\s]*?\)\s*;)'},
        # 'port'         : {'name': 'port',         'enabled': True, 'regex': r'(?im)^\s*(port\s*\([\S\s]*?\)\s*\)\s*;)'},
        #                                                                       (?im)^\s*(port\s*\([\S\s]*?(\)\s*\)\s*;|\)\s*(?:--.*\s*)*\)\s*;))
        #                                                                       (?im)^\s*(port\s*\(([^\(\)]*\([^\(\)]*\)[^\(\)]*)*?[^\(\)]*\s*\)\s*;)

        # Creates a dictionary of results with the same keys as in commands
        self.res_command = {}
        for key, val in self.commands.items():
            if val['enabled']:
                self.res_command[key] = {'data' : [], 'spans' : []}

        # Creates a dictionary of block results and their location in the file
        self.res_block = {}
        for key, val in self.elements.items():
            if val['enabled']:
                self.res_block[key] = {'data' : [], 'spans' : []} 

        # Reading a file for analysis
        with open(argv) as f:
            self.document = f.read()

    def locateBlock(self, document, idx):
        opened  = 0
        started = False
        comment = False
        total   = len(document)
        begin   = idx

        while idx < total:
            if not comment:
                if not started:
                    if document[idx] == '(':
                        started = True
                        continue
                else:
                    if document[idx] == '(':
                        opened += 1
                    if document[idx] == ')':
                        opened -= 1
                    if opened == 0:
                        if document[idx] == ';':
                            break

                if document[idx: idx+2] == '--':
                    comment = True
            else:
                if document[idx] == '\n':
                    comment = False

            idx += 1

        return document[begin: idx+1], (begin, idx+1)

    def analyze(self, document):
        """Function to analyze input file."""

        # Finds all enabled commands related to doxygen
        for key, val in self.commands.items():
            if val['enabled']:
                pattern = re.compile(val['regex'])
                for result in pattern.finditer(document):
                    self.res_command[key]['data'].append(result.group())
                    self.res_command[key]['spans'].append(result.span())
            
            print("{:8} {:12} found: {}".format("Command:", key, len(self.res_command[key]['spans'])))

        # Finds all entities, architectures and their boundaries
        for key, val in self.elements.items():
            if val['enabled']:
                if val['regex'] == 'parentheses':
                    pattern = re.compile(r'(?i)\s*('+val['name']+r'\s*\(.*)')
                    for result in pattern.finditer(document):
                        data, span = self.locateBlock(document, result.span(1)[0])
                        self.res_block[key]['data'].append(data)
                        self.res_block[key]['spans'].append(span)

                else:
                    pattern = re.compile(val['regex'])
                    for result in pattern.finditer(document):
                        self.res_block[key]['data'].append(result.group(1))
                        self.res_block[key]['spans'].append(result.span(1))



            print("{:8} {:12} found: {}".format("Element:", key, len(self.res_block[key]['spans'])))
        # print(self.res_block['generate']['data'])
        # print(self.res_block['instance']['data'])

        return self.res_command


    def search(self, documet):
        """Function to search special comands."""
        pass
        return result

    def result(self, documet):
        """Function to make conclusions and return results."""
        pass
        return result
    
    def test(self, line):
        """Simple test function."""
        return self.lines[line]
