
import regex

stack = []

#uses the "parse tree" as a guide to calculate the polish notation's result, and returns that.(FLOAT)
def interpreter(parse_tree):
    global stack

    for item in parse_tree:

        if isinstance(item, tuple):
            interpreter(item)

        elif isinstance(item, str): #OPERATOR

            op_2 = stack.pop()
            op_1 = stack.pop()

            exec("stack.append(%s %s %s)" % (op_1, item, op_2))

        elif isinstance(item, float): #OPERAND
            stack.append(item)

    return stack[0]

#returns "parse tree" of which consists of tuples, 
#    detailing the information in the polish notation expression in an easier format for the interpreter to work with.
def gpt(match_arg):
    
    tree = []

    for x in range(2):

        tval = match_arg.group("operand%d" % x)

        try:

            tree.append(float(tval))

        except ValueError:

            match = regex.search(
                expression, 
                tval
            )

            match_2 = regex.search( #just in case the expression turns out to be a negative number.
                "(%s)" % neg, 
                regex.sub("[\(\)]", "", tval)
            )

            if match:
                tree.append(gpt(match))

            else:
                tree.append(float(match_2.group(0)))

    tree.append(match_arg.group("operator"))

    return tuple(tree)

#extra-step between user and regex/gpt, by having that handled here, returning from gpt.
def get_parse_tree(pn_expr):

    match = regex.search(
        expression, 
        regex.sub(
            "[A-z_:]+", 
            "", 
            pn_expr.replace("^", "**")
        )
    )

    return gpt(match)


neg = "-\d+(?:\.\d+)?" # used in negative number declaration

operator = "(?P<operator>\+|\-|\/|\*|\*\*)" #add, sub, div, mul, pwr

operand = "(?P<operand%d>\d+\.\d+|\({}\)|\w+|(?R))+".format(neg) #a positive number declaration, a negative number declaration, or another expression.

expression = " *\( *{} *{} +{} *\) *" \
    .format(operator, operand % 0, operand % 1) #the finished product. this contains everything to parse the normal polish notation expression.

print(
    interpreter(
        get_parse_tree(
            "(+ (- 20.5 (-6.5)) (^ (/ 25 5) (* 1 2)))" #52
        )
    )
)
