from fastmcp import FastMCP
import math
from typing import Union, List, Dict, Any
import json

# Create an instance of FastMCP
mcp_math_server = FastMCP(name="MathTools")

@mcp_math_server.tool()
def add(a: Union[int, float], b: Union[int, float]) -> Dict[str, Any]:
    """Adds two numbers and returns the result with step-by-step explanation."""
    result = a + b
    return {
        "operation": "addition",
        "expression": f"{a} + {b}",
        "result": result,
        "steps": [
            f"Step 1: Add {a} and {b}",
            f"{a} + {b} = {result}",
            f"Final result: {result}"
        ]
    }

@mcp_math_server.tool()
def subtract(a: Union[int, float], b: Union[int, float]) -> Dict[str, Any]:
    """Subtracts the second number from the first and returns the result with steps."""
    result = a - b
    return {
        "operation": "subtraction",
        "expression": f"{a} - {b}",
        "result": result,
        "steps": [
            f"Step 1: Subtract {b} from {a}",
            f"{a} - {b} = {result}",
            f"Final result: {result}"
        ]
    }

@mcp_math_server.tool()
def multiply(a: Union[int, float], b: Union[int, float]) -> Dict[str, Any]:
    """Multiplies two numbers and returns the result with steps."""
    result = a * b
    return {
        "operation": "multiplication",
        "expression": f"{a} × {b}",
        "result": result,
        "steps": [
            f"Step 1: Multiply {a} by {b}",
            f"{a} × {b} = {result}",
            f"Final result: {result}"
        ]
    }

@mcp_math_server.tool()
def divide(a: Union[int, float], b: Union[int, float]) -> Dict[str, Any]:
    """Divides the first number by the second and returns the result with steps."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    result = a / b
    return {
        "operation": "division",
        "expression": f"{a} ÷ {b}",
        "result": result,
        "steps": [
            f"Step 1: Divide {a} by {b}",
            f"{a} ÷ {b} = {result}",
            f"Final result: {result}"
        ]
    }

@mcp_math_server.tool()
def power(base: Union[int, float], exponent: Union[int, float]) -> Dict[str, Any]:
    """Raises a number to a power and returns the result with steps."""
    result = base ** exponent
    return {
        "operation": "exponentiation",
        "expression": f"{base}^{exponent}",
        "result": result,
        "steps": [
            f"Step 1: Raise {base} to the power of {exponent}",
            f"{base}^{exponent} = {result}",
            f"Final result: {result}"
        ]
    }

@mcp_math_server.tool()
def square_root(number: Union[int, float]) -> Dict[str, Any]:
    """Calculates the square root of a number and returns the result with steps."""
    if number < 0:
        raise ValueError("Cannot calculate square root of a negative number")
    result = math.sqrt(number)
    return {
        "operation": "square_root",
        "expression": f"√{number}",
        "result": result,
        "steps": [
            f"Step 1: Find the square root of {number}",
            f"√{number} = {result}",
            f"Final result: {result}"
        ]
    }

@mcp_math_server.tool()
def solve_equation(equation: str) -> Dict[str, Any]:
    """
    Solves a simple linear equation in the form 'ax + b = c' and returns the solution with steps.
    Example: solve_equation("2x + 3 = 7")
    """
    try:
        # Simple equation solver for demonstration
        parts = equation.replace(' ', '').split('=')
        if len(parts) != 2:
            raise ValueError("Equation must contain exactly one '='")
        
        left = parts[0]
        right = parts[1]
        
        # Very basic equation solving - this is just an example
        # In a real application, you'd want a proper equation parser
        if 'x' not in left:
            raise ValueError("Equation must contain 'x' on the left side")
            
        # Simple case: ax + b = c
        if '+' in left:
            a_part, b_part = left.split('+', 1)
            a = float(a_part.replace('x', '')) if 'x' in a_part else 1.0
            b = float(b_part)
            c = float(right)
            x = (c - b) / a
        # Handle other simple cases as needed...
        else:
            raise ValueError("Unsupported equation format")
            
        return {
            "operation": "solve_equation",
            "equation": equation,
            "result": x,
            "steps": [
                f"Step 1: Start with the equation: {equation}",
                f"Step 2: Isolate the variable x",
                f"{left} = {right}",
                f"{left.replace('+', '-')} = {right} - {b}" if '+' in left else "",
                f"{a}x = {c - b}" if '+' in left else "",
                f"x = ({c} - {b}) / {a}" if '+' in left else "",
                f"x = {x}",
                f"Final solution: x = {x}"
            ]
        }
    except Exception as e:
        return {
            "operation": "solve_equation",
            "equation": equation,
            "error": str(e),
            "message": "Failed to solve equation. Make sure it's in a supported format like '2x + 3 = 7'."
        }

if __name__ == "__main__":
    print("Starting MathTools MCP Server (for mcp-use command execution)...")
    mcp_math_server.run()
