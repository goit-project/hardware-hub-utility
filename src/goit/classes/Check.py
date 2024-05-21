class Check():
    """Documentation for a class.
 
    More details.
    """
    def __init__(self, argv):
        with open(argv) as f:
            self.document = f.read()


    def analyze(self, document):
        """Function to analyze document."""
        return document


    def search(self, document):
        """Function to search special commands."""
        return document


    def result(self, document):
        """Function to make conclusions and return results."""
        return document


    def printDemo(self, args):
        """Function print out demo."""
        return args
    

    def test(self, document):
        """Simple test function."""
        return document
