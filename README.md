Projekt wykonali:

Edward Sucharda 284388

Kacper Baczyński 276409

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

by uruchomić projekt należy wpisać komendęw terminalu:


python validator.py exampleFile.txt



^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Gramatyka BNF:






SYMBOL | WYRAŻENIE
:-|:-
start |	OCB program CCB EOF
program	| start_statement program
| | eps
start_statement | QUOTES statement statement_cont
statement | id_stmt
| | schema_stmt
| | title_stmt
| | required_stmt
| | type_stmt
| | propertioes_stmt
| | string_stmt
| | description_stmt
| | min_max_stmt
| | enum_stmt
| | ref_stmt
| | definitions_stmt
| | min_max_length_stmt
statement_cont | COMMA QUOTES statement statement_cont
| | eps
id_stmt	| $ID qcq_stmt STRING QUOTES
schema_stmt | $SCHEMA qcq_stmt STRING QUOTES
title_stm |TITLE qcq_stmt STRING QUOTES
requaired_stmt |REQUAIRED qc_stmt string_array
type_stmt | TYPE qc_stmt type_element
properties_stmt	| PROPERTIES qc_stmt order_in_CB
string_stmt | STRING qc_stmt value
| | STRING qc_stmt OSB any_type_array
| | STRING qc_stmt OCB object
description_stmt | DESCRIPTION qcq_stmt STRING QUOTES
min_max_stmt | min_max qc_stmt SIGN number
| | min_max qc_stmt number
enum_stmt | ENUM qc_stmt any_type_array
ref_stmt | $REF qcq_stmt REF QUOTES
definitions_stmt | DEFINITIONS qc_stmt order_in_CB
min_max_lenhth_stmt | min_max_length qc_stmt INTEGER
qcq_stmt | QUOTES COLON QUOTES
qc_stmt | QUOTES COLON
string_array | OSB string string_array_cont CSB
| | OSB CSB			
string_array_cont | COMMA string string_array_cont
| | eps
type_element | type_string
| | type_array
order_in_CB | OCB string COLON object order_in_CB_cont CCB
order_in_CB_cont | COMMA string COLON object order_in_CB_cont
| | eps
value | SIGN number
| | number
| | string
| | boolen
any_type_array | OSB value any_type_array_cont CSB
| | OSB CSB
any_type_array_cont | COMMA value any_type_array_cont
| | eps
object | OCB program CCB
| | OCB CCB
min_max	| MINIMUM
| | MAXIMUM
min_max_length | MINLENGTH
| | MAXLENGTH
number | NUMBER
| | INTEGER
string | QUOTES keyword QUOTES
| | QUOTES STRING QUOTES
| | QUOTES type QUOTES
| | OUTES QUOTES
type_string| QUOTES type QUOTES
type_array | OSB type_string type_array_cont CSB
type_array_cont | COMMA type_string type_array_cont
| | eps
boolen	| FALSE
| | TRUE
keyword | $ID
| | $SCHEMA
| | TITLE
| | TYPE
| | PROPERTIES
| | DESCRIPTION
| | REQUIRED
| | min_max
| | min_max_length
| | ENUM
| | DEFINITIONS
| | $REF
type | ARR_TYPE
| | BOOL_TYPE
| | OBJ_TYPE
| | NULL_TYPE
| | NUM_TYPE
| | INT_TYPE
| | STR_TYPE
