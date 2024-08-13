DIGITS = '0123456789'

T_INT    = 'INT'
T_FLOAT  = 'FLOAT'
T_PLUS   = 'PLUS'
T_MINUS  = 'MINUS'
T_MUL    = 'MUL'
T_DIV    = 'DIV'
T_LPAREN = 'LPAREN'
T_RPAREN = 'RPAREN'

class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
    def __repr__(self):
       return f"T({self.type}, {self.value})"   

TokensStrings = {
    '+': T_PLUS,
    '-': T_MINUS,
    '*': T_MUL,
    '/': T_DIV,
    '(': T_LPAREN,
    ')': T_RPAREN
}

class Lexer: 
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.next_char = text[self.pos] if text != '' else None
   
    def next(self):
        self.pos += 1
        self.next_char = self.text[self.pos] \
                         if self.pos < len(self.text) \
                         else None
        
    def parse_number(self) -> Token:
        is_float = False
        num_str = ''
        while (self.next_char is not None and 
               self.next_char in (*DIGITS, '.')):
            if self.next_char == '.':
                is_float = True
                num_str += '.'
            else:
                num_str += self.next_char
            self.next()
            
        return Token(T_FLOAT, float(num_str)) if is_float \
          else Token(T_INT,   int  (num_str)) 
            

    def make_tokens(self) -> list:
        tokens = []
        while self.next_char != None:
            if self.next_char in ' \t':
                self.next()
                continue
            elif self.next_char in DIGITS:
                tokens.append(self.parse_number())
            else:
                tokens.append(Token(TokensStrings[self.next_char]))
                self.next()
        return tokens


