import re
import itertools

from goit.classes.Check import Check

class Element():
    id_iter = itertools.count(1)

    def __init__(self, name = "", span = (0,0), data = "", validate = None, type = ""):
        self.name       = name                              # Name of the element from the configuration
        self.span       = span                              # Element span in the document
        self.data       = data                              # Element data 
        self.validate   = validate                          # If True the element must be documented and a search will be performed
        self.type       = type                              # There are two types of elements: documentation and code
        self.id         = next(Element.id_iter)             # Unique element identifier
        self.parent_id  = 0                                 # Parent identifier
        self.doc_id     = []                                # List of documentation IDs for this element
        self.depth      = 0                                 # Element depth
        self.end        = "{} end".format(name)             # End of element if it contains others
        self.color      = ['\x1b[38;2;0;0;0m', '\x1b[0m']   # Element color
        self.note       = ""                                # Documentation conclusions if validate == True
        self.note_color = ['\x1b[38;2;0;0;0m', '\x1b[0m']   # Conclusions color


class Settings():
    def __init__(self, name = "", entry = {}):
        self.name    = name
        self.enabled = entry['enabled'] if 'enabled' in entry else True
        self.valid   = entry['validate'] if 'validate' in entry else False
        self.func    = entry['fun'] if 'fun' in entry else None
        self.args    = entry['args']
        self.type    = entry['type']
        self.regex   = self.args[0]
        self.configs = self.args[1] if 1 < len(self.args) else None


