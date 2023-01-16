import sys
from Parser import Parser

assembly_filename = sys.argv[1]

parser = Parser(assembly_filename)
parser.create_output_file()
parser.parse()