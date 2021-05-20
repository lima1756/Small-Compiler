# Small-Compiler
Small compiler project created for TC3048 - Compiler Design course at Tec de Monterrey

## Table of contents 

- [TODO](#TODO)
- [Project structure](#project-structure)
- [Requirements](#requirements)
- [How to run?](#how-to-run)
  - [Using main.sh script](#using-mainsh-script)
  - [Using commands directly](#using-commands-directly)
- [Libraries used](#libraries-used)
- [Tokens](#tokens)
- [Syntax specification](#syntax-specification)
- [Operator precedence](#operator-precedence)
- [Example Input](#example-input)
- [Output](#output)

## TODO

- [ ] generate ast
- [ ] simplify ast to parse tree
- [ ] verify semantics

## Project structure

```
.
├── app                     # app's source code
│   ├── lex.py              # lexer implementation using PLY
│   └── parse.py            # parser implementation using PLY
│
├── tests                   # Unit testing directory
│   └── input_tests         # directory with valid and invalid input code for testing
│
├── main.sh                 # Script para ejecutar funciones generales del proyecto
└── requirements.txt        # Lista de dependencias del proyecto (actualizar con "pip freeze > requirements.txt")

```

## Requirements

- Python3 & PIP3

## How to run?

### Using `main.sh` script

Execute main program (not doing anything yet):
`./main.sh run`

Run tests: 
`./main.sh test <extra optional parameters for pytest>`

Install requirements:
`./main.sh install`

Create python's virtual environment: 
`./main.sh env`

Source python virtual environment: 
`. ./main.sh source` or `source ./main.sh activate`

### Using commands directly

Before everything you need to install the virtual environment, this can be done with: 
`python3 -m venv env`

Once you have the env folder, every time you work with the project you need to source it first using:
`source ./env/bin/activate`

Before running any test or the main program you need to install requirements: 
`pip3 install -r requirements.txt`

To run tests:
`pytest <optional parameters for pytest>`

To run the main program (not doing anything yet):
`python3 app`


## Libraries used

- [PLY](https://www.dabeaz.com/ply/)
- [pytest](https://docs.pytest.org/en/6.2.x/)


## Tokens

| definition | Terminal  |  Regular expression |
|--|--|--|
| int declaration | INT | int |
| float declaration | FLOAT | float |
| string declaration | STRING | string |
| boolean declaration | BOOLEAN | bool |
| if reserved word | IF | if |
| else reserved word | ELSE | else |
| elif reserved word | ELIF | elif |
| while reserved word | WHILE | while |
| print reserved word | PRINT | print |
| do reserved word | DO | do |
| for reserved word | FOR | for |
| boolean value true | BOOLEAN_VALUE_T | true |
| boolean value false | BOOLEAN_VALUE_F | false |
| one character symbols | \<same as the character\> | [=+\-*/^><(){};] |
| equals | EQUALS | == |
| different | DIFFERENT | != |
| great or equal | GREAT_EQUAL | >= |
| less or equal | LESS_EQUAL | <= |
| and | AND | && |
| or | OR | \|\| |
| int value | INT_VALUE | [0-9]+ |
| float value | FLOAT_VALUE | [0-9]*\.[0-9]+ |
| string value | STRING_VALUE | ".*" |
| id | ID | [a-zA-Z]+[a-zA-Z0-9]* |


## Syntax specification

||||
|---|---|---|
| prog |  → | expression │ prog expression 
| expression |  →  |  closed_statement │  selection_statement │ iteration_statement
| selection_statement | → |  IF special_statement │ IF special_statement ELSE blocked_content │ IF special_statement elif ELSE blocked_content
| iteration_statement | → | WHILE special_statement │ DO blocked_content WHILE blocked_op ';' │ FOR '(' for_first for_second ')' blocked_content │ FOR '(' for_first for_second op_expression ')' blocked_content 
| elif | → | ELIF special_statement │ elif ELIF special_statement
| blocked_content | → | '{' prog '}'
| blocked_op | → | '(' op_expression ')'
| special_statement | → | blocked_op blocked_content
| closed_statement | → | ';' │ statement ';' 
| for_first | → | ';'  │ assign_op ';' │ declaration ';'
| for_second | → | ';'  │ op_expression ';'
| statement | → | print │ op_expression │ declaration
| print | → | PRINT '(' op_expression ')'
| declaration | → | type ID │ type assign_op
| op_expression | → | val │ assign_op │ bin_op 
| assign_op | → | ID '=' op_expression
| bin_op | → | op_expression symbol op_expression
| val | → | ID │ lit_val
| lit_val | → | INT_VALUE │ FLOAT_VALUE │ STRING_VALUE │ BOOLEAN_VALUE_T │ BOOLEAN_VALUE_F
| type | → | INT │ FLOAT │ STRING │ BOOLEAN
| symbol | → | '+' │ '-' │ '*' │ '/' │ '^' │ '>' │ '<' │ AND │ OR │ EQUALS │ DIFFERENT │ GREAT_EQUAL │ LESS_EQUAL

## Operator precedence

|precedence|associativity|operators|
|---|---|---|
|8|right|=|
|7|left|AND, OR|
|6|left|EQUALS, DIFFERENT|
|5|nonassoc|\<, \>, GREAT_EQUAL, LESS_EQUAL|
|4|left|+,-|
|3|left|*,/|
|2|left|^|
|1|nonassoc|Unary -|

## Example input:

[Code 1](https://github.com/lima1756/Small-Compiler/blob/main/tests/input_tests/ok1.txt)

[Code 2](https://github.com/lima1756/Small-Compiler/blob/main/tests/input_tests/ok2.txt)



## Output:

Currently when running the parser it generates a `parsetab.py` file, which is used by the parser in future process to accelerate it. Also it creates the `parser.out` file which describes the parser path and decision making.