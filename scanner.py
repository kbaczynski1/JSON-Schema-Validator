import collections
import re

Token = collections.namedtuple("Token", ["type", "value", "line", "column"])

class Scanner:

    def __init__(self, input_string):
        self.tokens = []
        for token in self.tokenize(input_string):
            self.tokens.append(token)

    def tokenize(self, input_string):
        keywords = {"$id", "$schema", "title", "type", "properties", "description", "required", "minimum", "maximum",
                    "minLength", "maxLength", "enum", "definitions", "$ref"}
        token_specification = [
            ('OCB',     '\{'),                    # OPENING CURLY BRACKET
            ('CCB',     '\}'),                    # CLOSING CURLY BRACKET
            ('OSB',     '\['),                    # OPENING SQUARE BRACKET
            ('CSB',     '\]'),                    # CLOSING SQUARE BRACKET
            ('COLON',   ':'),                     # COLON
            ('COMMA',   ','),                     # COMMA
            ('REF',     '"#/definitions/(.+?)"'), # REF
            ('STRING',  '"(.+?)"'),               # STRING
            ('SIGN', '[+-]'),                     # SIGN
            ('INTEGER', '\d+'),                   # INTEGER
            ('NUMBER', '[+-]?\d+\.\d+'),          # NUMBER
            ('NEWLINE', '\n'),                    # Line endings
            ('SKIP',    '[ \t]'),                 # Skip over spaces and tabs
            ('FALSE', 'false'),                   # FALSE
            ('TRUE', 'true'),                     # TRUE
        ]
        types = {
            "string" :  "STR_TYPE",
            "number" :  "NUM_TYPE",
            "integer" : "INT_TYPE",
            "boolean" : "BOOL_TYPE",
            "null" :    "NULL_TYPE",
            "object" :  "OBJ_TYPE",
            "array" :   "ARR_TYPE"
        }
        token_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        get_token = re.compile(token_regex).match
        line_number = 1
        current_position = line_start = 0
        match = get_token(input_string)
        while match is not None:
            type = match.lastgroup
            #print(type)
            if type == 'NEWLINE':
                line_start = current_position
                line_number += 1
            elif type != 'SKIP':
                value = match.group(type).strip("\"")
                #print(value)
                if type == "STRING" or type == "REF":
                    yield Token("QUOTES", "\"", line_number, match.start()-line_start)
                    if value in keywords:
                        type = value.upper()
                    if value in types.keys():
                        type = types[value]
                    yield Token(type, value, line_number, match.start()-line_start+1)
                    yield Token("QUOTES", "\"", line_number, match.end()-(line_start+1))
                else:
                    yield Token(type, value, line_number, match.start()-line_start)
            current_position = match.end()
            match = get_token(input_string, current_position)
        if current_position != len(input_string):
            raise RuntimeError('Error: Unexpected character %r on line %d' % (input_string[current_position], line_number))
        yield Token('EOF', '', line_number, current_position-line_start)

'''
if __name__ == "__main__":
    with open("exampleFile.txt") as file:
        input_string = file.read()
        scann = Scanner(input_string)
        print(scann.tokens)
    pass
'''
