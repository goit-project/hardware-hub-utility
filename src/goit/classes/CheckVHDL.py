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

class CheckVHDL(Check):
    """Documentation for a class.
 
    More details.
    """

    def settings(settings = None):
        # name      mandatory entry | name of element
        # type      mandatory entry | doc - documentation, cod - code
        # args      mandatory entry | 
        # enabled   optional entry  | default will be True
        # validate  optional entry  | default will be False
        # fun       optional entry  | default will be None
        if settings is None:
            settings = { '--!'          :{'enabled': True, 'validate': False, 'type': 'doc', 'fun': None,                 'args': [r'(--!.*)']},
                         '@file'        :{'enabled': True, 'validate': False, 'type': 'doc', 'fun': None,                 'args': [r'--!\s*(@file\s+.*)']},
                         '@author'      :{'enabled': True, 'validate': False, 'type': 'doc', 'fun': None,                 'args': [r'--!\s*(@author\s+.*)']},
                         '@brief'       :{'enabled': True, 'validate': False, 'type': 'doc', 'fun': None,                 'args': [r'--!\s*(@brief\s+.*)']},
                         '@param'       :{'enabled': True, 'validate': False, 'type': 'doc', 'fun': None,                 'args': [r'--!\s*(@param\s+.*)']},
                         'library'      :{'enabled': True, 'validate': True,  'type': 'cod', 'fun': None,                 'args': [r'(?i)\s*(library\s+\S+\s*;)']},
                         'use'          :{'enabled': True, 'validate': True,  'type': 'cod', 'fun': None,                 'args': [r'(?i)\s*(use\s+\S+[.]\S+\s*;)']},
                         'entity'       :{'enabled': True, 'validate': True,  'type': 'cod', 'fun': None,                 'args': [r'(?im)^\s*(entity\s+(?P<id>\S+)\s+is[\S\s]+?end(\s+entity)?(\s+(?P=id))?\s*;)']},
                         'architecture' :{'enabled': True, 'validate': True,  'type': 'cod', 'fun': None,                 'args': [r'(?im)^\s*(architecture\s+(?P<id>\S+)\s+of\s+\S+\s+is[\S\s]+?begin[\S\s]+?end(\s+architecture)?(\s+(?P=id))?\s*;)']},
                         'generic'      :{'enabled': True, 'validate': True,  'type': 'cod', 'fun': CheckVHDL.locate_end, 'args': [r'(?i)\s*(generic\s*\()']},
                         'port'         :{'enabled': True, 'validate': True,  'type': 'cod', 'fun': CheckVHDL.locate_end, 'args': [r'(?i)\s*(port\s*\()']},
                         'port map'     :{'enabled': True, 'validate': True,  'type': 'cod', 'fun': CheckVHDL.locate_end, 'args': [r'(?i)\s*(port\s+map\s*\()']},
                         'generic map'  :{'enabled': True, 'validate': True,  'type': 'cod', 'fun': CheckVHDL.locate_end, 'args': [r'(?i)\s*(generic\s+map\s*\()']},
                         'generate'     :{'enabled': True, 'validate': True,  'type': 'cod', 'fun': None,                 'args': [r'(?im)^\s*((?P<id>\S+)\s*:\s*(for\s+[\S\s]+?\sin\s+[\S\s]+?\s|if\s+[\S\s]+?\s+)generate\s+[\S\s]+?end\s+generate(\s+(?P=id))?\s*;)']},
                         'instance'     :{'enabled': True, 'validate': True,  'type': 'cod', 'fun': None,                 'args': [r'(?im)begin[\S\s]*?^\s*(\w+\s*:(?!\s*if\s+)(\s*component|\s*entity|\s*configuration)?\s+[\S\s]*?;)']},
                         'port_signal'  :{'enabled': True, 'validate': True,  'type': 'cod', 'fun': CheckVHDL.locate_in,  'args': [r'(?i)\s*(\w+\s*:\s*(in|out|inout|buffer|linkage)?\s+[\S\s]+?)(\s+:=\s+[\S\s]+?)?\s*(;|--|\)\s*)', ['port']]},
                         'generic_param':{'enabled': True, 'validate': True,  'type': 'cod', 'fun': CheckVHDL.locate_in,  'args': [r'(?i)\s*(\w+\s*:\s*[\S\s]+?(\s+:=\s+[\S\s]+?)?)\s*(;|--|\)\s*)', ['generic']]},
                        }

        return settings

    def analyze(self, document, settings):
        """Function to analyze document."""
        self.elements   = {}
        Element.id_iter = itertools.count(1)

        # Creates all elements according to settings
        for name, entry in settings.items():
            e_enabled = entry['enabled'] if 'enabled' in entry else True
            
            if e_enabled:
                e_name  = name
                e_valid = entry['validate'] if 'validate' in entry else False
                e_func  = entry['fun'] if 'fun' in entry else None
                e_args  = entry['args']
                e_type  = entry['type']
                e_regex = e_args[0]
                e_names = e_args[1] if 1 < len(e_args) else None

                # Composes a pattern to search for elements in a document
                pattern = re.compile(e_regex)

                if e_func == CheckVHDL.locate_end:
                    for result in pattern.finditer(document):
                        data, span = e_func(document, result.span(1))
                        element = Element(e_name, span, data, e_valid, e_type)
                        self.elements[element.id] = element
                
                elif e_func == CheckVHDL.locate_in:
                    for name in e_names: 
                        prt  = settings[name]
                        patr = re.compile(prt['args'][0])

                        for res in patr.finditer(document):
                            elem_data, elem_span = CheckVHDL.locate_end(document, res.span(1))
                            
                            for res_p in pattern.finditer(elem_data):
                                data, span = (res_p.group(1), (elem_span[0] + res_p.span(1)[0], elem_span[0] + res_p.span(1)[1]))
                                element = Element(e_name, span, data, e_valid, e_type)
                                self.elements[element.id] = element
                else:
                    for result in pattern.finditer(document):
                        data, span = (result.group(1), result.span(1))
                        element = Element(e_name, span, data, e_valid, e_type)
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

                # # Looking for documentation in @param (special case for generic_param)
                # if element.name == "generic_param":
                #     parent       = self.elements[element.parent_id]
                #     grand_parent = self.elements[parent.parent_id]


        return self.elements


    def demo(self, elements):
        """Function to print demo after analysis."""

        tab_len  = 4
        elem_map = []
        demo     = []

        # Maps all elements and their boundaries
        for element in elements.values():
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
                    
                    if prev_element.type == "doc":
                        doc_bwd += 1
                    else:
                        break

                # Looking for documentation inside the element
                fwd_i = i
                while fwd_i + 1 < len(elem_map_sorted):
                    fwd_i += 1
                    next_element = elem_map_sorted[fwd_i][1]
                    
                    if next_element.type == "doc":
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

                if element.name == 'port_signal' or element.name == 'generic_param':
                    element.note = "{c0}--! Documented: {:} before, {:} inside{c1} {}".format(doc_bwd, doc_fwd, element.data, c0=element.note_color[0], c1=element.note_color[1])
                else:
                    element.note = "{c0}--! Documented: {:} before, {:} inside{c1}".format(doc_bwd, doc_fwd, c0=element.note_color[0], c1=element.note_color[1])
                # element.note = "{c0}--! Documented: {:} before, {:} inside{c1} doc_id: {}".format(doc_bwd, doc_fwd, element.doc_id, c0=element.note_color[0], c1=element.note_color[1])

        # Sets the color according to the depth of the element
        for elem in elem_map_sorted:
            element = elem[1]
            element.color[0] = self.set_text_color(0, element.depth * 80, 0)

        # Gets the object of the longest element and its length to format notes 
        element = max(elem_map, key=lambda elem: len(elem[1].end) + elem[1].depth * tab_len)[1]
        max_len = len(element.end) + element.depth * tab_len

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
                name = element.end
            
            if element.validate:
                demo.append("{}{c0}{:{w}}{c1} {}".format(tabs, name, note, w=width, c0=color0, c1=color1))
    
        return demo


    def stats(self, elements, settings):
        """Function to print statistics after analysis."""

        stats = []
        for name, elem in settings.items():
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
        """Function to print compact file analysis result."""

        elements_sorted = sorted(self.elements.items(), key=lambda item: item[1].span[0])
        # print(elements)

        compact  = []
        
        for (id, element) in elements_sorted:
            if element.name == "port_signal":
                names = []
                for i in element.doc_id:
                    names.append(elements[i].name)
                lines = self.span_to_lines(element.span, self.line_pos)
                compact.append("{} {} {} {}".format(element.name, lines, element.doc_id, names))


            if element.name == "entity":
                names = []
                for i in element.doc_id:
                    names.append(elements[i].name)
                lines = self.span_to_lines(element.span, self.line_pos)
                compact.append("{} {} {} {}".format(element.name, lines, element.doc_id, names))


            if element.name == "generic_param":
                parent       = self.elements[element.parent_id]
                grand_parent = self.elements[parent.parent_id]

                name_in_code  = element.data.split(' ')[0]

                for i in grand_parent.doc_id:
                    if elements[i].name == "@param":
                        name_in_param = elements[i].data.split(' ')[1]

                        if name_in_code.upper() == name_in_param.upper():
                            element.doc_id.append(elements[i].id)
                
                names = []
                for i in element.doc_id:
                    names.append(elements[i].name)
                lines = self.span_to_lines(element.span, self.line_pos)
                compact.append("{} {} {} {}".format(element.name, lines, element.doc_id, names))
                




        # for (id, element) in elements_sorted:
        #         compact.append("{:2} p: {:2} {:15} {}".format(element.id, element.parent_id, element.name, element.doc_id))

        return compact


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
            if not comment:
                if document[pos] == begin:
                    opened += 1
                if document[pos] == end:
                    opened -= 1
                if opened == 0:
                    break

                if document[pos: pos+2] == '--':
                    comment = True
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


