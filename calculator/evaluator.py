import math

from calculator.stack import Stack
from calculator.converter import infix_to_postfix, is_number


def perform_operation(operator, first, second):
    if operator == "+":
        return first + second

    if operator == "-":
        return first - second

    if operator == "*":
        return first * second

    if operator == "/":
        if second == 0:
            raise ZeroDivisionError(
                "Division by zero is not allowed."
            )
        return first / second

    if operator == "%":
        if second == 0:
            raise ZeroDivisionError(
                "Modulo by zero is not allowed."
            )
        return first % second

    if operator == "^":
        result = first ** second

        if isinstance(result, complex):
            raise ValueError(
                "Complex-number results are not supported."
            )

        return result

    raise ValueError(
        f"Unsupported operator: {operator}"
    )


def evaluate_postfix(postfix_tokens):
    value_stack = Stack()

    for token in postfix_tokens:

        if is_number(token):
            value_stack.push(float(token))

        elif token in {"u+", "u-"}:
            if value_stack.size() < 1:
                raise ValueError(
                    "Invalid unary expression."
                )

            value = value_stack.pop()

            if token == "u-":
                value = -value

            value_stack.push(value)

        elif token in {"+", "-", "*", "/", "%", "^"}:
            if value_stack.size() < 2:
                raise ValueError(
                    "Invalid expression."
                )

            second_operand = value_stack.pop()
            first_operand = value_stack.pop()

            result = perform_operation(
                token,
                first_operand,
                second_operand
            )

            value_stack.push(result)

        else:
            raise ValueError(
                f"Invalid postfix token: {token}"
            )

    if value_stack.size() != 1:
        raise ValueError(
            "Invalid expression."
        )

    result = value_stack.pop()

    if not math.isfinite(result):
        raise ValueError(
            "The calculated result is too large."
        )

    if float(result).is_integer():
        return int(result)

    return round(result, 10)


def evaluate_infix(expression):
    postfix_tokens = infix_to_postfix(expression)
    result = evaluate_postfix(postfix_tokens)

    return {
        "infix": expression,
        "postfix": " ".join(postfix_tokens),
        "result": result
    }