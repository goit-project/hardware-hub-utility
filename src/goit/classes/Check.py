class Check():
    """Documentation for a class.
 
    More details.
    """
    file_path = ""
    settings  = []
    document  = ""
    elements  = {}
    line_pos  = []

    def __init__(self, file_path, settings):
        """The constructor."""
        self.file_path = file_path
        self.settings  = settings

        # Reading a file for analysis
        with open(file_path) as f:
            self.document = f.read()

        # Get all '\n' positions
        self.line_pos = []
        for i, symbol in enumerate(self.document):
            if symbol == '\n':
                self.line_pos.append(i)


    def analyze(self, document, settings):
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


    def search(self, document):
        """Function to search special commands."""
        return document


    def result(self, document):
        """Function to make conclusions and return results."""
        return document
    

    def test(self, document):
        """Simple test function."""
        return document
