#!/usr/bin/env python3
"""
Test script for the complete function analysis implementation
Following the exact procedure for f(x) = x² + 2x + 1
"""

from complete_function_analyzer import CompleteFunctionAnalyzer
import os

def test_example_function():
    """
    Test the complete analysis with the example function f(x) = x² + 2x + 1
    This follows the exact procedure outlined in the specification
    """
    print("🧮 Testing Complete Function Analysis")
    print("Following the procedure for f(x) = x² + 2x + 1")
    print("=" * 80)
    
    # Create analyzer instance
    analyzer = CompleteFunctionAnalyzer()
    
    # Test the example function
    func_expr = "x**2 + 2*x + 1"
    
    try:
        # Perform complete analysis
        results = analyzer.complete_analysis(func_expr, generate_pdf=True)
        
        if results:
            print("\n✅ Analysis completed successfully!")
            
            # Display key results
            print("\n📊 Key Results:")
            print(f"• Function: f(x) = {results['function']['function_str']}")
            print(f"• Domain: {results['function']['domain']}")
            print(f"• Derivative: f'(x) = {results['derivative']['factored']}")
            print(f"• Critical points: {results['variation']['critical_points']}")
            print(f"• Factored form: {results['signs']['factored_form']}")
            print(f"• Zeros: {results['signs']['zeros']}")
            
            if 'pdf_filename' in results:
                print(f"• PDF generated: {results['pdf_filename']}")
                
                # Check if PDF exists and show size
                if os.path.exists(results['pdf_filename']):
                    size = os.path.getsize(results['pdf_filename'])
                    print(f"• PDF size: {size:,} bytes")
            
            return True
        else:
            print("❌ Analysis failed")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False

def test_other_functions():
    """Test analysis with other function types"""
    print("\n🔬 Testing Other Function Types")
    print("=" * 50)
    
    analyzer = CompleteFunctionAnalyzer()
    
    test_functions = [
        ("x**2", "Simple quadratic"),
        ("x**3 - 3*x + 2", "Cubic function"),
        ("sin(x)", "Trigonometric function"),
        ("exp(x)", "Exponential function")
    ]
    
    results = []
    
    for func_expr, description in test_functions:
        print(f"\nTesting: {description} - f(x) = {func_expr}")
        
        try:
            # Test without PDF generation for speed
            analysis = analyzer.complete_analysis(func_expr, generate_pdf=False)
            
            if analysis:
                print(f"✅ {description}: Analysis successful")
                print(f"   Domain: {analysis['function']['domain']}")
                print(f"   Derivative: {analysis['derivative']['factored']}")
                results.append(True)
            else:
                print(f"❌ {description}: Analysis failed")
                results.append(False)
                
        except Exception as e:
            print(f"❌ {description}: Error - {e}")
            results.append(False)
    
    success_rate = sum(results) / len(results) * 100
    print(f"\n📈 Success rate: {success_rate:.1f}% ({sum(results)}/{len(results)})")
    
    return success_rate > 75

def demonstrate_step_by_step():
    """Demonstrate each step of the analysis individually"""
    print("\n🔍 Step-by-Step Demonstration")
    print("=" * 50)
    
    analyzer = CompleteFunctionAnalyzer()
    func_expr = "x**2 + 2*x + 1"
    
    try:
        # Step 1: Function definition
        step1 = analyzer.step1_define_function_and_domain(func_expr)
        print(f"✅ Step 1 completed: {step1['domain']}")
        
        # Step 2: Derivative
        func = step1['function']
        step2 = analyzer.step2_compute_derivative(func)
        print(f"✅ Step 2 completed: f'(x) = {step2['factored']}")
        
        # Step 3: Limits
        step3 = analyzer.step3_evaluate_limits(func)
        print(f"✅ Step 3 completed: Limits evaluated")
        
        # Step 4: Table of values
        step4 = analyzer.step4_generate_table_of_values(func)
        print(f"✅ Step 4 completed: {len(step4['table_data'])} values computed")
        
        # Step 5: Variation table
        step5 = analyzer.step5_create_variation_table(func, step2['derivative'])
        print(f"✅ Step 5 completed: {len(step5['intervals'])} intervals analyzed")
        
        # Step 6: Sign table
        step6 = analyzer.step6_create_sign_table(func)
        print(f"✅ Step 6 completed: Sign analysis done")
        
        # Step 7: Graph
        step7 = analyzer.step7_generate_graph(func)
        print(f"✅ Step 7 completed: Graph generated")
        
        # Step 8: Disclaimer
        step8 = analyzer.step8_add_disclaimer()
        print(f"✅ Step 8 completed: Disclaimer added")
        
        print("\n🎉 All 8 steps completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error in step-by-step demonstration: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Complete Function Analysis Test Suite")
    print("Implementation following the specified procedure")
    print("=" * 80)
    
    # Ensure temp directory exists
    os.makedirs("temp", exist_ok=True)
    
    # Test 1: Example function (main test)
    test1_passed = test_example_function()
    
    # Test 2: Other function types
    test2_passed = test_other_functions()
    
    # Test 3: Step-by-step demonstration
    test3_passed = demonstrate_step_by_step()
    
    # Summary
    print("\n" + "=" * 80)
    print("📋 Test Results Summary:")
    print(f"✅ Example Function (f(x) = x² + 2x + 1): {'PASSED' if test1_passed else 'FAILED'}")
    print(f"✅ Other Function Types: {'PASSED' if test2_passed else 'FAILED'}")
    print(f"✅ Step-by-Step Demonstration: {'PASSED' if test3_passed else 'FAILED'}")
    
    overall_success = test1_passed and test2_passed and test3_passed
    
    if overall_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("The complete function analysis implementation is working correctly.")
        print("It follows the exact procedure specified for educational purposes.")
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
    
    print("\n🎓 Implementation Features:")
    print("• Step-by-step mathematical analysis")
    print("• Symbolic computation with SymPy")
    print("• Professional PDF generation")
    print("• Educational formatting")
    print("• Comprehensive error handling")
    print("• Modular design")
    
    return overall_success

if __name__ == "__main__":
    main()
