#created 2024 Joshua Henize
import lexer

class Node:
    token_or_node = None
    def __init__(self):
        pass
    def get_pval(self):
        return self.token_or_node
    def set_pval(self, value):
        self.token_or_node = value

class NumberNode(Node):
    def __init__(self, token_or_node) -> None:
        if isinstance(token_or_node, NumberNode):
            self.token_or_node = token_or_node.token_or_node
        else:
            self.token_or_node = token_or_node
    def __repr__(self) -> str:
        return f"n_n({self.token_or_node})"
    
class BinaryOPNode(Node): 
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

class Parser: 
    tokens = []
    token_idx = -1
    current_token = None

    def __init__(self, tokens) -> None:
        self.tokens = tokens

    def parse(self) -> list:
        expr_buff = []
        while self.parse_next(expr_buff) is not None:
            pass
        print ("break")
        return expr_buff[-1]
        
    def parse_next(self, expr_buff) -> Node:
        if self.next_token() is None:
            return None
        if expr_buff is None:
            expr_buff = []
            
        if self.current_token.type == lexer.T_LPAREN:
            expr_buff.append(NumberNode(self.parse()))
        elif self.current_token.type == lexer.T_RPAREN:
            return None
        elif self.current_token.type in (lexer.T_INT, lexer.T_FLOAT):
            expr_buff.append(NumberNode(self.current_token))
        
        #also handles unary op -5 + 1 or 3 + -5
        elif self.current_token.type in (lexer.T_PLUS, lexer.T_MINUS): 
            if len(expr_buff) > 0:
                left_node = expr_buff[-1]
            else:
                left_node = lexer.Token(lexer.T_INT, 0)
            new_node = BinaryOPNode(self.current_token,  \
                                    NumberNode(left_node),\
                                    self.parse_next(None))
            expr_buff.append(new_node)
                    
        elif self.current_token.type in (lexer.T_DIV, lexer.T_MUL):
            new_node = BinaryOPNode(self.current_token,  \
                                    NumberNode(expr_buff[-1].get_pval()),  \
                                    self.parse_next(None))
            expr_buff.append(new_node)
            expr_buff[-2].set_pval(expr_buff[-1])
            expr_buff.append(expr_buff[-2])
            

        return expr_buff[-1]

    def next_token(self):
        self.token_idx += 1
        self.current_token = self.tokens[self.token_idx] if self.token_idx < len(self.tokens) else None
        return self.current_token
    
