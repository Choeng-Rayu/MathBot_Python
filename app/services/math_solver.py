import sympy as sp
import re
from typing import Tuple, Optional
import math

class MathSolver:
    def __init__(self):
        # Define common mathematical constants and functions
        self.constants = {
            'pi': sp.pi,
            'e': sp.E,
            'inf': sp.oo,
            'infinity': sp.oo
        }
        
        # Define function mappings
        self.functions = {
            'sin': sp.sin,
            'cos': sp.cos,
            'tan': sp.tan,
            'asin': sp.asin,
            'acos': sp.acos,
            'atan': sp.atan,
            'sinh': sp.sinh,
            'cosh': sp.cosh,
            'tanh': sp.tanh,
            'log': sp.log,
            'ln': sp.log,
            'log10': lambda x: sp.log(x, 10),
            'sqrt': sp.sqrt,
            'abs': sp.Abs,
            'exp': sp.exp,
            'factorial': sp.factorial,
            'floor': sp.floor,
            'ceil': sp.ceiling,
        }
    
    def preprocess_expression(self, expression: str) -> str:
        """Preprocess the mathematical expression for better parsing"""
        # Remove spaces
        expression = expression.replace(' ', '')
        
        # Replace common patterns
        expression = expression.replace('^', '**')  # Power operator
        expression = expression.replace('π', 'pi')
        expression = expression.replace('∞', 'inf')
        
        # Handle factorial (convert ! to factorial function)
        expression = re.sub(r'(\d+)!', r'factorial(\1)', expression)
        expression = re.sub(r'([a-zA-Z]+)!', r'factorial(\1)', expression)
        
        # Handle implicit multiplication (e.g., 2x -> 2*x, 3(x+1) -> 3*(x+1))
        expression = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expression)
        expression = re.sub(r'(\d)(\()', r'\1*\2', expression)
        expression = re.sub(r'(\))(\d)', r'\1*\2', expression)
        expression = re.sub(r'(\))(\()', r'\1*\2', expression)
        expression = re.sub(r'([a-zA-Z])(\()', r'\1*\2', expression)
        
        return expression
    
    def solve_expression(self, expression: str) -> Tuple[bool, str, Optional[str]]:
        """
        Solve a mathematical expression or equation
        Returns: (success, result, steps)
        """
        try:
            # Check if it's an equation (contains = sign)
            if '=' in expression:
                return self.solve_equation(expression)
            
            # Preprocess the expression
            processed_expr = self.preprocess_expression(expression)
            
            # Combine constants and functions for sympify
            sympify_locals = {**self.constants, **self.functions}
            
            # Parse the expression using SymPy
            expr = sp.sympify(processed_expr, locals=sympify_locals)
            
            # Evaluate the expression
            result = expr.evalf()
            
            # Generate steps if possible
            steps = self._generate_steps(expr, result)
            
            # Format the result
            if result.is_real:
                if result == int(result):
                    formatted_result = str(int(result))
                else:
                    formatted_result = f"{float(result):.10g}"
            else:
                formatted_result = str(result)
            
            return True, formatted_result, steps
            
        except Exception as e:
            return False, f"Error: {str(e)}", None

    def solve_equation(self, equation: str) -> Tuple[bool, str, Optional[str]]:
        """
        Solve one-step and multi-step equations
        Returns: (success, solution, steps)
        """
        try:
            # Split equation by = sign
            parts = equation.split('=')
            if len(parts) != 2:
                return False, "Invalid equation format. Use format: expression = expression", None
            
            left_side, right_side = parts[0].strip(), parts[1].strip()
            
            # Preprocess both sides
            left_expr = self.preprocess_expression(left_side)
            right_expr = self.preprocess_expression(right_side)
            
            # Combine constants and functions for sympify
            sympify_locals = {**self.constants, **self.functions}
            
            # Parse both sides
            left = sp.sympify(left_expr, locals=sympify_locals)
            right = sp.sympify(right_expr, locals=sympify_locals)
            
            # Create equation
            equation_obj = sp.Eq(left, right)
            
            # Find variables in the equation
            variables = equation_obj.free_symbols
            
            if len(variables) == 0:
                # No variables - check if equation is true
                is_true = sp.simplify(left - right) == 0
                result = "True" if is_true else "False"
                steps = f"Checking: {left} = {right}\nResult: {result}"
                return True, result, steps
            
            elif len(variables) == 1:
                # One variable - solve for it
                var = list(variables)[0]
                solutions = sp.solve(equation_obj, var)
                
                if not solutions:
                    return True, "No solution", f"The equation {equation} has no solution"
                
                # Format solutions
                if len(solutions) == 1:
                    sol = solutions[0]
                    if sol.is_real:
                        if sol == int(sol):
                            formatted_sol = str(int(sol))
                        else:
                            formatted_sol = f"{float(sol):.10g}"
                    else:
                        formatted_sol = str(sol)
                    
                    result = f"{var} = {formatted_sol}"
                    steps = self._generate_equation_steps(equation, var, sol)
                    return True, result, steps
                else:
                    # Multiple solutions
                    formatted_sols = []
                    for sol in solutions:
                        if sol.is_real:
                            if sol == int(sol):
                                formatted_sols.append(str(int(sol)))
                            else:
                                formatted_sols.append(f"{float(sol):.10g}")
                        else:
                            formatted_sols.append(str(sol))
                    
                    result = f"{var} = {', '.join(formatted_sols)}"
                    steps = f"Solving: {equation}\nSolutions: {result}"
                    return True, result, steps
            
            else:
                # Multiple variables
                return False, "Equation has multiple variables. Please specify which variable to solve for.", None
                
        except Exception as e:
            return False, f"Error solving equation: {str(e)}", None

    def _generate_equation_steps(self, original_equation: str, variable, solution) -> str:
        """Generate step-by-step solution for equations"""
        steps = []
        
        try:
            steps.append(f"Original equation: {original_equation}")
            
            # Detect equation type
            if '+' in original_equation and '-' not in original_equation:
                steps.append("This is an addition equation")
                steps.append("To solve: subtract the constant from both sides")
            elif '-' in original_equation and '+' not in original_equation:
                steps.append("This is a subtraction equation")
                steps.append("To solve: add the constant to both sides")
            elif '*' in original_equation and '/' not in original_equation:
                steps.append("This is a multiplication equation")
                steps.append("To solve: divide both sides by the coefficient")
            elif '/' in original_equation and '*' not in original_equation:
                steps.append("This is a division equation")
                steps.append("To solve: multiply both sides by the divisor")
            else:
                steps.append("Solving the equation step by step...")
            
            steps.append(f"Solution: {variable} = {solution}")
            
            return "\n".join(steps)
            
        except:
            return f"Equation: {original_equation}\nSolution: {variable} = {solution}"
    
    def _generate_steps(self, expr, result) -> str:
        """Generate step-by-step solution if possible"""
        steps = []
        
        try:
            # Original expression
            steps.append(f"Original: {expr}")
            
            # Try to show intermediate steps for common operations
            if expr.has(sp.log):
                steps.append("Evaluating logarithmic functions...")
            
            if expr.has(sp.sin, sp.cos, sp.tan):
                steps.append("Evaluating trigonometric functions...")
            
            if expr.has(sp.exp):
                steps.append("Evaluating exponential functions...")
            
            # Final result
            steps.append(f"Result: {result}")
            
            return "\n".join(steps)
            
        except:
            return f"Direct evaluation: {result}"
    
    def validate_expression(self, expression: str) -> Tuple[bool, str]:
        """Validate if the expression is mathematically valid"""
        try:
            processed_expr = self.preprocess_expression(expression)
            sympify_locals = {**self.constants, **self.functions}
            sp.sympify(processed_expr, locals=sympify_locals)
            return True, "Valid expression"
        except Exception as e:
            return False, f"Invalid expression: {str(e)}"
    
    def get_expression_info(self, expression: str) -> dict:
        """Get additional information about the expression"""
        try:
            processed_expr = self.preprocess_expression(expression)
            sympify_locals = {**self.constants, **self.functions}
            expr = sp.sympify(processed_expr, locals=sympify_locals)
            
            info = {
                "variables": list(expr.free_symbols),
                "is_constant": len(expr.free_symbols) == 0,
                "complexity": len(str(expr)),
                "has_trig": expr.has(sp.sin, sp.cos, sp.tan),
                "has_log": expr.has(sp.log),
                "has_exp": expr.has(sp.exp),
            }
            
            return info
            
        except:
            return {}

# Global math solver instance
math_solver = MathSolver()
