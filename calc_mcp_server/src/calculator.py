def calculator(x: float, y: float, operation: str) -> float:
    """Simple calculator tool that performs basic math operations.

    :param x: First number to perform operation on
    :param y: Second number to perform operation on
    :param operation: Mathematical operation to perform ('add', 'subtract', 'multiply', 'divide')
    :returns: Dictionary containing success status and result or error message
    """
    if operation == "add":
        result = float(x) + float(y)
    elif operation == "subtract":
        result = float(x) - float(y)
    elif operation == "multiply":
        result = float(x) * float(y)
    elif operation == "divide":
        if float(y) == 0:
            return {"success": False, "error": "Cannot divide by zero"}
        result = float(x) / float(y)
    else:
        raise ValueError("Invalid operation: {operation}")

    return str(result)
