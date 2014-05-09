"""
@author sophie
Function to emulate Unix grep, creates a generator.
Only for strings, not regex.
"""

def grep(paths, string):
    """ Performs a search on files with given paths for a
    string. Emulates Unix grep, for strings only.
    """
    for f in paths:
        for line in open(f):
            if string in line:
                yield(f + ":" + line)
