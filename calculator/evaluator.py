
import math

from calculator.stack import Stack
from calculator.converter import (
    infix_to_postfix,
    is_number,
    is_operand
)


def perform_operation(
    operator,
    first,
    second
):

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


def evaluate_postfix(
    postfix_tokens,
    variables=None
):

    value_stack = Stack()

    if variables is None:
        variables = {}

    for token in postfix_tokens:

        # -------------------------
        # Number
        # -------------------------
        if is_number(token):

            value_stack.push(
                float(token)
            )

        # -------------------------
        # Variable
        # -------------------------
        elif is_operand(token) and token not in {
            "u+",
            "u-"
        }:

            if token not in variables:

                raise ValueError(
                    f"No value provided for variable '{token}'."
                )

            value = variables[token]

            try:

                value = float(value)

            except (
                TypeError,
                ValueError
            ):

                raise ValueError(
                    f"Invalid value for variable '{token}'."
                )

            value_stack.push(value)

        # -------------------------
        # Unary operators
        # -------------------------
        elif token in {
            "u+",
            "u-"
        }:

            if value_stack.size() < 1:

                raise ValueError(
                    "Invalid unary expression."
                )

            value = value_stack.pop()

            if token == "u-":
                value = -value

            value_stack.push(value)

        # -------------------------
        # Binary operators
        # -------------------------
        elif token in {
            "+",
            "-",
            "*",
            "/",
            "%",
            "^"
        }:

            if value_stack.size() < 2:

                raise ValueError(
                    "Invalid expression."
                )

            second_operand = (
                value_stack.pop()
            )

            first_operand = (
                value_stack.pop()
            )

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

    # There should be exactly one result
    if value_stack.size() != 1:

        raise ValueError(
            "Invalid expression."
        )

    result = value_stack.pop()

    # Check infinity / overflow
    if not math.isfinite(result):

        raise ValueError(
            "The calculated result is too large."
        )

    # Return integer instead of 10.0
    if float(result).is_integer():

        return int(result)

    return round(
        result,
        10
    )


def evaluate_infix(
    expression,
    variables=None
):

    postfix_tokens = (
        infix_to_postfix(expression)
    )

    result = evaluate_postfix(
        postfix_tokens,
        variables
    )

    return {
        "infix": expression,

        "postfix":
            " ".join(postfix_tokens),

        "result": result
    }
