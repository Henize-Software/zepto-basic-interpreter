import lexer

class Node:
    def __init__(self):
        pass

class NumberNode:
    def __init__(self, token_or_node) -> None:
        if isinstance(token_or_node, NumberNode):
            self.token_or_node = token_or_node.token_or_node
        else:
            self.token_or_node = token_or_node
    def __repr__(self) -> str:
        return f"n_n({self.token_or_node})"
        
    def get_pval(self):
        return self.token_or_node
    def set_pval(self, value):
        self.token_or_node = value

class BinaryOPNode: 
    def __init__(self, op_token, left_number_node, right_number_node) -> None:
        self.op_token = op_token
        self.left_number_node = left_number_node
        self.right_number_node = right_number_node
    def __repr__(self) -> str:
        return f"n_op({self.left_number_node} {self.op_token} {self.right_number_node})"
        
    def get_pval(self):
        return self.right_number_node
    def set_pval(self, value):
        self.right_number_node = value

class UnaryOPNode: 
    def __init__(self, op_token, number_node) -> None:
        self.op_token = op_token
        self.number_node = number_node

    def get_pval(self):
        return self.number_node
    def set_pval(self, value):
        self.number_node = value

class Parser: 
    tokens = []
    token_idx = -1
    current_token = None

    def __init__(self, tokens) -> None:
        self.tokens = tokens

    def parse(self) -> list:
        expression_scratch_pad = []
        while self.parse_next(expression_scratch_pad) is not None:
            pass
        print ("break")
        return expression_scratch_pad
        
    def parse_next(self, expression_scratch_pad) -> Node:
        if self.next_token() is None:
            return None
        if expression_scratch_pad is None:
            expression_scratch_pad = []
            
        if self.current_token.type == lexer.T_LPAREN:
            expression_scratch_pad.append(NumberNode(self.parse()[-1]))
        elif self.current_token.type == lexer.T_RPAREN:
            return None
        elif self.current_token.type in (lexer.T_INT, lexer.T_FLOAT):
            expression_scratch_pad.append(NumberNode(self.current_token))

        elif self.current_token.type in (lexer.T_PLUS, lexer.T_MINUS): #also handles unary op -5 + 1 or 3 + -5
            left_node = expression_scratch_pad[-1] if len(expression_scratch_pad) > 0  \
                                                              else \
                                                                 lexer.Token(lexer.T_INT, 0)
            expression_scratch_pad.append(BinaryOPNode(self.current_token,  \
                                                   NumberNode(left_node), \
                                                   self.parse_next(None)))
                    
        elif self.current_token.type in (lexer.T_DIV, lexer.T_MUL):
            expression_scratch_pad.append(BinaryOPNode(self.current_token,  \
                                                   NumberNode(expression_scratch_pad[-1].get_pval()),  \
                                                   self.parse_next(None)))
            expression_scratch_pad[-2].set_pval(expression_scratch_pad[-1])
            expression_scratch_pad.append(expression_scratch_pad[-2])
            

        return expression_scratch_pad[-1]
       
   
            
    def next_token(self):
        self.token_idx += 1
        self.current_token = self.tokens[self.token_idx] if self.token_idx < len(self.tokens) else None
        return self.current_token
    
     

#Parser(lexer.Lexer("1+1").make_tokens()).parse()

ast = Parser(lexer.Lexer("(-1 - -3) * (2 + 3) / 2 + 1").make_tokens()).parse()
print (ast)
