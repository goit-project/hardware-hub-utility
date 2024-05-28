import re
import itertools

from goit.classes.Check import Check

class Element():
    id_iter = itertools.count(1)

    def __init__(self, name = "", span = (0,0), data = "", validate = None):
        self.__dict__   = dict(vars())           
        self.id         = next(Element.id_iter)
        self.parent_id  = 0
        self.depth      = 0
        self.ending     = "{} end".format(name)
        self.color      = ['\x1b[38;2;0;0;0m', '\x1b[0m']
        self.note       = ""
        self.note_color = ['\x1b[38;2;0;0;0m', '\x1b[0m']

class CheckVHDL(Check):
    """Documentation for a class.
 
    More details.
    """
    settings = []
    elements = {}

    def __init__(self, argv):
        """The constructor."""

        self.settings = [{'name': '--!',          'enabled': True,                    'regex': r'(--!.*)'},
                         {'name': '@file',        'enabled': True,                    'regex': r'(--!\s+@file\s+.*)'},
                         {'name': '@author',      'enabled': True,                    'regex': r'(--!\s+@author\s+.*)'},
                         {'name': '@brief',       'enabled': True,                    'regex': r'(--!\s+@brief\s+.*)'},
                         {'name': '@param',       'enabled': True,                    'regex': r'(--!\s+@param\s+.*)'},
                         {'name': 'library',      'enabled': True, 'validate': True,  'regex': r'(?i)\s*(library\s+\S+\s*;)'},
                         {'name': 'use',          'enabled': True, 'validate': True,  'regex': r'(?i)\s*(use\s+\S+[.]\S+\s*;)'},
                         {'name': 'entity',       'enabled': True, 'validate': True,  'regex': r'(?im)^\s*(entity\s+(?P<id>\S+)\s+is[\S\s]+?end(\s+entity)?(\s+(?P=id))?\s*;)'},
                         {'name': 'architecture', 'enabled': True, 'validate': True,  'regex': r'(?im)^\s*(architecture\s+(?P<id>\S+)\s+of\s+\S+\s+is[\S\s]+?begin[\S\s]+?end(\s+architecture)?(\s+(?P=id))?\s*;)'},
                         {'name': 'generic',      'enabled': True, 'validate': True,  'regex': 'parentheses'},
                         {'name': 'port',         'enabled': True, 'validate': True,  'regex': 'parentheses'},
                         {'name': 'port map',     'enabled': True, 'validate': True,  'regex': 'parentheses'},
                         {'name': 'generic map',  'enabled': True, 'validate': True,  'regex': 'parentheses'},
                         {'name': 'generate',     'enabled': True, 'validate': True,  'regex': r'(?im)^\s*((?P<id>\S+)\s*:\s*(for\s+[\S\s]+?\sin\s+[\S\s]+?\s|if\s+[\S\s]+?\s+)generate\s+[\S\s]+?end\s+generate(\s+(?P=id))?\s*;)'},
                         {'name': 'instance',     'enabled': True, 'validate': True,  'regex': r'(?im)begin[\S\s]*?^\s*(\w+\s*:(?!\s*if\s+)(\s*component|\s*entity|\s*configuration)?\s+[\S\s]*?;)'}]

        # Reading a file for analysis
        with open(argv) as f:
            self.document = f.read()

        # Get all '\n' positions
        self.line_pos = []
        for i, symbol in enumerate(self.document):
            if symbol == '\n':
                self.line_pos.append(i)

    def analyze(self, document):
        """Function to analyze input file."""

        # Creates all elements according to settings
        for val in self.settings:
            if val['enabled']:
                name     = val['name']
                validate = val['validate'] if 'validate' in val else None
                
                # Composes a pattern to search for elements in a document
                if val['regex'] == 'parentheses':
                    pattern = re.compile(r'(?i)\s*('+name+r'\s*\(.*)')
                else:
                    pattern = re.compile(val['regex'])

                for result in pattern.finditer(document):
                    if val['regex'] == 'parentheses':
                        data, span = self.locateBlock(document, result.span(1)[0])
                    else:
                        data, span = (result.group(1), result.span(1))

                    element = Element(name, span, data, validate)
                    
                    self.elements[element.id] = element

        # Sets the depth and parent id for all newly created elements
        for child in self.elements.values():
            for parent in self.elements.values():
                # The element is inside another element
                if parent.span[0] < child.span[0] and child.span[1] < parent.span[1]:
                    child.depth += 1
                    
                    if child.parent_id == 0:
                        child.parent_id = parent.id
                    else:
                        parent_current = self.elements[child.parent_id]
                        
                        # The nearest element is parent
                        if parent_current.span[0] < parent.span[0]:
                            child.parent_id = parent.id

        return self.elements


    def print_demo(self, args):
        tab_len  = 4
        elem_map = []

        # Maps all elements and their boundaries
        for element in self.elements.values():
            lines = self.span_to_lines(element.span, self.line_pos)
            
            elem_map.append([element.span[0], element, 0])
            
            if lines[0] != lines[1]:
                elem_map.append([element.span[1], element, 1])

        # Sorts the data in the correct order, taking into account the location in the file
        elem_map_sorted = sorted(elem_map, key=lambda elem: elem[0])

        # Formats notes on doxygen documentation
        for i, elem in enumerate(elem_map_sorted):
            element = elem[1]
            doc_bwd = 0
            doc_fwd = 0
            
            if element.validate and elem[2] == 0:
                # Looking for documentation before the element
                bwd_i = i
                while 0 < bwd_i:
                    bwd_i -= 1
                    prev_element = elem_map_sorted[bwd_i][1]
                    
                    if prev_element.name == "--!":
                        doc_bwd += 1
                    else:
                        break

                # Looking for documentation inside the element
                fwd_i = i
                while fwd_i < len(elem_map_sorted):
                    fwd_i += 1
                    next_element = elem_map_sorted[fwd_i][1]
                    
                    if next_element.name == "--!":
                        doc_fwd += 1
                    else:
                        # Documentation previously found was for a different element
                        if next_element != element:
                            doc_fwd = 0
                        break
                
                # Set the color depending on the availability of the documentation
                if doc_bwd == 0 and doc_fwd == 0:
                    element.note_color[0] = self.set_text_color(180, 0, 0)
                if doc_bwd > 0 or doc_fwd > 0:
                    element.note_color[0] = self.set_text_color(180, 180, 0)
                if doc_bwd > 0 and doc_fwd > 0:
                    element.note_color[0] = self.set_text_color(0, 180, 0)

                element.note = "{c0}--! Documented: {:} before, {:} inside{c1}".format(doc_bwd, doc_fwd, c0=element.note_color[0], c1=element.note_color[1])

        # Sets the color according to the depth of the element
        for elem in elem_map_sorted:
            element = elem[1]
            element.color[0] = self.set_text_color(0, element.depth * 80, 0)

        # Gets the object of the longest element and its length to format notes 
        element = max(elem_map, key=lambda elem: len(elem[1].ending) + elem[1].depth * tab_len)[1]
        max_len = len(element.ending) + element.depth * tab_len

        # Formats output
        for elem in elem_map_sorted:
            element = elem[1]

            tabs    = "\t".expandtabs(tab_len * element.depth)
            name    = ""
            note    = ""
            width   = max_len - tab_len * element.depth
            color0  = element.color[0]
            color1  = element.color[1] 

            if elem[2] == 0:
                name = element.name

                if element.validate:
                    note = element.note
            else:
                name = element.ending
            
            if element.validate is not None:
                print("{}{c0}{:{w}}{c1} {}".format(tabs, name, note, w=width, c0=color0, c1=color1))
            # print("{}{c0}{:{w}}{c1} {}".format(tabs, name, note, w=width, c0=color0, c1=color1))


    def print_stats(self):
        """Function to print statistics after analysis."""

        for elem in self.settings:
            if elem['enabled']:
                count = 0
                lines = []
                for key, element in self.elements.items():
                    if element.name == elem['name']:
                        count += 1
                        lines.append(self.span_to_lines(element.span, self.line_pos))
                    
                print("{:8} {:12} found: {:2} {}".format("Element:", elem['name'], count, lines))


    def locateBlock(self, document, pos):
        opened  = 0
        comment = False
        total   = len(document)
        begin   = pos

        while pos < total:
            if not comment:
                if opened == 0:
                    if document[pos] == '(':
                        opened += 1
                else:
                    if document[pos] == '(':
                        opened += 1
                    if document[pos] == ')':
                        opened -= 1
                    if opened == 0:
                        break

                if document[pos: pos+2] == '--':
                    comment = True
            else:
                if document[pos] == '\n':
                    comment = False

            pos += 1

        return document[begin: pos+1], (begin, pos+1)
    

    def span_to_lines(self, span, line_pos):
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
    
    def set_text_color(self, r, g, b):
        return "\x1b[38;2;{};{};{}m".format(r, g, b)


