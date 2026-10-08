
const expressionInput =
    document.getElementById("expression");

const convertButton =
    document.getElementById("convert-button");

const evaluateButton =
    document.getElementById("evaluate-button");

const clearButton =
    document.getElementById("clear-button");

const messageBox =
    document.getElementById("message");

const infixResult =
    document.getElementById("infix-result");

const postfixResult =
    document.getElementById("postfix-result");

const finalResult =
    document.getElementById("final-result");

const variablesContainer =
    document.getElementById(
        "variables-container"
    );

const variablesList =
    document.getElementById(
        "variables-list"
    );


convertButton.addEventListener(
    "click",
    convertExpression
);


evaluateButton.addEventListener(
    "click",
    evaluateExpression
);


clearButton.addEventListener(
    "click",
    clearCalculator
);


expressionInput.addEventListener(
    "input",
    detectVariables
);


expressionInput.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Enter") {
            evaluateExpression();
        }

    }
);


document
    .querySelectorAll(".example-button")
    .forEach(function (button) {

        button.addEventListener(
            "click",
            function () {

                expressionInput.value =
                    button.textContent.trim();

                detectVariables();

                expressionInput.focus();

            }
        );

    });


function detectVariables() {

    const expression =
        expressionInput.value;

    const matches =
        expression.match(
            /[A-Za-z_][A-Za-z0-9_]*/g
        );


    if (!matches) {

        variablesContainer
            .classList
            .add("hidden");

        variablesList.innerHTML = "";

        return;
    }


    const variables =
        [...new Set(matches)];


    variablesContainer
        .classList
        .remove("hidden");


    variablesList.innerHTML = "";


    variables.forEach(
        function (variable) {

            const row =
                document.createElement("div");

            row.className =
                "variable-row";


            const label =
                document.createElement("label");

            label.textContent =
                variable + ":";

            label.setAttribute(
                "for",
                "variable-" + variable
            );


            const input =
                document.createElement("input");

            input.type = "number";

            input.step = "any";

            input.id =
                "variable-" + variable;

            input.className =
                "variable-input";

            input.placeholder =
                "Enter value";


            row.appendChild(label);

            row.appendChild(input);

            variablesList.appendChild(row);

        }
    );
}


function getVariableValues() {

    const variables = {};

    const inputs =
        document.querySelectorAll(
            ".variable-input"
        );


    for (const input of inputs) {

        const variable =
            input.id.replace(
                "variable-",
                ""
            );


        const value =
            input.value.trim();


        if (value === "") {

            throw new Error(
                `Please enter a value for '${variable}'.`
            );

        }


        const numericValue =
            Number(value);


        if (!Number.isFinite(
            numericValue
        )) {

            throw new Error(
                `Invalid value for '${variable}'.`
            );

        }


        variables[variable] =
            numericValue;
    }


    return variables;
}


async function convertExpression() {

    const expression =
        expressionInput.value.trim();


    if (!expression) {

        showMessage(
            "Please enter an expression.",
            "error"
        );

        return;
    }


    setLoading(true);


    try {

        const response =
            await fetch(
                "/api/convert",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        expression:
                            expression
                    })

                }
            );


        const responseText =
            await response.text();


        let data;


        try {

            data =
                JSON.parse(responseText);

        }

        catch {

            throw new Error(
                "The backend returned an invalid response. Check the Flask terminal."
            );

        }


        if (
            !response.ok ||
            !data.success
        ) {

            throw new Error(
                data.error ||
                "Conversion failed."
            );

        }


        infixResult.textContent =
            data.infix;


        postfixResult.textContent =
            data.postfix;


        finalResult.textContent =
            "Not evaluated";


        showMessage(
            "Expression converted successfully.",
            "success"
        );

    }

    catch (error) {

        showMessage(
            error.message,
            "error"
        );

    }

    finally {

        setLoading(false);

    }
}


async function evaluateExpression() {

    const expression =
        expressionInput.value.trim();


    if (!expression) {

        showMessage(
            "Please enter an expression.",
            "error"
        );

        return;
    }


    let variables;


    try {

        variables =
            getVariableValues();

    }

    catch (error) {

        showMessage(
            error.message,
            "error"
        );

        return;
    }


    setLoading(true);


    try {

        const response =
            await fetch(
                "/api/evaluate",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        expression:
                            expression,

                        variables:
                            variables

                    })

                }
            );


        const responseText =
            await response.text();


        let data;


        try {

            data =
                JSON.parse(responseText);

        }

        catch {

            throw new Error(
                "The backend returned an invalid response. Check the Flask terminal."
            );

        }


        if (
            !response.ok ||
            !data.success
        ) {

            throw new Error(
                data.error ||
                "Evaluation failed."
            );

        }


        infixResult.textContent =
            data.infix;


        postfixResult.textContent =
            data.postfix;


        finalResult.textContent =
            data.result;


        showMessage(
            "Expression evaluated successfully.",
            "success"
        );

    }

    catch (error) {

        showMessage(
            error.message,
            "error"
        );

    }

    finally {

        setLoading(false);

    }
}


function clearCalculator() {

    expressionInput.value = "";


    infixResult.textContent =
        "—";


    postfixResult.textContent =
        "—";


    finalResult.textContent =
        "—";


    variablesContainer
        .classList
        .add("hidden");


    variablesList.innerHTML =
        "";


    messageBox.className =
        "message hidden";


    expressionInput.focus();
}


function showMessage(
    message,
    type
) {

    messageBox.textContent =
        message;


    messageBox.className =
        `message ${type}`;
}


function setLoading(
    isLoading
) {

    convertButton.disabled =
        isLoading;

    evaluateButton.disabled =
        isLoading;

    clearButton.disabled =
        isLoading;


    if (isLoading) {

        convertButton.textContent =
            "Processing...";

        evaluateButton.textContent =
            "Processing...";

    }

    else {

        convertButton.textContent =
            "Convert to Postfix";

        evaluateButton.textContent =
            "Evaluate";

    }
}
