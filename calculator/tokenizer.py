
def tokenize(expression):
    tokens = []
    i = 0

    while i < len(expression):
        character = expression[i]

        # Ignore spaces
        if character.isspace():
            i += 1
            continue

        # -------------------------
        # Numbers
        # -------------------------
        if character.isdigit() or character == ".":
            number = character
            i += 1

            while i < len(expression):
                current = expression[i]

                if current.isdigit() or current == ".":
                    number += current
                    i += 1
                else:
                    break

            if number.count(".") > 1:
                raise ValueError(
                    "Invalid number: multiple decimal points."
                )

            if number == ".":
                raise ValueError(
                    "Invalid number: '.'."
                )

            tokens.append(number)
            continue

        # -------------------------
        # Variables / identifiers
        # -------------------------
        if character.isalpha() or character == "_":
            identifier = character
            i += 1

            while i < len(expression):
                current = expression[i]

                if current.isalnum() or current == "_":
                    identifier += current
                    i += 1
                else:
                    break

            tokens.append(identifier)
            continue

        # -------------------------
        # Operators / parentheses
        # -------------------------
        if character in "+-*/%^()":
            tokens.append(character)
            i += 1
            continue

        # -------------------------
        # Invalid character
        # -------------------------
        raise ValueError(
            f"Invalid character '{character}' in expression."
        )

    return handle_unary_minus(tokens)


def handle_unary_minus(tokens):
    processed_tokens = []

    for index, token in enumerate(tokens):

        if token == "-":
            if (
                index == 0
                or tokens[index - 1] in "+-*/%^("
            ):
                processed_tokens.append("u-")

            else:
                processed_tokens.append("-")

        else:
            processed_tokens.append(token)

    return processed_tokens
