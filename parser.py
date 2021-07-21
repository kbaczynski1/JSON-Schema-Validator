
class Parser:

    ##### Parser header #####

    def __init__(self, scanner):
        self.current_token_number = 0
        self.tokens = scanner.tokens
        self.token = self.next_token()
        self.flag_required = False
        self.required = []
        self.flag_properties = False
        self.flag_definitions = False
        self.definitions = []

    def next_token(self):
        self.current_token_number += 1
        if self.current_token_number - 1 < len(self.tokens):
            return self.tokens[self.current_token_number - 1]
        else:
            raise RuntimeError("Error: No more tokens")

    def take_token(self, token_type):
        if self.token.type != token_type:
            self.error("Unexpected token: %s, expected token is: %s" % (self.token.type, token_type))
        if token_type != "EOF":
            self.token = self.next_token()

    def error(self, msg):
        raise RuntimeError("Parser error, %s, line %d" % (msg, self.token.line))

    ##### Parser body #####

    # Starting symbol
    def start(self):
        # start -> OCB program CCB EOF
        self.take_token('OCB')
        self.program()
        self.take_token('CCB')
        self.take_token('EOF')
        if self.check_definitions_and_required():
            print("\nJSON Schema: OK")

    def program(self):
        # program -> start_statement program
        if self.token.type == "QUOTES":
            self.start_statement()
            self.program()
        # program -> eps
        else:
            pass

    def start_statement(self):
        # start_statement -> QUOTES statement statement_cont
        self.take_token("QUOTES")
        self.statement()
        self.statement_cont()

    def statement(self):
        # statement -> id_stmt
        if self.token.type == "$ID":
            self.id_stmt()
        # statement -> schema_stmt
        elif self.token.type == "$SCHEMA":
            self.schema_stmt()
        # statement -> title_stmt
        elif self.token.type == "TITLE":
            self.title_stmt()
        # statement -> required_stmt
        elif self.token.type == "REQUIRED":
            self.required_stmt()
        # statement -> type_stmt
        elif self.token.type == "TYPE":
            self.type_stmt()
        # statement -> properties_stmt
        elif self.token.type == "PROPERTIES":
            self.properties_stmt()
        # statement -> string_stmt
        elif self.token.type == "STRING":
            self.string_stmt()
        # statement -> description_stmt
        elif self.token.type == "DESCRIPTION":
            self.description_stmt()
        # statement -> min_max_stmt
        elif self.token.type == "MINIMUM" or self.token.type == "MAXIMUM":
            self.min_max_stmt()
        # statement -> enum_stmt
        elif self.token.type == "ENUM":
            self.enum_stmt()
        # statement -> ref_stmt
        elif self.token.type == "$REF":
            self.ref_stmt()
        # statement -> definitions_stmt
        elif self.token.type == "DEFINITIONS":
            self.definitions_stmt()
        # statement -> min_max_length_stmt
        elif self.token.type == self.token.type == "MINLENGTH" or self.token.type == "MAXLENGTH":
            self.min_max_length_stmt()
        else:
            self.error("Epsilon not allowed")

    def statement_cont(self):
        # statement_cont -> COMMA QUOTES statement statement_cont
        if self.token.type == "COMMA":
            self.take_token("COMMA")
            self.take_token("QUOTES")
            self.statement()
            self.statement_cont()
        # statement_cont -> eps
        else:
            pass

    def id_stmt(self):
        # id_stmt -> $ID qcq_stmt STRING QUOTES
        self.take_token("$ID")
        self.qcq_stmt()
        self.take_token("STRING")
        self.take_token("QUOTES")
        print("id_stmt: OK")

    def schema_stmt(self):
        # schema_stmt -> SCHEMA qcq_stmt STRING QUOTES
        self.take_token("$SCHEMA")
        self.qcq_stmt()
        self.take_token("STRING")
        self.take_token("QUOTES")
        print("schema_stmt: OK")

    def title_stmt(self):
        # title_stmt -> TITLE qcq_stmt STRING QUOTES
        self.take_token("TITLE")
        self.qcq_stmt()
        self.take_token("STRING")
        self.take_token("QUOTES")
        print("title_stmt: OK")

    def required_stmt(self):
        # required_stmt -> REQUIRED qc_stmt string_array
        self.flag_required = True
        self.take_token("REQUIRED")
        self.qc_stmt()
        self.string_array()
        self.flag_required = False
        print("required_stmt: OK")

    def type_stmt(self):
        # type_stmt -> TYPE qc_stmt type_element
        self.take_token("TYPE")
        self.qc_stmt()
        self.type_element()
        print("type_stmt: OK")

    def properties_stmt(self):
        # properties_stmt -> PROPERTIES qc_stmt order_in_CB
        self.flag_properties = True
        self.take_token("PROPERTIES")
        self.qc_stmt()
        self.order_in_CB()
        self.flag_properties = False
        print("properties_stmt: OK")

    def string_stmt(self):
        # string_stmt -> STRING qc_stmt value |
        # STRING qc_stmt OSB any_type_array | STRING qc_stmt OCB object
        self.take_token("STRING")
        self.qc_stmt()
        if self.token.type == "SIGN" or self.token.type == "QUOTES" or self.token.type == "INTEGER" \
                or self.token.type == "NUMBER" or self.token.type == "FALSE" or self.token.type == "TRUE":
            self.value()
        elif self.token.type == "OSB":
            self.any_type_array()
        elif self.token.type == "OCB":
            self.object()
        else:
            self.error("%s is not an expected string_stmt" % self.token.type)
        print("string_stmt: OK")

    def description_stmt(self):
        # description_stmt -> DESCRIPTION qcq_stmt STRING QUOTES
        self.take_token("DESCRIPTION")
        self.qcq_stmt()
        self.take_token("STRING")
        self.take_token("QUOTES")
        print("description_stmt: OK")

    def min_max_stmt(self):
        # min_max_stmt -> min_max qc_stmt SIGN number | min_max qc_stmt number
        self.min_max()
        self.qc_stmt()
        if self.token.type == "SIGN":
            self.take_token("SIGN")
        self.number()
        print("min_max_stmt: OK")

    def enum_stmt(self):
        # enum_stmt -> ENUM qc_stmt any_type_array
        self.take_token("ENUM")
        self.qc_stmt()
        self.any_type_array()
        print("enum_stmt: OK")

    def ref_stmt(self):
        # ref_stmt -> $REF qcq_stmt REF QUOTES
        self.take_token("$REF")
        self.qcq_stmt()
        if self.token.type == "REF":
            splitted_token_value = self.token.value.split("/")
            if splitted_token_value[1] == "definitions":
                if splitted_token_value[2] not in self.definitions:
                    self.definitions.append(splitted_token_value[2])
        self.take_token("REF")
        self.take_token("QUOTES")
        print("ref_stmt: OK")

    def definitions_stmt(self):
        # definitions_stmt -> DEFINITIONS qc_stmt order_in_CB
        self.flag_definitions = True
        self.take_token("DEFINITIONS")
        self.qc_stmt()
        self.order_in_CB()
        self.flag_definitions = False
        print("definitions_stmt: OK")

    def min_max_length_stmt(self):
        # min_max_length_stmt -> min_max_length qc_stmt INTEGER
        self.min_max_length()
        self.qc_stmt()
        self.take_token("INTEGER")
        print("min_max_length_stmt: OK")

    def qcq_stmt(self):
        # qcq_stmt -> QUOTES COLON QUOTES
        self.take_token("QUOTES")
        self.take_token("COLON")
        self.take_token("QUOTES")

    def qc_stmt(self):
        # qc_stmt -> QUOTES COLON
        self.take_token("QUOTES")
        self.take_token("COLON")

    def string_array(self):
        # string_array -> OSB string string_array_cont CSB | OSB CSB
        self.take_token("OSB")
        if self.token.type == "QUOTES":
            self.string()
            self.string_array_cont()
        self.take_token("CSB")

    def string_array_cont(self):
        # string_array_cont -> COMMA string string_array_cont
        if self.token.type == "COMMA":
            self.take_token("COMMA")
            self.string()
            self.string_array_cont()
        # string_array_cont -> eps
        else:
            pass

    def type_element(self):
        # type_element -> type_string
        if self.token.type == "QUOTES":
            self.type_string()
        # type_element -> type_array
        elif self.token.type == "OSB":
            self.type_array()
        else:
            self.error("%s is not an expected type_element" % self.token.type)

    def order_in_CB(self):
        # order_in_CB -> OCB string COLON object order_in_CB_cont CCB
        self.take_token("OCB")
        self.string()
        self.take_token("COLON")
        self.object()
        self.order_in_CB_cont()
        self.take_token("CCB")

    def order_in_CB_cont(self):
        # order_in_CB_cont -> COMMA string COLON object order_in_CB_cont
        if self.token.type == "COMMA":
            self.take_token("COMMA")
            self.string()
            self.take_token("COLON")
            self.object()
            self.order_in_CB_cont()
        # order_in_CB_cont -> eps
        else:
            pass

    def value(self):
        # value -> SIGN number
        if self.token.type == "SIGN":
            self.take_token("SIGN")
            self.number()
        # value -> number
        elif self.token.type == "INTEGER" or self.token.type == "NUMBER":
            self.number()
        # value -> string
        elif self.token.type == "QUOTES":
            self.string()
        # value -> boolean
        elif self.token.type == "FALSE" or self.token.type == "TRUE":
            self.boolean()
        else:
            self.error("%s is not an expected value" % self.token.type)

    def any_type_array(self):
        # any_type_array -> OSB value any_type_array_cont CSB | OSB CSB
        self.take_token("OSB")
        if self.token.type == "SIGN" or self.token.type == "QUOTES" \
                or self.token.type == "INTEGER" or self.token.type == "NUMBER":
            self.value()
            self.any_type_array_cont()
        self.take_token("CSB")

    def any_type_array_cont(self):
        # any_type_array_cont -> COMMA value any_type_array_cont
        if self.token.type == "COMMA":
            self.take_token("COMMA")
            self.value()
            self.any_type_array_cont()
        # any_type_array_cont -> eps
        else:
            pass

    def object(self):
        # object -> OCB program CCB | OCB CCB
        self.take_token("OCB")
        if self.token.type == "QUOTES":
            self.program()
        self.take_token("CCB")

    def min_max(self):
        # min_max -> MINIMUM
        if self.token.type == "MINIMUM":
            self.take_token("MINIMUM")
        # min_max -> MAXIMUM
        else:
            self.take_token("MAXIMUM")

    def min_max_length(self):
        # min_max_length -> MINLENGTH
        if self.token.type == "MINLENGTH":
            self.take_token("MINLENGTH")
        # min_max_length -> MAXLENGTH
        else:
            self.take_token("MAXLENGTH")

    def number(self):
        # number -> NUMBER
        if self.token.type == "NUMBER":
            self.take_token("NUMBER")
        # number -> INTEGER
        elif self.token.type == "INTEGER":
            self.take_token("INTEGER")
        else:
            self.error("%s is not an expected number" % self.token.type)

    def string(self):
        # string -> QUOTES keyword QUOTES | QUOTES STRING QUOTES | QUOTES type QUOTES | QUOTES QUOTES
        self.take_token("QUOTES")
        if self.token.type == "$ID" or self.token.type == "$SCHEMA" or self.token.type == "TITLE" \
                or self.token.type == "TYPE" or self.token.type == "PROPERTIES" or self.token.type == "DESCRIPTION" \
                or self.token.type == "REQUIRED" or self.token.type == "MINIMUM" or self.token.type == "MAXIMUM" \
                or self.token.type == "MINLENGTH" or self.token.type == "MAXLENGTH" or self.token.type == "ENUM" \
                or self.token.type == "DEFINITIONS" or self.token.type == "$REF":
            self.keyword()
        elif self.token.type == "STRING":
            if self.flag_definitions:
                if self.token.value in self.definitions:
                    self.definitions.remove(self.token.value)
            if self.flag_required:
                self.required.append(self.token.value)
            if self.flag_properties:
                if len(self.required) > 0:
                    try:
                        self.required.remove(self.token.value)
                    except:
                        pass
            self.take_token("STRING")
        elif self.token.type == "ARR_TYPE" or self.token.type == "BOOL_TYPE" or self.token.type == "OBJ_TYPE" or \
                self.token.type == "NULL_TYPE" or self.token.type == "NUM_TYPE" or self.token.type == "INT_TYPE" or \
                self.token.type == "STR_TYPE":
            self.type()
        self.take_token("QUOTES")

    def type_string(self):
        # type_string -> QUOTES type QUOTES
        self.take_token("QUOTES")
        self.type()
        self.take_token("QUOTES")

    def type_array(self):
        # type_array -> OSB type_string type_array_cont CSB
        self.take_token("OSB")
        self.type_string()
        self.type_array_cont()
        self.take_token("CSB")

    def type_array_cont(self):
        # type_array_cont -> COMMA type_string type_array_cont
        if self.token.type == "COMMA":
            self.take_token("COMMA")
            self.type_string()
            self.type_array_cont()
        # type_array_cont -> eps
        else:
            pass

    def boolean(self):
        # boolean -> FALSE
        if self.token.type == "FALSE":
            self.take_token("FALSE")
        # boolean -> TRUE
        else:
            self.take_token("TRUE")

    def keyword(self):
        # keyword -> $ID
        if self.token.type == "$ID":
            self.take_token("$ID")
        # keyword -> $SCHEMA
        elif self.token.type == "$SCHEMA":
            self.take_token("$SCHEMA")
        # keyword -> TITLE
        elif self.token.type == "TITLE":
            self.take_token("TITLE")
        # keyword -> TYPE
        elif self.token.type == "TYPE":
            self.take_token("TYPE")
        # keyword -> PROPERTIES
        elif self.token.type == "PROPERTIES":
            self.take_token("PROPERTIES")
        # keyword -> DESCRIPTION
        elif self.token.type == "DESCRIPTION":
            self.take_token("DESCRIPTION")
        # keyword -> REQUIRED
        elif self.token.type == "REQUIRED":
            self.take_token("REQUIRED")
        # keyword -> min_max
        elif self.token.type == "MINIMUM" or self.token.type == "MAXIMUM":
            self.min_max()
        # keyword -> min_max_length
        elif self.token.type == "MINLENGTH" or self.token.type == "MAXLENGTH":
            self.min_max_length()
        # keyword -> ENUM
        elif self.token.type == "ENUM":
            self.take_token("ENUM")
        # keyword -> DEFINITIONS
        elif self.token.type == "DEFINITIONS":
            self.take_token("DEFINITIONS")
        # keyword -> $REF
        elif self.token.type == "$REF":
            self.take_token("$REF")
        else:
            self.error("%s is not an expected keyword" % self.token.type)

    def type(self):
        # type -> ARR_TYPE
        if self.token.type == "ARR_TYPE":
            self.take_token("ARR_TYPE")
        # type -> BOOL_TYPE
        elif self.token.type == "BOOL_TYPE":
            self.take_token("BOOL_TYPE")
        # type -> OBJ_TYPE
        elif self.token.type == "OBJ_TYPE":
            self.take_token("OBJ_TYPE")
        # type -> NULL_TYPE
        elif self.token.type == "NULL_TYPE":
            self.take_token("NULL_TYPE")
        # type -> NUM_TYPE
        elif self.token.type == "NUM_TYPE":
            self.take_token("NUM_TYPE")
        # type -> INT_TYPE
        elif self.token.type == "INT_TYPE":
            self.take_token("INT_TYPE")
        # type -> STR_TYPE
        elif self.token.type == "STR_TYPE":
            self.take_token("STR_TYPE")
        else:
            self.error("%s is not an expected type" % self.token.type)

    def check_definitions_and_required(self):
        if len(self.definitions) > 0:
            print("The following definitions are missing:")
            for definition in self.definitions:
                print(definition)
            return False
        if len(self.required) > 0:
            print("The following instantces are required:")
            for arg in self.required:
                print(arg)
            return False
        return True
