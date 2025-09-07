#!/usr/bin/env python3
"""
Test script for the new structured function analysis
"""

from function_analyzer import function_analyzer
from pdf_generator import pdf_generator
import os

def test_structured_analysis():
    """Test the new step-by-step function analysis"""
    print("📈 Testing Structured Function Analysis...")
    print("=" * 50)
    
    # Test function: f(x) = x^2 + 2x + 1
    test_function = "f(x) = x^2 + 2*x + 1"
    
    print(f"Analyzing function: {test_function}")
    print("-" * 30)
    
    try:
        # Analyze the function
        analysis = function_analyzer.analyze_function(test_function)
        
        if 'error' in analysis:
            print(f"❌ Error: {analysis['error']}")
            return False
        
        # Display each step
        steps = [
            ('step1_definition', 'Step 1: Function Definition'),
            ('step2_domain', 'Step 2: Domain Analysis'),
            ('step3_derivative', 'Step 3: Derivative Analysis'),
            ('step4_limits', 'Step 4: Limits Analysis'),
            ('step5_critical_points', 'Step 5: Critical Points'),
            ('step6_table_values', 'Step 6: Table of Values'),
            ('step7_variation_table', 'Step 7: Variation Table'),
            ('step8_sign_table', 'Step 8: Sign Table'),
            ('step9_intercepts', 'Step 9: Intercepts'),
            ('step10_asymptotes', 'Step 10: Asymptotes'),
            ('step11_graph_description', 'Step 11: Graph Description')
        ]
        
        for step_key, step_title in steps:
            if step_key in analysis:
                print(f"\n{step_title}:")
                print(analysis[step_key])
                print("-" * 30)
        
        # Generate graph
        print("\nGenerating graph...")
        graph_base64 = function_analyzer.plot_function(test_function)
        
        if graph_base64:
            print("✅ Graph generated successfully")
        else:
            print("⚠️ Graph generation failed")
        
        # Generate PDF
        print("\nGenerating PDF...")
        pdf_filename = pdf_generator.generate_function_pdf(
            analysis=analysis,
            graph_base64=graph_base64,
            user_id=12345
        )
        
        if pdf_filename and os.path.exists(pdf_filename):
            print(f"✅ PDF generated: {pdf_filename}")
            
            # Show PDF size
            size = os.path.getsize(pdf_filename)
            print(f"📄 PDF size: {size} bytes")
            
            # Clean up
            pdf_generator.cleanup_file(pdf_filename)
            print("✅ PDF cleaned up")
            
            return True
        else:
            print("❌ PDF generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return False

def test_multiple_functions():
    """Test analysis with different types of functions"""
    print("\n📊 Testing Multiple Function Types...")
    print("=" * 50)
    
    test_functions = [
        "f(x) = x^2 + 2*x + 1",  # Quadratic
        "f(x) = sin(x)",          # Trigonometric
        "f(x) = 1/x",             # Rational
        "f(x) = exp(x)",          # Exponential
        "f(x) = ln(x)"            # Logarithmic
    ]
    
    results = []
    
    for func in test_functions:
        print(f"\nTesting: {func}")
        try:
            analysis = function_analyzer.analyze_function(func)
            
            if 'error' in analysis:
                print(f"❌ Error: {analysis['error']}")
                results.append(False)
            else:
                print("✅ Analysis completed")
                # Show just the definition and domain
                if 'step1_definition' in analysis:
                    print(f"   {analysis['step1_definition']}")
                if 'step2_domain' in analysis:
                    print(f"   {analysis['step2_domain']}")
                results.append(True)
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            results.append(False)
    
    success_rate = sum(results) / len(results) * 100
    print(f"\n📈 Success rate: {success_rate:.1f}% ({sum(results)}/{len(results)})")
    
    return success_rate > 80

def main():
    """Run all function analysis tests"""
    print("🧪 Function Analysis Test Suite")
    print("=" * 50)
    
    # Ensure temp directory exists
    from config import Config
    os.makedirs(Config.TEMP_DIR, exist_ok=True)
    
    try:
        # Test structured analysis
        test1_passed = test_structured_analysis()
        
        # Test multiple functions
        test2_passed = test_multiple_functions()
        
        print("\n" + "=" * 50)
        print("📋 Test Results:")
        print(f"✅ Structured Analysis: {'PASSED' if test1_passed else 'FAILED'}")
        print(f"✅ Multiple Functions: {'PASSED' if test2_passed else 'FAILED'}")
        
        if test1_passed and test2_passed:
            print("\n🎉 All tests passed! Function analysis is working correctly.")
        else:
            print("\n⚠️ Some tests failed. Check the output above for details.")
        
    except Exception as e:
        print(f"❌ Test suite failed: {e}")

if __name__ == "__main__":
    main()
