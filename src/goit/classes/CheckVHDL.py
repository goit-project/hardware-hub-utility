import re

from goit.classes.Check import Check

class CheckVHDL(Check):
    """Documentation for a class.
 
    More details.
    """
    def __init__(self, argv):
        """The constructor."""
        # A dictionary of regular expression settings for each command
        self.commands = {'--!'    : {'name': '--!',     'enabled': True, 'regex': r'\--!.*'},
                        '@file'   : {'name': '@file',   'enabled': True, 'regex': r'\--!\s+@file\s+.*'},
                        '@author' : {'name': '@author', 'enabled': True, 'regex': r'\--!\s+@author\s+.*'},
                        '@brief'  : {'name': '@brief',  'enabled': True, 'regex': r'\--!\s+@brief\s+.*'},
                        '@param'  : {'name': '@param',  'enabled': True, 'regex': r'\--!\s+@param\s+.*'},}
        
        # A dictionary of regular expression settings for each block
        self.elements = {'library'     : {'name': 'library',      'enabled': True, 'document': True,  'regex': r'(?i)\s*(library\s+\S+\s*;)'},
                        'use'          : {'name': 'use',          'enabled': True, 'document': False, 'regex': r'(?i)\s*(use\s+\S+[.]\S+\s*;)'},
                        'entity'       : {'name': 'entity',       'enabled': True, 'document': True,  'regex': r'(?im)^\s*(entity\s+(?P<id>\S+)\s+is[\S\s]+?end(\s+entity)?(\s+(?P=id))?\s*;)'},
                        'architecture' : {'name': 'architecture', 'enabled': True, 'document': True,  'regex': r'(?im)^\s*(architecture\s+(?P<id>\S+)\s+of\s+\S+\s+is[\S\s]+?begin[\S\s]+?end(\s+architecture)?(\s+(?P=id))?\s*;)'},
                        'generic'      : {'name': 'generic',      'enabled': True, 'document': True,  'regex': 'parentheses'},
                        'port'         : {'name': 'port',         'enabled': True, 'document': True,  'regex': 'parentheses'},
                        'port map'     : {'name': 'port map',     'enabled': True, 'document': False, 'regex': 'parentheses'},
                        'generic map'  : {'name': 'generic map',  'enabled': True, 'document': True,  'regex': 'parentheses'},
                        'generate'     : {'name': 'generate',     'enabled': True, 'document': True,  'regex': r'(?im)^\s*((?P<id>\S+)\s*:\s*(for\s+[\S\s]+?\sin\s+[\S\s]+?\s|if\s+[\S\s]+?\s+)generate\s+[\S\s]+?end\s+generate(\s+(?P=id))?\s*;)'},
                        'instance'     : {'name': 'instance',     'enabled': True, 'document': True,  'regex': r'(?im)begin[\S\s]*?^\s*(\w+\s*:(?!\s*if\s+)(\s*component|\s*entity|\s*configuration)?\s+[\S\s]*?;)'}}
        
        # 'generic'      : {'name': 'generic',      'enabled': True, 'regex': r'(?im)^\s*(generic\s*\([\S\s]*?\)\s*;)'},
        # 'port'         : {'name': 'port',         'enabled': True, 'regex': r'(?im)^\s*(port\s*\([\S\s]*?\)\s*\)\s*;)'},
        #                                                                       (?im)^\s*(port\s*\([\S\s]*?(\)\s*\)\s*;|\)\s*(?:--.*\s*)*\)\s*;))
        #                                                                       (?im)^\s*(port\s*\(([^\(\)]*\([^\(\)]*\)[^\(\)]*)*?[^\(\)]*\s*\)\s*;)

        # 'parent': [],                                       
        # 'parent': [],                                       
        # 'parent': [],                                       
        # 'parent': [],                                       
        # 'parent': ['component', 'entity', 'configuration'], 
        # 'parent': ['component', 'entity', 'configuration'], 
        # 'parent': ['instance'],                             
        # 'parent': ['instance'],                             
        # 'parent': ['architecture'],                         
        # 'parent': ['architecture'],                         

        # Creates a dictionary of results with the same keys as in commands
        self.res_command = {}
        for key, val in self.commands.items():
            if val['enabled']:
                self.res_command[key] = {'data' : [], 'spans' : [], 'lines' : []}

        # Creates a dictionary of block results and their location in the file
        self.res_block = {}
        for key, val in self.elements.items():
            if val['enabled']:
                self.res_block[key] = {'data' : [], 'spans' : [], 'lines' : []} 

        # Reading a file for analysis
        with open(argv) as f:
            self.document = f.read()

        # Get all '\n' positions
        self.line_pos = []
        for i, symbol in enumerate(self.document):
            if symbol == '\n':
                self.line_pos.append(i)

    def locateBlock(self, document, idx):
        opened  = 0
        comment = False
        total   = len(document)
        begin   = idx

        while idx < total:
            if not comment:
                if opened == 0:
                    if document[idx] == '(':
                        opened += 1
                else:
                    if document[idx] == '(':
                        opened += 1
                    if document[idx] == ')':
                        opened -= 1
                    if opened == 0:
                        break

                if document[idx: idx+2] == '--':
                    comment = True
            else:
                if document[idx] == '\n':
                    comment = False

            idx += 1

        return document[begin: idx+1], (begin, idx+1)
    

    def spanToLines(self, span, line_pos):
        line_first = 0
        line_last  = 0

        for i, pos in enumerate(line_pos):
            if pos >= span[0]:
                line_first = i + 1
                break

        for i, pos in enumerate(line_pos):
            if not pos < span[1]:
                line_last = i + 1
                break
        
        return (line_first, line_last)
    

    def printDemo(self, args):
        data = []
        for key in self.res_block.keys():
            for bounds in self.res_block[key]['lines']:
                # Checks if documentation for element is required
                document = ""
                if self.elements[key]['document'] == True:
                    document = '--!'

                # Finds closest previous element boundary
                previous = 0
                for k in self.res_block.keys():
                    for bnd in self.res_block[k]['lines']:
                        if bnd[0] == bnd[1]: # One line element
                            if bounds[0] < bnd[0] and bnd[0] > previous:
                                previous = bnd[0]
                        else: # Block
                            if bnd[0] < bounds[0] and bounds[0] < bnd[1]: # Inside
                                pass
                            else: # Outside
                                pass

                if document == '--!':
                    document += ' Prev element at: ' + str(previous) + ' ' + key

                # Determines if a block is contained within another block
                tabbed = ""
                for k in self.res_block.keys():
                    for bnd in self.res_block[k]['lines']:
                        if bnd[0] < bounds[0] and bounds[0] < bnd[1]:
                            tabbed += "\t".expandtabs(4)
                
                # Sets the color depending on the depth of the element
                if bounds[0] == bounds[1]:
                    data.append([tabbed + key, bounds[0], '', '', document])
                else:
                    data.append([tabbed + key,          bounds[0], '\x1b[38;2;0;' + str(int(len(tabbed)/4 * 100)) +';0m', '\x1b[0m', document])
                    data.append([tabbed + key + " end", bounds[1], '\x1b[38;2;0;' + str(int(len(tabbed)/4 * 100)) +';0m', '\x1b[0m', ''])
        
        # Sorts the data in the correct order, taking into account the location in the file
        data_sorted = sorted(data, key=lambda x: x[1])

        # Finds the longest possible line
        str_len = len(max(data, key=lambda x: len(x[0]))[0])

        for i in data_sorted:
            print("{}{:{}}{} {:}".format(i[2], i[0], str_len, i[3], i[4]))
        
        # print(data_sorted)
        # print(len(self.document.splitlines()))


    def analyze(self, document):
        """Function to analyze input file."""

        # Finds all enabled commands related to doxygen
        for key, val in self.commands.items():
            if val['enabled']:
                pattern = re.compile(val['regex'])
                for result in pattern.finditer(document):
                    self.res_command[key]['data'].append(result.group())
                    self.res_command[key]['spans'].append(result.span())
                    self.res_command[key]['lines'].append(self.spanToLines(result.span(), self.line_pos))

        # Finds all entities, architectures and their boundaries
        for key, val in self.elements.items():
            if val['enabled']:
                if val['regex'] == 'parentheses':
                    pattern = re.compile(r'(?i)\s*('+val['name']+r'\s*\(.*)')
                    for result in pattern.finditer(document):
                        data, span = self.locateBlock(document, result.span(1)[0])
                        self.res_block[key]['data'].append(data)
                        self.res_block[key]['spans'].append(span)
                        self.res_block[key]['lines'].append(self.spanToLines(span, self.line_pos))
                else:
                    pattern = re.compile(val['regex'])
                    for result in pattern.finditer(document):
                        self.res_block[key]['data'].append(result.group(1))
                        self.res_block[key]['spans'].append(result.span(1))
                        self.res_block[key]['lines'].append(self.spanToLines(result.span(1), self.line_pos))

        return self.res_command, self.res_block


    def printStats(self):
        """Function to print statistics after analysis."""

        for key, val in self.commands.items():
            if val['enabled']:
                print("{:} {:12} found: {:2} {}".format("Command:", key, len(self.res_command[key]['spans']), self.res_command[key]['lines']))

        for key, val in self.elements.items():
            if val['enabled']:
                print("{:8} {:12} found: {:2} {}".format("Element:", key, len(self.res_block[key]['spans']), self.res_block[key]['lines']))


