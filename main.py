
import lark

stack = []

#uses the converted parse tree as a guide to calculate the polish notation's result, and returns that.(FLOAT)
def interpreter(parse_tree):
    global stack

    for item in parse_tree:

        if isinstance(item, tuple): #PARSE_TREE/EXPRESSION
            interpreter(item)

        elif isinstance(item, str): #OPERATOR

            op_2 = stack.pop()
            op_1 = stack.pop()

            exec("stack.append(%s %s %s)" % (op_1, item, op_2))

        elif isinstance(item, float): #OPERAND
            stack.append(item)

    return stack[0]

#to convert the parse tree into a usable format.
class tran(lark.Transformer):

    def signed(self, n):
        return float(n[0])

    def unsigned(self, n):
        return float(n[0][1:-1])

    def operator(self, n):
        return str(n[0])

    expr = tuple

    operand = lambda _, n: n[0]
    num     = lambda _, n: n[0]

#for reversing the polish notation so that it's able to be interpreted by the interpreter(parse_tree) function.
def gpt(match):

    tree = []

    for x in range(2):

        tval = match[x + 1]

        if isinstance(tval, float):
            tree.append(tval)

        else:
            tree.append(gpt(tval))

    tree.append(match[0])

    return tuple(tree)

def get_parse_tree(pn_expr):
    return pn_parser.parse(pn_expr.replace("^", "**"))

def convert(a):
    return gpt(tran().transform(a))

with open("grammar.ebnf") as file:
    pn_grammar = r''.join([line for line in file])

pn_parser = lark.Lark(
    pn_grammar, 
    start  = "expr", 
    parser = "lalr"
)

if __name__ == "__main__":
    print(
        interpreter(
            convert(
                get_parse_tree(
                    "(+ (- 20.5 (-6.5)) (^ (/ 25 5) (* 1 2)))"
                )
            )
        )
    )
