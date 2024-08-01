class Check():
    """Documentation for a class.
 
    More details.
    """
    file_path = ""
    config    = []
    document  = ""
    elements  = {}
    line_pos  = []

    def __init__(self, file_path, config):
        """The constructor."""
        self.file_path = file_path
        self.config    = config

        # Reading a file for analysis
        with open(file_path) as f:
            self.document = f.read()

        # Get all '\n' positions
        self.line_pos = []
        for i, symbol in enumerate(self.document):
            if symbol == '\n':
                self.line_pos.append(i)


    def analyze(self, document, config):
        """Function to analyze document."""
        elements = {}
        return elements
    

    def demo(self, elements):
        """Function print out demo."""
        demo = []
        return demo
    
    
    def stats(self):
        """Function print out statistics."""
        stats = []
        return stats
    

    def compact(self, elements):
        """Function to print compact file analysis result."""
        compact = []
        return compact


    def search(self, document):
        """Function to search special commands."""
        return document


    def result(self, document):
        """Function to make conclusions and return results."""
        return document
    

    def test(self, document):
        """Simple test function."""
        return document
