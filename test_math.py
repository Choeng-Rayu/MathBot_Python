#!/usr/bin/env python3
"""
Test script for mathematical functions
"""

from math_solver import math_solver
from function_analyzer import function_analyzer
from pdf_generator import pdf_generator
import os

def test_math_solver():
    """Test the math solver functionality"""
    print("🧮 Testing Math Solver...")
    print("-" * 30)
    
    test_expressions = [
        "2^3 + log(100) + sin(pi/2)",
        "sqrt(16) * cos(0) + 5!",
        "exp(2) - ln(10) + abs(-5)",
        "tan(pi/4) + log10(1000)",
        "2*pi*sin(pi/6)",
        "invalid_expression_test"
    ]
    
    for expr in test_expressions:
        print(f"\nExpression: {expr}")
        success, result, steps = math_solver.solve_expression(expr)
        
        if success:
            print(f"✅ Result: {result}")
            if steps:
                print(f"📝 Steps: {steps}")
        else:
            print(f"❌ Error: {result}")
    
    print("\n" + "=" * 50)

def test_function_analyzer():
    """Test the function analyzer functionality"""
    print("📈 Testing Function Analyzer...")
    print("-" * 30)
    
    test_functions = [
        "f(x) = x^2 + 2*x + 1",
        "y = sin(x) + cos(x)",
        "f(x) = ln(x) + x^3",
        "y = 1/x + x^2",
        "f(x) = exp(x) - x^2"
    ]
    
    for func in test_functions:
        print(f"\nFunction: {func}")
        try:
            analysis = function_analyzer.analyze_function(func)
            
            if 'error' in analysis:
                print(f"❌ Error: {analysis['error']}")
            else:
                print(f"✅ Domain: {analysis.get('domain', 'N/A')}")
                print(f"✅ Derivative: {analysis.get('derivative', 'N/A')}")
                print(f"✅ Critical points: {len(analysis.get('critical_points', []))}")
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    print("\n" + "=" * 50)

def test_pdf_generation():
    """Test PDF generation"""
    print("📄 Testing PDF Generation...")
    print("-" * 30)
    
    # Test math PDF
    print("\nTesting math expression PDF...")
    try:
        pdf_file = pdf_generator.generate_math_pdf(
            expression="2^3 + log(100)",
            result="11.0",
            steps="Step 1: 2^3 = 8\nStep 2: log(100) = 2\nStep 3: 8 + 2 = 10",
            user_id=12345
        )
        
        if pdf_file and os.path.exists(pdf_file):
            print(f"✅ Math PDF generated: {pdf_file}")
            pdf_generator.cleanup_file(pdf_file)
            print("✅ PDF cleaned up successfully")
        else:
            print("❌ Failed to generate math PDF")
    except Exception as e:
        print(f"❌ Error generating math PDF: {e}")
    
    # Test function PDF
    print("\nTesting function analysis PDF...")
    try:
        analysis = {
            'function': 'x^2 + 2*x + 1',
            'domain': 'ℝ (all real numbers)',
            'derivative': "f'(x) = 2*x + 2",
            'limits': {
                'positive_infinity': 'lim(x→+∞) f(x) = +∞',
                'negative_infinity': 'lim(x→-∞) f(x) = +∞'
            },
            'critical_points': ['x = -1, f(-1) = 0'],
            'sign_table': 'f\'(x) changes sign at x = -1',
            'variation_table': 'Function decreases then increases'
        }
        
        pdf_file = pdf_generator.generate_function_pdf(
            analysis=analysis,
            user_id=12345
        )
        
        if pdf_file and os.path.exists(pdf_file):
            print(f"✅ Function PDF generated: {pdf_file}")
            pdf_generator.cleanup_file(pdf_file)
            print("✅ PDF cleaned up successfully")
        else:
            print("❌ Failed to generate function PDF")
    except Exception as e:
        print(f"❌ Error generating function PDF: {e}")
    
    print("\n" + "=" * 50)

def test_graph_generation():
    """Test graph generation"""
    print("📊 Testing Graph Generation...")
    print("-" * 30)
    
    test_functions = [
        "x^2 + 2*x + 1",
        "sin(x)",
        "exp(x)"
    ]
    
    for func in test_functions:
        print(f"\nTesting graph for: {func}")
        try:
            graph_base64 = function_analyzer.plot_function(func)
            
            if graph_base64:
                print(f"✅ Graph generated (length: {len(graph_base64)} chars)")
            else:
                print("❌ Failed to generate graph")
        except Exception as e:
            print(f"❌ Error generating graph: {e}")
    
    print("\n" + "=" * 50)

def main():
    """Run all tests"""
    print("🧪 MathBot Component Tests")
    print("=" * 50)

    # Ensure temp directory exists
    from config import Config
    os.makedirs(Config.TEMP_DIR, exist_ok=True)

    try:
        test_math_solver()
        test_function_analyzer()
        test_graph_generation()
        test_pdf_generation()

        print("🎉 All math tests completed!")
        print("💡 To test AI functionality, run: python test_ai.py")
        print("Check the output above for any errors.")

    except Exception as e:
        print(f"❌ Test suite failed: {e}")

if __name__ == "__main__":
    main()
