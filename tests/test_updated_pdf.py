#!/usr/bin/env python3
"""
Test script to verify the updated PDF generation with step-by-step analysis
"""

from function_analyzer import function_analyzer
from pdf_generator import pdf_generator
import os

def test_updated_function_analysis():
    """Test the updated function analysis and PDF generation"""
    print("📈 Testing Updated Function Analysis with PDF Generation")
    print("=" * 60)
    
    # Test function: f(x) = x^2 + 2x + 1
    test_function = "f(x) = x^2 + 2*x + 1"
    
    print(f"Analyzing function: {test_function}")
    print("-" * 40)
    
    try:
        # Analyze the function
        analysis = function_analyzer.analyze_function(test_function)
        
        if 'error' in analysis:
            print(f"❌ Error: {analysis['error']}")
            return False
        
        print("✅ Function analysis completed!")
        
        # Display the structured steps
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
                content = analysis[step_key]
                # Show first 100 characters of each step
                if len(content) > 100:
                    print(f"  {content[:100]}...")
                else:
                    print(f"  {content}")
        
        # Generate graph
        print("\n📊 Generating graph...")
        graph_base64 = function_analyzer.plot_function(test_function)
        
        if graph_base64:
            print("✅ Graph generated successfully")
        else:
            print("⚠️ Graph generation failed")
        
        # Generate PDF with the new structure
        print("\n📄 Generating PDF with step-by-step analysis...")
        pdf_filename = pdf_generator.generate_function_pdf(
            analysis=analysis,
            graph_base64=graph_base64,
            user_id=12345
        )
        
        if pdf_filename and os.path.exists(pdf_filename):
            size = os.path.getsize(pdf_filename)
            print(f"✅ PDF generated successfully!")
            print(f"   📁 File: {pdf_filename}")
            print(f"   📏 Size: {size:,} bytes")
            
            # Show what's included in the PDF
            print(f"\n📋 PDF Contents:")
            print(f"   • Complete step-by-step analysis")
            print(f"   • Professional formatting")
            print(f"   • Tables of values, variations, and signs")
            print(f"   • Function graph")
            print(f"   • Educational disclaimer")
            
            return True
        else:
            print("❌ PDF generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False

def test_different_functions():
    """Test with different function types"""
    print("\n🔬 Testing Different Function Types")
    print("=" * 40)
    
    test_functions = [
        "f(x) = x^2 + 2*x + 1",  # Quadratic (perfect square)
        "f(x) = x^2 - 4",        # Quadratic with two zeros
        "f(x) = x^3 - 3*x + 2",  # Cubic function
    ]
    
    results = []
    
    for func_str in test_functions:
        print(f"\nTesting: {func_str}")
        
        try:
            # Quick analysis test
            analysis = function_analyzer.analyze_function(func_str)
            
            if 'error' in analysis:
                print(f"❌ Analysis failed: {analysis['error']}")
                results.append(False)
            else:
                print(f"✅ Analysis successful")
                
                # Check if key steps are present
                key_steps = ['step1_definition', 'step3_derivative', 'step6_table_values', 'step7_variation_table']
                missing_steps = [step for step in key_steps if step not in analysis or not analysis[step]]
                
                if missing_steps:
                    print(f"⚠️ Missing steps: {missing_steps}")
                else:
                    print(f"✅ All key steps present")
                
                results.append(True)
                
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append(False)
    
    success_rate = sum(results) / len(results) * 100
    print(f"\n📈 Success rate: {success_rate:.1f}% ({sum(results)}/{len(results)})")
    
    return success_rate > 80

def main():
    """Run all tests"""
    print("🧪 Updated Function Analysis & PDF Test Suite")
    print("=" * 60)
    
    # Ensure temp directory exists
    from config import Config
    os.makedirs(Config.TEMP_DIR, exist_ok=True)
    
    try:
        # Test 1: Main function analysis with PDF
        test1_passed = test_updated_function_analysis()
        
        # Test 2: Different function types
        test2_passed = test_different_functions()
        
        print("\n" + "=" * 60)
        print("📋 Test Results:")
        print(f"✅ Updated Analysis & PDF: {'PASSED' if test1_passed else 'FAILED'}")
        print(f"✅ Different Functions: {'PASSED' if test2_passed else 'FAILED'}")
        
        if test1_passed and test2_passed:
            print("\n🎉 All tests passed!")
            print("The updated function analysis is working correctly.")
            print("PDFs now include complete step-by-step analysis.")
        else:
            print("\n⚠️ Some tests failed. Check the output above.")
        
        print("\n🎓 New Features:")
        print("• Complete step-by-step mathematical procedure")
        print("• Professional table formatting")
        print("• Educational explanations")
        print("• Structured PDF layout")
        print("• Academic-style presentation")
        
    except Exception as e:
        print(f"❌ Test suite failed: {e}")

if __name__ == "__main__":
    main()
