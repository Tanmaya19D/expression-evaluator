from calculator.stack import Stack
from calculator.tokenizer import tokenize


PRECEDENCE = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "%": 2,
    "^": 3,
    "u+": 4,
    "u-": 4
}


RIGHT_ASSOCIATIVE = {
    "^",
    "u+",
    "u-"
}


def is_number(token):
    try:
        float(token)
        return True
    except ValueError:
        return False


def validate_token_order(tokens):
    previous_type = None
    parentheses_count = 0

    for token in tokens:
        if is_number(token):
            current_type = "number"

            if previous_type in {"number", "right_parenthesis"}:
                raise ValueError("Missing operator between values.")

        elif token == "(":
            current_type = "left_parenthesis"
            parentheses_count += 1

            if previous_type in {"number", "right_parenthesis"}:
                raise ValueError("Missing operator before '('.")

        elif token == ")":
            current_type = "right_parenthesis"
            parentheses_count -= 1

            if parentheses_count < 0:
                raise ValueError("Mismatched parentheses.")

            if previous_type in {
                None,
                "operator",
                "left_parenthesis",
                "unary"
            }:
                raise ValueError("Invalid closing parenthesis.")

        elif token in {"u+", "u-"}:
            current_type = "unary"

        elif token in {"+", "-", "*", "/", "%", "^"}:
            current_type = "operator"

            if previous_type in {
                None,
                "operator",
                "left_parenthesis",
                "unary"
            }:
                raise ValueError(
                    f"Invalid operator placement near '{token}'."
                )

        else:
            raise ValueError(f"Invalid token '{token}'.")

        previous_type = current_type

    if parentheses_count != 0:
        raise ValueError("Mismatched parentheses.")

    if previous_type in {
        "operator",
        "left_parenthesis",
        "unary"
    }:
        raise ValueError("Expression cannot end with an operator.")


def infix_to_postfix(expression):
    tokens = tokenize(expression)

    if not tokens:
        raise ValueError("Expression cannot be empty.")

    validate_token_order(tokens)

    output = []
    operator_stack = Stack()

    for token in tokens:
        if is_number(token):
            output.append(token)

        elif token == "(":
            operator_stack.push(token)

        elif token == ")":
            while (
                not operator_stack.is_empty()
                and operator_stack.peek() != "("
            ):
                output.append(operator_stack.pop())

            if operator_stack.is_empty():
                raise ValueError("Mismatched parentheses.")

            operator_stack.pop()

        elif token in PRECEDENCE:
            while (
                not operator_stack.is_empty()
                and operator_stack.peek() != "("
                and (
                    PRECEDENCE[operator_stack.peek()]
                    > PRECEDENCE[token]
                    or (
                        PRECEDENCE[operator_stack.peek()]
                        == PRECEDENCE[token]
                        and token not in RIGHT_ASSOCIATIVE
                    )
                )
            ):
                output.append(operator_stack.pop())

            operator_stack.push(token)

    while not operator_stack.is_empty():
        operator = operator_stack.pop()

        if operator in {"(", ")"}:
            raise ValueError("Mismatched parentheses.")

        output.append(operator)

    return output