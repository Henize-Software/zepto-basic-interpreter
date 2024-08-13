import parser
import lexer

#Parser(lexer.Lexer("1+1").make_tokens()).parse()[-1]

#the last element in the list returned is the final AST
ast = parser.Parser(lexer.Lexer("(-1 - -3) * (2 + 3) / 2 + 1").make_tokens()).parse()[-1]
print (ast)
