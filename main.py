
import regex

stack = []

def interpreter(parse_tree):
    global stack

    for item in parse_tree:

        if isinstance(item, tuple):
            interpreter(item)

        else:

            if isinstance(item, str): #OPERATOR
                
                op_2 = stack.pop()
                op_1 = stack.pop()

                exec("stack.append(%s %s %s)" % (op_1, item, op_2))

            elif isinstance(item, int) or isinstance(item, float): #OPERAND
                stack.append(item)

    return stack[0]

def gpt(match_arg):
    
    tree = []

    for x in range(2):
        try:
            tree.append(float(match_arg.group("operand%d" % x)))

        except ValueError:
            match = regex.fullmatch(
                polish_notation, 
                match_arg.group("operand%d" % x)
            )

            tree.append(gpt(match))

    tree.append(match_arg.group("operator"))

    return tuple(tree)

polish_notation = " *(\( *(?P<operator>\+|\-|\/|\*|\*\*) *(?P<operand0>\d+\.\d+|\w+|(?R))+ +(?P<operand1>\d+\.\d+|\w+|(?R))+ *\)) *"

def get_parse_tree(string):

    match = regex.fullmatch(polish_notation, string.replace("^", "**"))

    return gpt(match)

print(
    interpreter(
        get_parse_tree(
            "(+ (- 20 6) (^ (/ 25 5) (* 1 2)))" #39
        )
    )
)
