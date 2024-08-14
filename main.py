import parser
import lexer

#Parser(lexer.Lexer("1+1").make_tokens()).parse()

ast = parser.Parser(lexer.Lexer("(-1 - -3) * (2 + 3) / 2 + 1").make_tokens()).parse()
print (ast)
