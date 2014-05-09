"""
Convert files from from_format to to_format.
"""
import argparse
from functools import partial
import sys
from collections import Counter

from declass.utils import filefilter, text_processors, nlp


def _cli():
    # Text to display after help
    epilog = """
    EXAMPLES

    Convert mydata-vw to mydata-svmlight
    $ python format_converter.py -f vw -t svmlight mydata-vw > mydata-svmlight 

    Put in a pipeline with files_to_vw.py
    $ python files_to_vw.py --base_path=mydata \
        | python format_converter.py -f vw -t svmlight > mydata-svmlight
    """
    parser = argparse.ArgumentParser(
        description=globals()['__doc__'], epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
        help='Convert infile rather than reading from sys.stdin'
        )
    parser.add_argument(
        '-o', '--outfile', default=sys.stdout,
        type=argparse.FileType('w'),
        help='Write to OUT_FILE rather than sys.stdout.')
    parser.add_argument(
        '-f', '--from_format', required=True,
        help="input file should be in this format.  One of 'vw', 'svmlight'!")
    parser.add_argument(
        '-t', '--to_format', required=True,
        help="output will be in this format.  One of 'vw', 'svmlight'")

    # Parse and check args
    args = parser.parse_args()

    # Call the module interface
    convert(args.infile, args.outfile, args.from_format, args.to_format)


def convert(infile, outfile, from_format, to_format):
    """
    Write later if module interface is needed. See _cli for the documentation.
    """
    # Select the from and to formatters
    tp = text_processors
    formatter_dict = {'vw': tp.VWFormatter, 'svmlight': tp.SVMLightFormatter}

    from_formatter = formatter_dict[from_format]()
    to_formatter = formatter_dict[to_format]()

    for line in infile:
        line = line.rstrip('\n').rstrip('\r')
        line_dict = from_formatter.get_dict(line)
        output = to_formatter.get_sstr(**line_dict)

        outfile.write(output + '\n')



if __name__ == '__main__':
    _cli()

