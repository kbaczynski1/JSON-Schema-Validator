import sys
from scanner import *
from parser import *

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise RuntimeError("Missing input argument.")
    with open(sys.argv[1]) as file:
        input_string = file.read()

print(input_string)
scanner = Scanner(input_string)
#print(scanner.tokens)

parser = Parser(scanner)
parser.start()
