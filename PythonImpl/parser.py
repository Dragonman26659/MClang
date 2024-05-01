from rply import ParserGenerator
from PythonImpl.ast import Number, Sum, Sub, Print


class Parser():

  def __init__(self, module, builder, printf):
    self.pg = ParserGenerator([
        'NUMBER', 'PRINT', 'OPEN_PAREN', 'CLOSE_PAREN', 'SEMI_COLON', 'SUM',
        'SUB', 'VAR', 'INT', 'EQUALS', 'NUMBER_VALUE', 'CHAR', 'STRING',
        'ARRAY', 'BOOL', 'BYTEFUNCT', 'FUNCT', 'IF', 'ELSE', 'WHILE'
    ])
    self.module = module
    self.builder = builder
    self.printf = printf

  def parse(self):

    @self.pg.production(
        'program : PRINT OPEN_PAREN expression CLOSE_PAREN SEMI_COLON')
    def program(p):
      return Print(self.builder, self.module, self.printf, p[2])

    @self.pg.production('expression : expression SUM expression')
    @self.pg.production('expression : expression SUB expression')
    def expression(p):
      left = p[0]
      right = p[2]
      operator = p[1]
      if operator.gettokentype() == 'SUM':
        return Sum(self.builder, self.module, left, right)
      elif operator.gettokentype() == 'SUB':
        return Sub(self.builder, self.module, left, right)

    @self.pg.production('expression : NUMBER')
    def number(p):
      return Number(self.builder, self.module, p[0].value)

    @self.pg.production(
        'expression : VAR type IDENTIFIER EQUALS expression SEMI_COLON')
    def var_declaration(p):
      var_name = p[2]
      var_type = p[1]
      var_value = p[5]
      # Handle var declaration logic here
      return VariableDeclaration(self.builder, self.module, var_name, var_type,
                                 var_value)

    @self.pg.error
    def error_handle(token):
      raise ValueError(token)

  def get_parser(self):
    return self.pg.build()
