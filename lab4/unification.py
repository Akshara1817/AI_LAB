def is_variable(x):
    return isinstance(x, str) and x.startswith("?")

def split_args(s):
    args = []
    start = 0
    depth = 0

    for i, ch in enumerate(s):
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        elif ch == ',' and depth == 0:
            args.append(s[start:i].strip())
            start = i + 1

    args.append(s[start:].strip())
    return args


def parse(expr):
    expr = expr.strip()

    if '(' not in expr:
        return expr

    name, rest = expr.split('(', 1)
    rest = rest[:-1]

    return tuple([name.strip()] +
                 [parse(x) for x in split_args(rest)])


def apply_substitution(expr, subst):
    if is_variable(expr):
        if expr in subst:
            return apply_substitution(subst[expr], subst)
        return expr

    if isinstance(expr, tuple):
        return tuple(apply_substitution(x, subst) for x in expr)

    return expr


def occurs(var, expr, subst):
    expr = apply_substitution(expr, subst)

    if var == expr:
        return True

    if isinstance(expr, tuple):
        return any(occurs(var, x, subst) for x in expr)

    return False


def unify_terms(x, y, subst):

    x = apply_substitution(x, subst)
    y = apply_substitution(y, subst)

    if x == y:
        return True

    if is_variable(x):
        if occurs(x, y, subst):
            return False
        subst[x] = y
        return True

    if is_variable(y):
        if occurs(y, x, subst):
            return False
        subst[y] = x
        return True

    if isinstance(x, tuple) and isinstance(y, tuple):

        if x[0] != y[0] or len(x) != len(y):
            return False

        for a, b in zip(x[1:], y[1:]):
            if not unify_terms(a, b, subst):
                return False

        return True

    return False


def unify(p1, p2):

    if p1[0] != p2[0]:
        return "FAILURE"

    if len(p1) != len(p2):
        return "FAILURE"

    subst = {}

    for a, b in zip(p1[1:], p2[1:]):
        if not unify_terms(a, b, subst):
            return "FAILURE"

    if not subst:
        return "NIL"

    return subst


print("UNIFICATION ALGORITHM")

p1 = parse(input("Enter first predicate: "))
p2 = parse(input("Enter second predicate: "))

result = unify(p1, p2)

print("\nUnification Result:")

if result == "FAILURE":
    print("FAILURE")
elif result == "NIL":
    print("NIL")
else:
    for variable, value in result.items():
        print(variable, "=", value)