class CheckVHDL(Check):
    """Documentation for a class.
 
    More details.
    """

    def config(config = None):
        # name      mandatory entry | name of element
        # type      mandatory entry | doc - documentation, cod - code
        # args      mandatory entry | 
        # enabled   optional entry  | default will be True
        # validate  optional entry  | default will be False
        # fun       optional entry  | default will be None
        if config is None:
            config = { '--!'          :{'enabled': True, 'validate': False, 'type': 'doc', 'fun': None,                 'args': [r'(--!.*)']},
                       '@file'        :{'enabled': True, 'validate': False, 'type': 'doc', 'fun': None,                 'args': [r'--!\s*(@file\s+.*)']},
                       '@author'      :{'enabled': True, 'validate': False, 'type': 'doc', 'fun': None,                 'args': [r'--!\s*(@author\s+.*)']},
                       '@brief'       :{'enabled': True, 'validate': False, 'type': 'doc', 'fun': None,                 'args': [r'--!\s*(@brief\s+.*)']},
                       '@param'       :{'enabled': True, 'validate': False, 'type': 'doc', 'fun': None,                 'args': [r'--!\s*(@param\s+.*)']},
                       'library'      :{'enabled': True, 'validate': True,  'type': 'cod', 'fun': None,                 'args': [r'(?im)^(?:(?!--).)*?(library\s+\S+\s*;)']},
                       'use'          :{'enabled': True, 'validate': True,  'type': 'cod', 'fun': None,                 'args': [r'(?im)^(?:(?!--).)*?(use\s+\S+[.]\S+\s*;)']},
                       'entity'       :{'enabled': True, 'validate': True,  'type': 'cod', 'fun': None,                 'args': [r'(?im)^(?:(?!--).)*?(entity\s+(?P<id>\S+)\s+is[\S\s]+?end(\s+entity)?(\s+(?P=id))?\s*;)']},
                       'architecture' :{'enabled': True, 'validate': True,  'type': 'cod', 'fun': None,                 'args': [r'(?im)^(?:(?!--).)*?(architecture\s+(?P<id>\S+)\s+of\s+\S+\s+is[\S\s]+?begin[\S\s]+?end(\s+architecture)?(\s+(?P=id))?\s*;)']},
                       'generic'      :{'enabled': True, 'validate': True,  'type': 'cod', 'fun': CheckVHDL.locate_end, 'args': [r'(?im)^(?:(?!--).)*?(generic\s*\()']},
                       'port'         :{'enabled': True, 'validate': True,  'type': 'cod', 'fun': CheckVHDL.locate_end, 'args': [r'(?im)^(?:(?!--).)*?(port\s*\()']},
                       'port map'     :{'enabled': True, 'validate': True,  'type': 'cod', 'fun': CheckVHDL.locate_end, 'args': [r'(?im)^(?:(?!--).)*?(port\s+map\s*\()']},
                       'generic map'  :{'enabled': True, 'validate': True,  'type': 'cod', 'fun': CheckVHDL.locate_end, 'args': [r'(?im)^(?:(?!--).)*?(generic\s+map\s*\()']},
                       'generate'     :{'enabled': True, 'validate': True,  'type': 'cod', 'fun': None,                 'args': [r'(?im)^(?:(?!--).)*?((?P<id>\S+)\s*:\s*(for\s+[\S\s]+?\sin\s+[\S\s]+?\s|if\s+[\S\s]+?\s+)generate\s+[\S\s]+?end\s+generate(\s+(?P=id))?\s*;)']},
                       'instance'     :{'enabled': True, 'validate': True,  'type': 'cod', 'fun': None,                 'args': [r'(?im)^(?:(?!--).)*?begin[\S\s]*?^\s*(\w+\s*:(?!\s*if\s+)(\s*component|\s*entity|\s*configuration)?\s+[\S\s]*?;)']},
                       'port_signal'  :{'enabled': True, 'validate': True,  'type': 'cod', 'fun': CheckVHDL.locate_in,  'args': [r'(?im)^(?:(?!--).)*?(\w+\s*:\s*(in|out|inout|buffer|linkage)?\s+[\S\s]+?)(\s+:=\s+[\S\s]+?)?\s*(?:;|--|\)\s*;)', ['port']]},
                       'generic_param':{'enabled': True, 'validate': True,  'type': 'cod', 'fun': CheckVHDL.locate_in,  'args': [r'(?im)^(?:(?!--).)*?(\w+\s*:\s*[\S\s]+?(\s+:=\s+[\S\s]+?)?)\s*(?:;|--|\)\s*;)', ['generic']]},
                    }

        return config


    def analyze(self, document, config):
        """Function to analyze document."""
        self.elements   = {}
        Element.id_iter = itertools.count(1)

        # Creates all elements according to configuration
        for name, entry in config.items():
            set = Settings(name, entry)

            if set.enabled:
                # Composes a pattern to search for elements in a document
                pattern = re.compile(set.regex)

                if set.func == CheckVHDL.locate_end:
                    for result in pattern.finditer(document):
                        data, span = set.func(document, result.span(1))
                        element    = Element(set.name, span, data, set.valid, set.type)
                        self.elements[element.id] = element

                elif set.func == CheckVHDL.locate_in:
                    for name in set.configs:                        
                        parent_set     = Settings(name, config[name])
                        parent_pattern = re.compile(parent_set.regex)

                        for parent_result in parent_pattern.finditer(document):
                            parent_data, parent_span = CheckVHDL.locate_end(document, parent_result.span(1))
                            
                            for result in pattern.finditer(parent_data):
                                data, span = (result.group(1), (parent_span[0] + result.span(1)[0], parent_span[0] + result.span(1)[1]))
                                element    = Element(set.name, span, data, set.valid, set.type)
                                self.elements[element.id] = element
                else:
                    for result in pattern.finditer(document):
                        data, span = (result.group(1), result.span(1))
                        element    = Element(set.name, span, data, set.valid, set.type)
                        self.elements[element.id] = element                

        # Sets the depth and parent id for all newly created elements
        for child in self.elements.values():
            for parent in self.elements.values():
                # The child element is inside another element
                if parent.span[0] < child.span[0] and child.span[1] < parent.span[1]:
                    child.depth += 1
                    
                    if child.parent_id == 0:
                        child.parent_id = parent.id
                    else:
                        parent_current = self.elements[child.parent_id]
                        
                        # The nearest element is parent
                        if parent_current.span[0] < parent.span[0]:
                            child.parent_id = parent.id

        # Sorts elements by position in the file
        elements_sorted = sorted(self.elements.items(), key=lambda item: item[1].span[0])

        # Searches for documentation and adds its ID to the list
        for i, (_, element) in enumerate(elements_sorted):            
            if element.validate and element.type == "cod":
                # Looking for documentation before the element
                rear_i = i
                while 0 < rear_i:
                    rear_i -= 1
                    prev_element = elements_sorted[rear_i][1]
                    
                    if 0 < rear_i - 1:
                        prev_prev_element = elements_sorted[rear_i-1][1]
                        lines_prev_prev   = self.span_to_lines(prev_prev_element.span, self.line_pos)
                        lines_prev        = self.span_to_lines(prev_element.span, self.line_pos)

                        # The documentation is on the same line as the other code
                        if prev_prev_element.type == "cod" and lines_prev_prev[1] == lines_prev[1]:
                            break

                    if prev_element.type == "doc" and prev_element.parent_id == element.parent_id:
                        element.doc_id.insert(0, prev_element.id)
                    else:
                        break

                # Looking for documentation after the element on the same line (special case for port_signal)
                if element.name == "port_signal": 
                    front_i = i + 1 
                    if front_i < len(elements_sorted):
                        next_element = elements_sorted[front_i][1]
                        
                        # Checks if both are on the same line
                        next_lines = self.span_to_lines(next_element.span, self.line_pos)
                        lines      = self.span_to_lines(element.span, self.line_pos)

                        if next_element.type == "doc" and next_lines == lines:
                            element.doc_id.append(next_element.id)

                # Looking for documentation in @param (special case for generic_param)
                if element.name == "generic_param":
                    generic = self.elements[element.parent_id]
                    entity  = self.elements[generic.parent_id]

                    name_in_code = element.data.split(' ')[0]

                    for id in entity.doc_id:
                        if self.elements[id].name == "@param":
                            name_in_param = self.elements[id].data.split(' ')[1]

                            if name_in_code.upper() == name_in_param.upper():
                                element.doc_id.append(id)


        return self.elements


    def demo(self, elements):
        """Function to print demo after analysis."""

        # Sorts elements by position in the file
        elements_sorted = sorted(elements.values(), key=lambda item: item.span[0])

        for element in elements_sorted:
            # Checks documentation and formats notes
            if element.validate:    
                color = (0, 180, 0) if element.doc_id else (180, 0, 0)

                element.note_color[0] = self.set_text_color(*color)
                element.note          = " --! Documented: {c0}{}{c1}".format(bool(element.doc_id), c0=element.note_color[0], c1=element.note_color[1])

                # Sets the color according to the depth of the element
                element.color[0] = self.set_text_color(0, element.depth * 80, 0)

        # Gets the object of the longest element and its length to format notes 
        tab_len = 4
        element = max(elements_sorted, key=lambda elem: len(elem.end) + elem.depth * tab_len)
        max_len = len(element.end) + element.depth * tab_len

        # Helper class to improve readability
        class FormatElement():
            def __init__(self, element):
                self.tabs  = "\t".expandtabs(tab_len) * element.depth
                self.width = max_len - tab_len * element.depth
                self.c0    = element.color[0]
                self.c1    = element.color[1]

        # Formats output
        demo = []
        for element, next_element in zip(elements_sorted, elements_sorted[1:] + [elements_sorted[0]]):
            # Creates a record with the beginning of the element
            fmt = FormatElement(element)
            demo.append("{}{c0}{:{w}}{c1}{}".format(fmt.tabs, element.name, element.note, w=fmt.width, c0=fmt.c0, c1=fmt.c1))

            # A smaller depth for the next element means that a record must be created with the end of the element
            if next_element.depth < element.depth:
                current_depth = element.depth
                parent        = elements[element.parent_id]
                
                # Closes all elements until the level is the same as the next element
                while next_element.depth < current_depth: 
                    fmt = FormatElement(parent)
                    demo.append("{}{c0}{:{w}}{c1}".format(fmt.tabs, parent.end, w=fmt.width, c0=fmt.c0, c1=fmt.c1))

                    if parent.parent_id != 0:
                        parent = elements[parent.parent_id]

                    current_depth -= 1

        return demo


    def stats(self, elements, config):
        """Function to print statistics after analysis."""

        stats = []
        for name, elem in config.items():
            if elem['enabled']:
                count = 0
                lines = []
                for element in elements.values():
                    if element.name == name:
                        count += 1
                        lines.append(self.span_to_lines(element.span, self.line_pos))
                    
                stats.append("{:8} {:12} found: {:2} {}".format("Element:", name, count, lines))
        
        return stats
    
    def compact(self, elements):
        """Function to summarize the results of file analysis in a compact form"""

        # Sorts elements by location in the file using the starting position of the element
        elements_sorted = sorted(self.elements.items(), key=lambda item: item[1].span[0])

        result = {}
        for (_, element) in elements_sorted:
            # Checks if the document has @author
            if element.name == "@author":
                author = " ".join(element.data.split(' ')[1:])

                if element.name in result.keys():
                    result[element.name].append(author)
                else:
                    result[element.name] = [author]

            # Checks if the entity has @brief
            elif element.name == "entity":
                doc_key = "@brief"
                doc_val = 0

                for id in element.doc_id:
                    if elements[id].name == doc_key:
                        doc_val = 1
  
                if element.name in result.keys():
                    result[element.name].append({doc_key : doc_val})
                else:
                    result[element.name] = [{doc_key : doc_val}]

            # Counts elements and their documentation
            elif element.name == "port_signal" or element.name == "generic_param":
                docum, total = (0, 0)

                if element.name in result.keys():
                    docum, total = result[element.name]

                total += 1

                if 0 < len(element.doc_id):
                    docum += 1

                result[element.name] = (docum, total)

        return result


    @staticmethod
    def locate_in(document, span):
        total = len(document)
        pos   = span[1]

        
        return document[span[0]: pos+1], (span[0], pos+1)

    
    @staticmethod
    def locate_end(document, span):
        total   = len(document)
        pos     = span[1]       # Location next to the opening
        opened  = 1             # So, the block is already open
        comment = False         # Flag for iteration in a comment

        # Possible block boundaries
        begin, end = {'(': ('(',')'),
                      '[': ('[',']'),
                      '{': ('{','}')}[document[span[1]-1]]

        while pos < total:
            if document[pos: pos+2] == '--':
                comment = True
            
            if not comment:
                if 0 < opened:
                    if document[pos] == begin:
                        opened += 1
                    if document[pos] == end:
                        opened -= 1
                else:
                    if document[pos] == ';':
                        break
            else:
                if document[pos] == '\n':
                    comment = False

            pos += 1

        return document[span[0]: pos+1], (span[0], pos+1)


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


