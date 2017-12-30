
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

        tval = match_arg.group("operand%d" % x)
        
        try:

            tree.append(float(tval))

        except ValueError:

            match = regex.match(
                polish_notation, 
                tval
            )

            match_2 = regex.fullmatch(
                "(%s)" % neg, 
                regex.sub("[\(\)]", "", tval)
            )

            if match:
                tree.append(gpt(match))

            else:
                tree.append(float(match_2.group(0)))

    tree.append(match_arg.group("operator"))

    return tuple(tree)

neg = "-\d+(?:\.\d+)?"

operator = "(?P<operator>\+|\-|\/|\*|\*\*)"

operand = "(?P<operand%d>\d+\.\d+|\({}\)|\w+|(?R))+".format(neg)

polish_notation = "\( *{} *{} +{} *\)" \
    .format(operator, operand % 0, operand % 1)

def get_parse_tree(string):

    match = regex.fullmatch(polish_notation, string.replace("^", "**"))

    return gpt(match)

print(
    interpreter(
        get_parse_tree(
            "(+ (- 20.5 (-6.5)) (^ (/ 25 5) (* 1 2)))" #52
        )
    )
)
