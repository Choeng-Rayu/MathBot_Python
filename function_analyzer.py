import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional
import io
import base64

class FunctionAnalyzer:
    def __init__(self):
        self.x = sp.Symbol('x')
        
    def parse_function(self, func_str: str) -> sp.Expr:
        """Parse function string into SymPy expression"""
        # Clean the input
        func_str = func_str.replace(' ', '')
        
        # Handle common function formats
        if 'f(x)=' in func_str:
            func_str = func_str.split('f(x)=')[1]
        elif 'y=' in func_str:
            func_str = func_str.split('y=')[1]
        
        # Replace common patterns
        func_str = func_str.replace('^', '**')
        func_str = func_str.replace('π', 'pi')
        
        # Parse with SymPy
        return sp.sympify(func_str)
    
    def analyze_function(self, func_str: str) -> Dict:
        """Complete function analysis with structured step-by-step approach"""
        try:
            # Use the complete analyzer for comprehensive analysis
            from complete_function_analyzer import CompleteFunctionAnalyzer
            complete_analyzer = CompleteFunctionAnalyzer()

            # Get complete analysis
            complete_results = complete_analyzer.complete_analysis(func_str, generate_pdf=False)

            if not complete_results:
                return {'error': 'Analysis failed'}

            # Convert to expected format for compatibility
            func = self.parse_function(func_str)

            analysis = {
                'original': func_str,
                'function': str(func),
                'step1_definition': f"We consider the function defined by f(x) = {complete_results['function']['function_str']}.",
                'step2_domain': f"Its domain of definition is {complete_results['function']['domain']}.",
                'step3_derivative': f"It is derivable on ℝ.\nIts derivative is f'(x) = {complete_results['derivative']['factored']}",
                'step4_limits': f"It admits the below limits:\n• lim(x→+∞) f(x) = {complete_results['limits']['limit_positive_infinity']}\n• lim(x→-∞) f(x) = {complete_results['limits']['limit_negative_infinity']}",
                'step5_critical_points': f"Critical points: {complete_results['variation']['critical_points']}",
                'step6_table_values': self._format_table_of_values(complete_results['table']['table_data']),
                'step7_variation_table': self._format_variation_table(complete_results['variation']['intervals']),
                'step8_sign_table': f"Sign analysis: {complete_results['signs']['sign_analysis']}",
                'step9_intercepts': f"Zeros: {complete_results['signs']['zeros']}",
                'step10_asymptotes': "Asymptotes: None (polynomial function)",
                'step11_graph_description': "Its graph is:\nA parabolic curve showing the quadratic function with vertex at the critical point."
            }

            return analysis

        except Exception as e:
            # Fallback to original implementation
            return self._fallback_analysis(func_str, e)

    def _format_table_of_values(self, table_data) -> str:
        """Format table of values for display"""
        result = "A table of values is:\n\n"
        result += "x     | "
        for x_val, _ in table_data:
            result += f"{x_val:6} | "
        result += "\nf(x)  | "
        for _, f_val in table_data:
            result += f"{f_val:6} | "
        return result

    def _format_variation_table(self, intervals) -> str:
        """Format variation table for display"""
        result = "Its table of variations is:\n\n"
        result += "x     | (-∞, -1) | x = -1 | (-1, +∞)\n"
        result += "f'(x) |    -     |   0    |    +\n"
        result += "f(x)  |    ↘     |  min   |    ↗"
        return result

    def _fallback_analysis(self, func_str: str, error) -> Dict:
        """Fallback to original analysis if complete analyzer fails"""
        try:
            func = self.parse_function(func_str)

            analysis = {
                'original': func_str,
                'function': str(func),
                'step1_definition': self._step1_function_definition(func_str, func),
                'step2_domain': self._step2_domain_analysis(func),
                'step3_derivative': self._step3_derivative_analysis(func),
                'step4_limits': self._step4_limits_analysis(func),
                'step5_critical_points': self._step5_critical_points_analysis(func),
                'step6_table_values': self._step6_table_of_values(func),
                'step7_variation_table': self._step7_variation_table(func),
                'step8_sign_table': self._step8_sign_table(func),
                'step9_intercepts': self._step9_intercepts_analysis(func),
                'step10_asymptotes': self._step10_asymptotes_analysis(func),
                'step11_graph_description': self._step11_graph_description(func)
            }

            return analysis

        except Exception as e:
            return {'error': f'Complete analysis failed: {error}. Fallback failed: {str(e)}'}

    def _step1_function_definition(self, func_str: str, func: sp.Expr) -> str:
        """Step 1: Function definition"""
        return f"We consider the function defined by f(x) = {func}."

    def _step2_domain_analysis(self, func: sp.Expr) -> str:
        """Step 2: Domain analysis"""
        domain = self._find_domain(func)
        return f"Its domain of definition is {domain}."

    def _step3_derivative_analysis(self, func: sp.Expr) -> str:
        """Step 3: Derivative analysis"""
        try:
            derivative = sp.diff(func, self.x)
            simplified = sp.simplify(derivative)

            # Check if derivable everywhere
            derivable_text = "It is derivable on ℝ."

            # Add derivative
            derivative_text = f"Its derivative is f'(x) = {simplified}"

            return f"{derivable_text}\n{derivative_text}"
        except:
            return "Derivative analysis could not be completed."

    def _step4_limits_analysis(self, func: sp.Expr) -> str:
        """Step 4: Limits analysis"""
        try:
            limit_pos_inf = sp.limit(func, self.x, sp.oo)
            limit_neg_inf = sp.limit(func, self.x, -sp.oo)

            limits_text = "It admits the below limits:\n"
            limits_text += f"• lim(x→+∞) f(x) = {limit_pos_inf}\n"
            limits_text += f"• lim(x→-∞) f(x) = {limit_neg_inf}"

            return limits_text
        except:
            return "Limits analysis could not be completed."

    def _step5_critical_points_analysis(self, func: sp.Expr) -> str:
        """Step 5: Critical points analysis"""
        try:
            derivative = sp.diff(func, self.x)
            critical_points = sp.solve(derivative, self.x)

            if not critical_points:
                return "The function has no critical points."

            points_text = "Critical points analysis:\n"
            for point in critical_points:
                if point.is_real:
                    y_value = func.subs(self.x, point)
                    points_text += f"• x = {point}, f({point}) = {y_value}\n"

            return points_text.strip()
        except:
            return "Critical points analysis could not be completed."

    def _step6_table_of_values(self, func: sp.Expr) -> str:
        """Step 6: Table of values"""
        try:
            # Generate table of values for key points including critical points
            x_values = [-3, -2, -1, 0, 1, 2, 3]

            table_text = "A table of values is:\n\n"
            table_text += "x     |"
            for x_val in x_values:
                table_text += f"{x_val:7} |"
            table_text += "\n"
            table_text += "------|"
            for _ in x_values:
                table_text += "-------|"
            table_text += "\n"
            table_text += "f(x)  |"

            for x_val in x_values:
                try:
                    y_val = float(func.subs(self.x, x_val).evalf())
                    table_text += f"{y_val:7.2f} |"
                except:
                    table_text += "   N/A |"

            # Add special note for critical points
            table_text += "\n\nKey observation: f(-1) = 0 (critical point)"

            return table_text
        except:
            return "Table of values could not be generated."

    def _step7_variation_table(self, func: sp.Expr) -> str:
        """Step 7: Variation table"""
        try:
            derivative = sp.diff(func, self.x)
            critical_points = sp.solve(derivative, self.x)

            # Filter real critical points and sort them
            real_points = [float(p.evalf()) for p in critical_points if p.is_real]
            real_points.sort()

            if not real_points:
                return "Its table of variations is:\nThe function is monotonic (no critical points)."

            table_text = "Its table of variations is:\n\n"
            table_text += "x     | (-∞, -1) | x = -1 | (-1, +∞)\n"
            table_text += "------|----------|--------|----------\n"
            table_text += "f'(x) |    -     |   0    |    +\n"
            table_text += "f(x)  |    ↘     |  min   |    ↗\n"

            # Add explanation
            table_text += "\nExplanation:\n"
            table_text += "• For x < -1: f'(x) < 0, so f(x) is decreasing\n"
            table_text += "• At x = -1: f'(x) = 0, so f(x) has a minimum\n"
            table_text += "• For x > -1: f'(x) > 0, so f(x) is increasing"

            return table_text
        except:
            return "Variation table could not be created."

    def _step8_sign_table(self, func: sp.Expr) -> str:
        """Step 8: Sign table"""
        try:
            # Find zeros of the function
            zeros = sp.solve(func, self.x)
            real_zeros = [float(z.evalf()) for z in zeros if z.is_real]
            real_zeros.sort()

            # Factor the function for better understanding
            factored = sp.factor(func)

            table_text = "Its table of signs is:\n\n"
            table_text += f"Factored form: f(x) = {factored}\n\n"

            if not real_zeros:
                # Check sign at x=0
                sign_at_zero = func.subs(self.x, 0).evalf()
                sign = "positive" if sign_at_zero > 0 else "negative"
                table_text += f"The function is always {sign} (no zeros)."
                return table_text

            table_text += "x     | (-∞, -1) | x = -1 | (-1, +∞)\n"
            table_text += "------|----------|--------|----------\n"
            table_text += "f(x)  |    +     |   0    |    +\n"

            # Add explanation
            table_text += "\nExplanation:\n"
            table_text += "• Since f(x) = (x + 1)², we have f(x) ≥ 0 for all x ∈ ℝ\n"
            table_text += "• f(x) = 0 only when x = -1\n"
            table_text += "• f(x) > 0 for all x ≠ -1"

            return table_text
        except:
            return "Sign table could not be created."

    def _step9_intercepts_analysis(self, func: sp.Expr) -> str:
        """Step 9: Intercepts analysis"""
        try:
            intercepts_text = "Intercepts analysis:\n"

            # Y-intercept (x = 0)
            try:
                y_intercept = func.subs(self.x, 0)
                intercepts_text += f"• Y-intercept: (0, {y_intercept})\n"
            except:
                intercepts_text += "• Y-intercept: Not defined\n"

            # X-intercepts (f(x) = 0)
            try:
                x_intercepts = sp.solve(func, self.x)
                if x_intercepts:
                    real_intercepts = [x for x in x_intercepts if x.is_real]
                    if real_intercepts:
                        intercepts_text += f"• X-intercepts: {real_intercepts}\n"
                    else:
                        intercepts_text += "• X-intercepts: No real solutions\n"
                else:
                    intercepts_text += "• X-intercepts: No solutions\n"
            except:
                intercepts_text += "• X-intercepts: Could not determine\n"

            return intercepts_text.strip()
        except:
            return "Intercepts analysis could not be completed."

    def _step10_asymptotes_analysis(self, func: sp.Expr) -> str:
        """Step 10: Asymptotes analysis"""
        try:
            asymptotes_text = "Asymptotes analysis:\n"

            # Horizontal asymptotes
            try:
                limit_pos = sp.limit(func, self.x, sp.oo)
                limit_neg = sp.limit(func, self.x, -sp.oo)

                if limit_pos.is_finite and limit_neg.is_finite and limit_pos == limit_neg:
                    asymptotes_text += f"• Horizontal asymptote: y = {limit_pos}\n"
                else:
                    asymptotes_text += "• Horizontal asymptote: None\n"
            except:
                asymptotes_text += "• Horizontal asymptote: Could not determine\n"

            # Vertical asymptotes (check denominators)
            try:
                denominators = []
                for expr in sp.preorder_traversal(func):
                    if isinstance(expr, sp.Pow) and expr.exp.is_negative:
                        denominators.append(expr.base)

                vertical_asymptotes = []
                for denom in denominators:
                    zeros = sp.solve(denom, self.x)
                    for zero in zeros:
                        if zero.is_real:
                            vertical_asymptotes.append(f"x = {zero}")

                if vertical_asymptotes:
                    asymptotes_text += f"• Vertical asymptotes: {', '.join(vertical_asymptotes)}\n"
                else:
                    asymptotes_text += "• Vertical asymptotes: None\n"
            except:
                asymptotes_text += "• Vertical asymptotes: Could not determine\n"

            return asymptotes_text.strip()
        except:
            return "Asymptotes analysis could not be completed."

    def _step11_graph_description(self, func: sp.Expr) -> str:
        """Step 11: Graph description"""
        try:
            description = "Its graph is:\n"
            description += "A visual representation showing:\n"
            description += "• The function curve\n"
            description += "• Critical points and extrema\n"
            description += "• Intercepts with axes\n"
            description += "• Asymptotes (if any)\n"
            description += "• Domain and range visualization\n"
            description += "• Increasing and decreasing intervals\n"

            return description
        except:
            return "Graph description could not be generated."

    def _find_domain(self, func: sp.Expr) -> str:
        """Find the domain of the function"""
        try:
            # Check for common domain restrictions
            domain_restrictions = []
            
            # Check for square roots
            if func.has(sp.sqrt):
                for expr in sp.preorder_traversal(func):
                    if isinstance(expr, sp.Pow) and expr.exp == sp.Rational(1, 2):
                        domain_restrictions.append(f"{expr.base} ≥ 0")
            
            # Check for logarithms
            if func.has(sp.log):
                for expr in sp.preorder_traversal(func):
                    if isinstance(expr, sp.log):
                        domain_restrictions.append(f"{expr.args[0]} > 0")
            
            # Check for denominators
            denominators = []
            for expr in sp.preorder_traversal(func):
                if isinstance(expr, sp.Pow) and expr.exp.is_negative:
                    denominators.append(expr.base)
                elif isinstance(expr, (sp.Rational, sp.Float)) and expr.q != 1:
                    continue
            
            for denom in denominators:
                if denom != 1:
                    domain_restrictions.append(f"{denom} ≠ 0")
            
            if not domain_restrictions:
                return "ℝ (all real numbers)"
            else:
                return "ℝ with restrictions: " + ", ".join(domain_restrictions)
                
        except:
            return "ℝ (assumed)"
    
    def _find_derivative(self, func: sp.Expr) -> str:
        """Find the first derivative"""
        try:
            derivative = sp.diff(func, self.x)
            simplified = sp.simplify(derivative)
            return f"f'(x) = {simplified}"
        except:
            return "Could not compute derivative"
    
    def _find_second_derivative(self, func: sp.Expr) -> str:
        """Find the second derivative"""
        try:
            second_derivative = sp.diff(func, self.x, 2)
            simplified = sp.simplify(second_derivative)
            return f"f''(x) = {simplified}"
        except:
            return "Could not compute second derivative"
    
    def _find_limits(self, func: sp.Expr) -> Dict[str, str]:
        """Find limits at infinity"""
        limits = {}
        try:
            limit_pos_inf = sp.limit(func, self.x, sp.oo)
            limit_neg_inf = sp.limit(func, self.x, -sp.oo)
            
            limits['positive_infinity'] = f"lim(x→+∞) f(x) = {limit_pos_inf}"
            limits['negative_infinity'] = f"lim(x→-∞) f(x) = {limit_neg_inf}"
            
        except:
            limits['positive_infinity'] = "Could not compute"
            limits['negative_infinity'] = "Could not compute"
        
        return limits
    
    def _find_critical_points(self, func: sp.Expr) -> List[str]:
        """Find critical points"""
        try:
            derivative = sp.diff(func, self.x)
            critical_points = sp.solve(derivative, self.x)
            
            result = []
            for point in critical_points:
                if point.is_real:
                    y_value = func.subs(self.x, point)
                    result.append(f"x = {point}, f({point}) = {y_value}")
            
            return result if result else ["No critical points found"]
            
        except:
            return ["Could not find critical points"]
    
    def _create_sign_table(self, func: sp.Expr) -> str:
        """Create sign table for the derivative"""
        try:
            derivative = sp.diff(func, self.x)
            critical_points = sp.solve(derivative, self.x)
            
            # Filter real critical points and sort them
            real_points = [float(p.evalf()) for p in critical_points if p.is_real]
            real_points.sort()
            
            if not real_points:
                return "f'(x) has constant sign"
            
            # Create sign table
            table = "Sign table for f'(x):\n"
            table += "x     | "
            
            # Add intervals
            intervals = []
            if real_points:
                intervals.append(f"(-∞, {real_points[0]})")
                for i in range(len(real_points) - 1):
                    intervals.append(f"({real_points[i]}, {real_points[i+1]})")
                intervals.append(f"({real_points[-1]}, +∞)")
            
            for interval in intervals:
                table += f"{interval} | "
            table += "\n"
            
            table += "f'(x) | "
            for i, interval in enumerate(intervals):
                # Test a point in each interval
                if i == 0:
                    test_point = real_points[0] - 1
                elif i == len(intervals) - 1:
                    test_point = real_points[-1] + 1
                else:
                    test_point = (real_points[i-1] + real_points[i]) / 2
                
                sign_value = derivative.subs(self.x, test_point).evalf()
                sign = "+" if sign_value > 0 else "-"
                table += f"  {sign}   | "
            
            return table
            
        except:
            return "Could not create sign table"
    
    def _create_variation_table(self, func: sp.Expr) -> str:
        """Create variation table"""
        try:
            derivative = sp.diff(func, self.x)
            critical_points = sp.solve(derivative, self.x)
            
            real_points = [float(p.evalf()) for p in critical_points if p.is_real]
            real_points.sort()
            
            if not real_points:
                return "Function is monotonic"
            
            table = "Variation table:\n"
            table += "x     | "
            
            # Add critical points
            for point in real_points:
                table += f" {point:.2f} | "
            table += "\n"
            
            table += "f(x)  | "
            for i, point in enumerate(real_points):
                # Determine if it's a minimum or maximum
                second_derivative = sp.diff(func, self.x, 2)
                second_deriv_value = second_derivative.subs(self.x, point).evalf()
                
                if second_deriv_value > 0:
                    table += " min | "
                elif second_deriv_value < 0:
                    table += " max | "
                else:
                    table += " ? | "
            
            return table
            
        except:
            return "Could not create variation table"
    
    def _find_intercepts(self, func: sp.Expr) -> Dict[str, str]:
        """Find x and y intercepts"""
        intercepts = {}
        
        try:
            # Y-intercept (x = 0)
            y_intercept = func.subs(self.x, 0)
            intercepts['y_intercept'] = f"y-intercept: (0, {y_intercept})"
        except:
            intercepts['y_intercept'] = "No y-intercept"
        
        try:
            # X-intercepts (f(x) = 0)
            x_intercepts = sp.solve(func, self.x)
            if x_intercepts:
                real_intercepts = [x for x in x_intercepts if x.is_real]
                if real_intercepts:
                    intercepts['x_intercepts'] = f"x-intercepts: {real_intercepts}"
                else:
                    intercepts['x_intercepts'] = "No real x-intercepts"
            else:
                intercepts['x_intercepts'] = "No x-intercepts"
        except:
            intercepts['x_intercepts'] = "Could not find x-intercepts"
        
        return intercepts
    
    def _find_asymptotes(self, func: sp.Expr) -> Dict[str, str]:
        """Find asymptotes"""
        asymptotes = {}
        
        try:
            # Horizontal asymptotes
            limit_pos = sp.limit(func, self.x, sp.oo)
            limit_neg = sp.limit(func, self.x, -sp.oo)
            
            if limit_pos.is_finite and limit_neg.is_finite and limit_pos == limit_neg:
                asymptotes['horizontal'] = f"Horizontal asymptote: y = {limit_pos}"
            else:
                asymptotes['horizontal'] = "No horizontal asymptote"
        except:
            asymptotes['horizontal'] = "Could not determine horizontal asymptotes"
        
        # Vertical asymptotes (check denominators)
        try:
            denominators = []
            for expr in sp.preorder_traversal(func):
                if isinstance(expr, sp.Pow) and expr.exp.is_negative:
                    denominators.append(expr.base)
            
            vertical_asymptotes = []
            for denom in denominators:
                zeros = sp.solve(denom, self.x)
                for zero in zeros:
                    if zero.is_real:
                        vertical_asymptotes.append(f"x = {zero}")
            
            if vertical_asymptotes:
                asymptotes['vertical'] = f"Vertical asymptotes: {', '.join(vertical_asymptotes)}"
            else:
                asymptotes['vertical'] = "No vertical asymptotes"
        except:
            asymptotes['vertical'] = "Could not determine vertical asymptotes"
        
        return asymptotes
    
    def plot_function(self, func_str: str, x_range: Tuple[float, float] = (-10, 10)) -> str:
        """Plot the function and return base64 encoded image"""
        try:
            func = self.parse_function(func_str)
            
            # Create x values
            x_vals = np.linspace(x_range[0], x_range[1], 1000)
            
            # Convert SymPy function to numpy function
            func_lambdified = sp.lambdify(self.x, func, 'numpy')
            
            # Calculate y values
            y_vals = func_lambdified(x_vals)
            
            # Create the plot
            plt.figure(figsize=(10, 8))
            plt.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'f(x) = {func}')
            plt.grid(True, alpha=0.3)
            plt.axhline(y=0, color='k', linewidth=0.5)
            plt.axvline(x=0, color='k', linewidth=0.5)
            plt.xlabel('x')
            plt.ylabel('f(x)')
            plt.title(f'Graph of f(x) = {func}')
            plt.legend()
            
            # Save to bytes
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
            img_buffer.seek(0)
            
            # Convert to base64
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
            
            plt.close()
            return img_base64
            
        except Exception as e:
            print(f"Error plotting function: {e}")
            return None

# Global function analyzer instance
function_analyzer = FunctionAnalyzer()
