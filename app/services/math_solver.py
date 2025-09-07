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
        
        # Handle implicit multiplication (e.g., 2x -> 2*x, 3(x+1) -> 3*(x+1))
        expression = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expression)
        expression = re.sub(r'(\d)(\()', r'\1*\2', expression)
        expression = re.sub(r'(\))(\d)', r'\1*\2', expression)
        expression = re.sub(r'(\))(\()', r'\1*\2', expression)
        expression = re.sub(r'([a-zA-Z])(\()', r'\1*\2', expression)
        
        return expression
    
    def solve_expression(self, expression: str) -> Tuple[bool, str, Optional[str]]:
        """
        Solve a mathematical expression
        Returns: (success, result, steps)
        """
        try:
            # Preprocess the expression
            processed_expr = self.preprocess_expression(expression)
            
            # Parse the expression using SymPy
            expr = sp.sympify(processed_expr, locals=self.constants)
            
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
            sp.sympify(processed_expr, locals=self.constants)
            return True, "Valid expression"
        except Exception as e:
            return False, f"Invalid expression: {str(e)}"
    
    def get_expression_info(self, expression: str) -> dict:
        """Get additional information about the expression"""
        try:
            processed_expr = self.preprocess_expression(expression)
            expr = sp.sympify(processed_expr, locals=self.constants)
            
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
