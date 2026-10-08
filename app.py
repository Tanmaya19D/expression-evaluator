
from flask import Flask, jsonify, render_template, request

from calculator.converter import infix_to_postfix
from calculator.evaluator import evaluate_infix


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/convert", methods=["POST"])
def convert_expression():
    try:
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({
                "success": False,
                "error": "Invalid request data."
            }), 400

        expression = str(
            data.get("expression", "")
        ).strip()

        if not expression:
            return jsonify({
                "success": False,
                "error": "Please enter an expression."
            }), 400

        postfix_tokens = infix_to_postfix(expression)

        return jsonify({
            "success": True,
            "infix": expression,
            "postfix": " ".join(postfix_tokens)
        }), 200

    except (ValueError, ZeroDivisionError) as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 400

    except Exception as error:
        print("Conversion error:", error)

        return jsonify({
            "success": False,
            "error": f"Server error: {str(error)}"
        }), 500


@app.route("/api/evaluate", methods=["POST"])
def evaluate_expression():
    try:
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({
                "success": False,
                "error": "Invalid request data."
            }), 400

        expression = str(
            data.get("expression", "")
        ).strip()

        if not expression:
            return jsonify({
                "success": False,
                "error": "Please enter an expression."
            }), 400

        # Get variable values from frontend
        variables = data.get("variables", {})

        if not isinstance(variables, dict):
            return jsonify({
                "success": False,
                "error": "Variables must be provided as an object."
            }), 400

        result = evaluate_infix(
            expression,
            variables
        )

        return jsonify({
            "success": True,
            "infix": result["infix"],
            "postfix": result["postfix"],
            "result": result["result"]
        }), 200

    except (ValueError, ZeroDivisionError) as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 400

    except Exception as error:
        print("Evaluation error:", error)

        return jsonify({
            "success": False,
            "error": f"Server error: {str(error)}"
        }), 500


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({
        "success": False,
        "error": "API route not found."
    }), 404


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error."
    }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
