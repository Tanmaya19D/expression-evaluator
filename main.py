from converter import infix_to_postfix
from evaluator import evaluate_postfix, evaluate_infix


def display_title():
    print("\n" + "=" * 55)
    print("       EXPRESSION EVALUATOR AND CALCULATOR")
    print("=" * 55)


def display_menu():
    print("\n1. Convert infix expression to postfix")
    print("2. Evaluate postfix expression")
    print("3. Evaluate infix expression")
    print("4. Display operator precedence")
    print("5. Exit")


def convert_expression():
    expression = input("\nEnter an infix expression: ")

    postfix_tokens = infix_to_postfix(expression)
    postfix_expression = " ".join(postfix_tokens)

    print("\nInfix expression  :", expression)
    print("Postfix expression:", postfix_expression)


def calculate_postfix():
    expression = input(
        "\nEnter a space-separated postfix expression: "
    )

    postfix_tokens = expression.split()
    result = evaluate_postfix(postfix_tokens)

    print("\nPostfix expression:", expression)
    print("Result            :", result)


def calculate_infix():
    expression = input("\nEnter an infix expression: ")

    postfix_tokens, result = evaluate_infix(expression)

    print("\nInfix expression  :", expression)
    print("Postfix expression:", " ".join(postfix_tokens))
    print("Result            :", result)


def display_precedence():
    print("\nOperator Precedence")
    print("-" * 30)
    print("Unary minus (-) : Highest")
    print("Exponent (^)    : 3")
    print("*, /, %         : 2")
    print("+, -            : 1")
    print("-" * 30)


def main():
    while True:
        display_title()
        display_menu()

        choice = input("\nEnter your choice: ").strip()

        try:
            if choice == "1":
                convert_expression()

            elif choice == "2":
                calculate_postfix()

            elif choice == "3":
                calculate_infix()

            elif choice == "4":
                display_precedence()

            elif choice == "5":
                print("\nCalculator closed successfully.")
                break

            else:
                print("\nInvalid choice. Enter a number from 1 to 5.")

        except ValueError as error:
            print("\nExpression Error:", error)

        except ZeroDivisionError as error:
            print("\nMathematical Error:", error)

        except Exception as error:
            print("\nUnexpected Error:", error)

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()