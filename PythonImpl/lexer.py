from rply import LexerGenerator


class Lexer():
  def __init__(self):
      self.lexer = LexerGenerator()
  def _add_tokens(self):
      # Print
      self.lexer.add('PRINT', r'out')
      # Parenthesis
      self.lexer.add('OPEN_PAREN', r'\(')
      self.lexer.add('CLOSE_PAREN', r'\)')
      # Semi Colon
      self.lexer.add('SEMI_COLON', r'\;')
      # Operators
      self.lexer.add('SUM', r'\+')
      self.lexer.add('SUB', r'\-')
      # Number
      self.lexer.add('NUMBER', r'\d+')

  # Variables
      self.lexer.add('VAR', r'var')   
      self.lexer.add('INT', r'int')

  # Other tokens
      self.lexer.add('EQUALS', r'\=')
      self.lexer.add('NUMBER_VALUE', r'\d+')
      self.lexer.add('SEMICOLON', r'\;')
      # Ignore spaces
      self.lexer.ignore('\s+')
  def get_lexer(self):
      self._add_tokens()
      return self.lexer.build()