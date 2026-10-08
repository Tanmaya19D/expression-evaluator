def tokenize(expression):
    tokens = []
    number = ""
    i = 0

    while i < len(expression):
        character = expression[i]

        if character.isspace():
            i += 1
            continue

        if character.isdigit() or character == ".":
            number += character

            if number.count(".") > 1:
                raise ValueError("Invalid number: multiple decimal points.")

        else:
            if number:
                tokens.append(number)
                number = ""

            if character in "+-*/%^()":
                tokens.append(character)
            else:
                raise ValueError(
                    f"Invalid character '{character}' in expression."
                )

        i += 1

    if number:
        tokens.append(number)

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