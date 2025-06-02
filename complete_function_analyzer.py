#!/usr/bin/env python3
"""
Complete Function Analyzer Implementation
Following the procedure for analyzing f(x) = x² + 2x + 1

This implementation follows the exact procedure outlined in the specification
for educational mathematical analysis.
"""

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
import base64
from datetime import datetime
import os
from PIL import Image as PILImage

class CompleteFunctionAnalyzer:
    def __init__(self):
        self.x = sp.Symbol('x')
        
    def step1_define_function_and_domain(self, func_expr: str):
        """
        Step 1: Define the Function and Its Domain
        Create a function to represent f(x) = x² + 2x + 1
        Specify the domain as ℝ (all real numbers)
        """
        print("=" * 60)
        print("STEP 1: FUNCTION DEFINITION AND DOMAIN")
        print("=" * 60)
        
        # Parse the function
        func = sp.sympify(func_expr)
        
        # Analysis
        result = {
            'function': func,
            'function_str': str(func),
            'domain': 'ℝ (all real numbers)',
            'reasoning': 'The function is a polynomial and defined for all real x'
        }
        
        print(f"Function: f(x) = {func}")
        print(f"Domain: {result['domain']}")
        print(f"Reasoning: {result['reasoning']}")
        
        return result
    
    def step2_compute_derivative(self, func):
        """
        Step 2: Compute the Derivative
        Calculate f'(x) using symbolic computation
        For f(x) = x² + 2x + 1, compute f'(x) = 2x + 2 = 2(x + 1)
        """
        print("\n" + "=" * 60)
        print("STEP 2: DERIVATIVE COMPUTATION")
        print("=" * 60)
        
        # Compute derivative
        derivative = sp.diff(func, self.x)
        simplified_derivative = sp.simplify(derivative)
        factored_derivative = sp.factor(derivative)
        
        result = {
            'derivative': derivative,
            'simplified': simplified_derivative,
            'factored': factored_derivative,
            'differentiable': 'ℝ (entire domain)'
        }
        
        print(f"f'(x) = {derivative}")
        print(f"Simplified: f'(x) = {simplified_derivative}")
        print(f"Factored form: f'(x) = {factored_derivative}")
        print(f"Differentiable on: {result['differentiable']}")
        
        return result
    
    def step3_evaluate_limits(self, func):
        """
        Step 3: Evaluate Limits
        Compute limits as x → -∞ and x → +∞
        """
        print("\n" + "=" * 60)
        print("STEP 3: LIMITS EVALUATION")
        print("=" * 60)
        
        # Compute limits
        limit_neg_inf = sp.limit(func, self.x, -sp.oo)
        limit_pos_inf = sp.limit(func, self.x, sp.oo)
        
        result = {
            'limit_negative_infinity': limit_neg_inf,
            'limit_positive_infinity': limit_pos_inf,
            'reasoning': 'Quadratic function with positive leading coefficient'
        }
        
        print(f"lim(x→-∞) f(x) = {limit_neg_inf}")
        print(f"lim(x→+∞) f(x) = {limit_pos_inf}")
        print(f"Reasoning: {result['reasoning']}")
        
        return result
    
    def step4_generate_table_of_values(self, func):
        """
        Step 4: Generate Table of Values
        Select key points including x = -1 where f(-1) = 0
        """
        print("\n" + "=" * 60)
        print("STEP 4: TABLE OF VALUES")
        print("=" * 60)
        
        # Key points including critical point x = -1
        x_values = [-3, -2, -1, 0, 1]
        table_data = []
        
        print("Table of Values:")
        print("-" * 30)
        print("x\t|\tf(x)")
        print("-" * 30)
        
        for x_val in x_values:
            f_val = func.subs(self.x, x_val)
            table_data.append((x_val, f_val))
            print(f"{x_val}\t|\t{f_val}")
        
        print("-" * 30)
        
        # Special note for critical point
        critical_value = func.subs(self.x, -1)
        print(f"\nKey observation: f(-1) = {critical_value}")
        
        return {
            'table_data': table_data,
            'critical_point': (-1, critical_value)
        }
    
    def step5_create_variation_table(self, func, derivative):
        """
        Step 5: Create Table of Variations
        Analyze behavior using f'(x) = 2(x + 1)
        """
        print("\n" + "=" * 60)
        print("STEP 5: TABLE OF VARIATIONS")
        print("=" * 60)
        
        # Find critical points
        critical_points = sp.solve(derivative, self.x)
        print(f"Critical points: {critical_points}")
        
        # Analyze intervals
        print("\nVariation Analysis:")
        print("f'(x) = 2(x + 1) = 0 when x = -1")
        print("\nInterval analysis:")
        print("• For x < -1: f'(x) < 0 (decreasing)")
        print("• For x > -1: f'(x) > 0 (increasing)")
        print("• At x = -1: f'(x) = 0 (local minimum)")
        
        # Create variation table
        print("\nTable of Variations:")
        print("-" * 50)
        print("x\t|\t(-∞, -1)\t|\tx = -1\t|\t(-1, +∞)")
        print("-" * 50)
        print("f'(x)\t|\t   -\t\t|\t  0\t|\t   +")
        print("f(x)\t|\t   ↘\t\t|\t min\t|\t   ↗")
        print("-" * 50)
        
        return {
            'critical_points': critical_points,
            'intervals': [
                ('(-∞, -1)', 'decreasing', 'f\'(x) < 0'),
                ('x = -1', 'minimum', 'f\'(x) = 0'),
                ('(-1, +∞)', 'increasing', 'f\'(x) > 0')
            ]
        }
    
    def step6_create_sign_table(self, func):
        """
        Step 6: Create Table of Signs
        Determine sign of f(x) = (x + 1)² ≥ 0
        """
        print("\n" + "=" * 60)
        print("STEP 6: TABLE OF SIGNS")
        print("=" * 60)
        
        # Factor the function
        factored = sp.factor(func)
        print(f"Factored form: f(x) = {factored}")
        
        # Find zeros
        zeros = sp.solve(func, self.x)
        print(f"Zeros: {zeros}")
        
        print("\nSign Analysis:")
        print("Since f(x) = (x + 1)², we have:")
        print("• f(x) ≥ 0 for all x ∈ ℝ")
        print("• f(x) = 0 only at x = -1")
        print("• f(x) > 0 for all x ≠ -1")
        
        # Create sign table
        print("\nTable of Signs:")
        print("-" * 50)
        print("x\t|\t(-∞, -1)\t|\tx = -1\t|\t(-1, +∞)")
        print("-" * 50)
        print("f(x)\t|\t   +\t\t|\t  0\t|\t   +")
        print("-" * 50)
        
        return {
            'factored_form': factored,
            'zeros': zeros,
            'sign_analysis': 'f(x) ≥ 0 for all x ∈ ℝ'
        }
    
    def step7_generate_graph(self, func, save_path=None):
        """
        Step 7: Generate Graphical Representation
        Plot f(x) over range [-5, 5] showing parabolic shape
        """
        print("\n" + "=" * 60)
        print("STEP 7: GRAPHICAL REPRESENTATION")
        print("=" * 60)
        
        # Create x values for plotting
        x_vals = np.linspace(-5, 3, 1000)
        
        # Convert sympy function to numpy function
        func_lambdified = sp.lambdify(self.x, func, 'numpy')
        y_vals = func_lambdified(x_vals)
        
        # Create the plot
        plt.figure(figsize=(12, 8))
        plt.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'f(x) = {func}')
        
        # Mark critical point
        plt.plot(-1, 0, 'ro', markersize=8, label='Critical point (-1, 0)')
        
        # Add grid and labels
        plt.grid(True, alpha=0.3)
        plt.axhline(y=0, color='k', linewidth=0.5)
        plt.axvline(x=0, color='k', linewidth=0.5)
        plt.xlabel('x', fontsize=12)
        plt.ylabel('f(x)', fontsize=12)
        plt.title(f'Graph of f(x) = {func}', fontsize=14, fontweight='bold')
        plt.legend(fontsize=10)
        
        # Set reasonable axis limits
        plt.xlim(-5, 3)
        plt.ylim(-0.5, 10)
        
        # Add annotations
        plt.annotate('Vertex (minimum)\nat (-1, 0)', 
                    xy=(-1, 0), xytext=(-3, 2),
                    arrowprops=dict(arrowstyle='->', color='red'),
                    fontsize=10, ha='center')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Graph saved to: {save_path}")
        
        # Convert to base64 for PDF embedding
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        plt.show()
        
        print("Graph characteristics:")
        print("• Parabolic shape opening upward")
        print("• Vertex at (-1, 0)")
        print("• Decreasing on (-∞, -1)")
        print("• Increasing on (-1, +∞)")
        print("• Always non-negative")
        
        return {
            'graph_base64': img_base64,
            'characteristics': [
                'Parabolic shape opening upward',
                'Vertex at (-1, 0)',
                'Decreasing on (-∞, -1)',
                'Increasing on (-1, +∞)',
                'Always non-negative'
            ]
        }
    
    def step8_add_disclaimer(self):
        """
        Step 8: Add Disclaimer
        Include automated program disclaimer
        """
        print("\n" + "=" * 60)
        print("STEP 8: DISCLAIMER AND REFERENCES")
        print("=" * 60)
        
        disclaimer = """
DISCLAIMER:
The results presented in this analysis are generated by an automated 
mathematical program using symbolic computation. While every effort has 
been made to ensure accuracy, the results are not guaranteed to be exact 
in all cases. This analysis is intended for educational purposes.

For additional mathematical tools and applications, visit:
- Repository: https://github.com/choengrayu/mathbot
- Website: https://rayuchoeng-profolio-website.netlify.app/
- Creator: Choeng Rayu (@President_Alein)

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """.strip()
        
        print(disclaimer)

        return disclaimer

    def step9_generate_pdf_output(self, analysis_results, output_filename=None):
        """
        Step 9: Generate PDF Output
        Format output to resemble academic document structure
        """
        print("\n" + "=" * 60)
        print("STEP 9: PDF GENERATION")
        print("=" * 60)

        if not output_filename:
            output_filename = f"function_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        try:
            c = canvas.Canvas(output_filename, pagesize=A4)
            width, height = A4
            margin = 50

            # Page 1: Main Analysis
            y_position = height - 80

            # Title
            c.setFont("Helvetica-Bold", 18)
            c.drawString(margin, y_position, "Complete Function Analysis")
            y_position -= 30

            c.setFont("Helvetica", 12)
            c.drawString(margin, y_position, f"Function: f(x) = {analysis_results['function']['function_str']}")
            y_position -= 40

            # Step 1: Function and Domain
            c.setFont("Helvetica-Bold", 14)
            c.drawString(margin, y_position, "1. Function Definition and Domain")
            y_position -= 20
            c.setFont("Helvetica", 11)
            c.drawString(margin + 20, y_position, f"Function: f(x) = {analysis_results['function']['function_str']}")
            y_position -= 15
            c.drawString(margin + 20, y_position, f"Domain: {analysis_results['function']['domain']}")
            y_position -= 15
            c.drawString(margin + 20, y_position, f"Reasoning: {analysis_results['function']['reasoning']}")
            y_position -= 30

            # Step 2: Derivative
            c.setFont("Helvetica-Bold", 14)
            c.drawString(margin, y_position, "2. Derivative Analysis")
            y_position -= 20
            c.setFont("Helvetica", 11)
            c.drawString(margin + 20, y_position, f"f'(x) = {analysis_results['derivative']['simplified']}")
            y_position -= 15
            c.drawString(margin + 20, y_position, f"Factored: f'(x) = {analysis_results['derivative']['factored']}")
            y_position -= 15
            c.drawString(margin + 20, y_position, f"Differentiable on: {analysis_results['derivative']['differentiable']}")
            y_position -= 30

            # Step 3: Limits
            c.setFont("Helvetica-Bold", 14)
            c.drawString(margin, y_position, "3. Limits")
            y_position -= 20
            c.setFont("Helvetica", 11)
            c.drawString(margin + 20, y_position, f"lim(x→-∞) f(x) = {analysis_results['limits']['limit_negative_infinity']}")
            y_position -= 15
            c.drawString(margin + 20, y_position, f"lim(x→+∞) f(x) = {analysis_results['limits']['limit_positive_infinity']}")
            y_position -= 30

            # Step 4: Table of Values
            c.setFont("Helvetica-Bold", 14)
            c.drawString(margin, y_position, "4. Table of Values")
            y_position -= 20
            c.setFont("Courier", 10)
            c.drawString(margin + 20, y_position, "x     | f(x)")
            y_position -= 15
            c.drawString(margin + 20, y_position, "------|------")
            y_position -= 15

            for x_val, f_val in analysis_results['table']['table_data']:
                c.drawString(margin + 20, y_position, f"{x_val:5} | {f_val}")
                y_position -= 15
            y_position -= 20

            # Step 5: Variation Table
            c.setFont("Helvetica-Bold", 14)
            c.drawString(margin, y_position, "5. Table of Variations")
            y_position -= 20
            c.setFont("Courier", 9)
            c.drawString(margin + 20, y_position, "x     | (-∞, -1) | x = -1 | (-1, +∞)")
            y_position -= 15
            c.drawString(margin + 20, y_position, "f'(x) |    -     |   0    |    +")
            y_position -= 15
            c.drawString(margin + 20, y_position, "f(x)  |    ↘     |  min   |    ↗")
            y_position -= 30

            # Step 6: Sign Table
            c.setFont("Helvetica-Bold", 14)
            c.drawString(margin, y_position, "6. Table of Signs")
            y_position -= 20
            c.setFont("Courier", 9)
            c.drawString(margin + 20, y_position, "x     | (-∞, -1) | x = -1 | (-1, +∞)")
            y_position -= 15
            c.drawString(margin + 20, y_position, "f(x)  |    +     |   0    |    +")
            y_position -= 30

            # Add graph on new page
            c.showPage()

            # Page 2: Graph and Notes
            y_position = height - 80
            c.setFont("Helvetica-Bold", 18)
            c.drawString(margin, y_position, "Graphical Representation")
            y_position -= 40

            # Add graph if available
            if 'graph' in analysis_results and analysis_results['graph']['graph_base64']:
                try:
                    # Decode base64 image
                    img_data = base64.b64decode(analysis_results['graph']['graph_base64'])
                    img = PILImage.open(io.BytesIO(img_data))

                    # Save temporary image
                    temp_img_path = "temp_graph.png"
                    img.save(temp_img_path)

                    # Add image to PDF
                    c.drawImage(temp_img_path, margin, y_position - 400,
                              width=500, height=300, preserveAspectRatio=True)

                    # Clean up temporary image
                    os.remove(temp_img_path)

                    y_position -= 420
                except Exception as e:
                    print(f"Error adding graph to PDF: {e}")
                    c.setFont("Helvetica", 12)
                    c.drawString(margin, y_position, "Graph could not be embedded")
                    y_position -= 30

            # Graph characteristics
            c.setFont("Helvetica-Bold", 14)
            c.drawString(margin, y_position, "Graph Characteristics:")
            y_position -= 20
            c.setFont("Helvetica", 11)

            if 'graph' in analysis_results:
                for char in analysis_results['graph']['characteristics']:
                    c.drawString(margin + 20, y_position, f"• {char}")
                    y_position -= 15

            y_position -= 30

            # Disclaimer
            c.setFont("Helvetica-Bold", 12)
            c.drawString(margin, y_position, "Disclaimer:")
            y_position -= 20
            c.setFont("Helvetica", 9)

            disclaimer_lines = [
                "The results presented in this analysis are generated by an automated",
                "mathematical program using symbolic computation. While every effort has",
                "been made to ensure accuracy, the results are not guaranteed to be exact",
                "in all cases. This analysis is intended for educational purposes.",
                "",
                "For additional mathematical tools and applications:",
                "• Repository: https://github.com/choengrayu/mathbot",
                "• Website: https://rayuchoeng-profolio-website.netlify.app/",
                "• Creator: Choeng Rayu (@President_Alein)",
                "",
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            ]

            for line in disclaimer_lines:
                c.drawString(margin, y_position, line)
                y_position -= 12

            c.save()
            print(f"✅ PDF generated successfully: {output_filename}")
            return output_filename

        except Exception as e:
            print(f"❌ Error generating PDF: {e}")
            return None

    def complete_analysis(self, func_expr="x**2 + 2*x + 1", generate_pdf=True):
        """
        Complete Analysis: Execute all steps in sequence
        """
        print("🔬 COMPLETE FUNCTION ANALYSIS")
        print("Following the specified procedure for f(x) = x² + 2x + 1")
        print("=" * 80)

        analysis_results = {}

        try:
            # Step 1: Define function and domain
            analysis_results['function'] = self.step1_define_function_and_domain(func_expr)
            func = analysis_results['function']['function']

            # Step 2: Compute derivative
            analysis_results['derivative'] = self.step2_compute_derivative(func)
            derivative = analysis_results['derivative']['derivative']

            # Step 3: Evaluate limits
            analysis_results['limits'] = self.step3_evaluate_limits(func)

            # Step 4: Generate table of values
            analysis_results['table'] = self.step4_generate_table_of_values(func)

            # Step 5: Create variation table
            analysis_results['variation'] = self.step5_create_variation_table(func, derivative)

            # Step 6: Create sign table
            analysis_results['signs'] = self.step6_create_sign_table(func)

            # Step 7: Generate graph
            analysis_results['graph'] = self.step7_generate_graph(func)

            # Step 8: Add disclaimer
            analysis_results['disclaimer'] = self.step8_add_disclaimer()

            # Step 9: Generate PDF (optional)
            if generate_pdf:
                pdf_filename = self.step9_generate_pdf_output(analysis_results)
                analysis_results['pdf_filename'] = pdf_filename

            print("\n" + "=" * 80)
            print("🎉 ANALYSIS COMPLETE!")
            print("All steps have been executed successfully.")
            print("=" * 80)

            return analysis_results

        except Exception as e:
            print(f"❌ Error during analysis: {e}")
            return None

def main():
    """
    Main execution function
    Demonstrates the complete analysis procedure
    """
    print("🧮 Mathematical Function Analysis Program")
    print("Implementation following the specified procedure")
    print("=" * 80)

    # Create analyzer instance
    analyzer = CompleteFunctionAnalyzer()

    # Perform complete analysis
    results = analyzer.complete_analysis(
        func_expr="x**2 + 2*x + 1",
        generate_pdf=True
    )

    if results:
        print("\n📊 Analysis Summary:")
        print(f"• Function analyzed: f(x) = {results['function']['function_str']}")
        print(f"• Domain: {results['function']['domain']}")
        print(f"• Derivative: f'(x) = {results['derivative']['factored']}")
        print(f"• Critical points: {results['variation']['critical_points']}")
        print(f"• Zeros: {results['signs']['zeros']}")

        if 'pdf_filename' in results:
            print(f"• PDF report: {results['pdf_filename']}")

    print("\n🎓 Educational Analysis Complete!")

if __name__ == "__main__":
    main()
