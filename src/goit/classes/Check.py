class Check():
    """Documentation for a class.
 
    More details.
    """
    def __init__(self, argv):
        with open(argv) as f:
            self.document = f.read()


    def analyze(self, document):
        """Function to analyze document."""
        pass
        return result


    def search(self, documet):
        """Function to search special commands."""
        pass
        return result


    def result(self, documet):
        """Function to make conclusions and return results."""
        pass
        return result
    

    def test(self, line):
        """Simple test function."""
        return self.lines[line]
