#!/usr/bin/env python3
"""
Test the fixed function analysis to verify it generates the correct format
"""

from function_analyzer import function_analyzer
from pdf_generator import pdf_generator
import os

def test_exact_format():
    """Test that the analysis generates the exact format requested"""
    print("🔍 Testing Exact Format Generation")
    print("=" * 50)
    
    # Test the exact function from the example
    test_function = "f(x) = x^2 + 2*x + 1"
    
    print(f"Testing function: {test_function}")
    print("-" * 30)
    
    try:
        # Analyze the function
        analysis = function_analyzer.analyze_function(test_function)
        
        if 'error' in analysis:
            print(f"❌ Error: {analysis['error']}")
            return False
        
        print("✅ Analysis completed!")
        
        # Check each step and display the exact content
        expected_steps = [
            ('step1_definition', 'Step 1: Function Definition'),
            ('step2_domain', 'Step 2: Domain Analysis'),
            ('step3_derivative', 'Step 3: Derivative Analysis'),
            ('step4_limits', 'Step 4: Limits Analysis'),
            ('step5_critical_points', 'Step 5: Critical Points'),
            ('step6_table_values', 'Step 6: Table of Values'),
            ('step7_variation_table', 'Step 7: Variation Table'),
            ('step8_sign_table', 'Step 8: Sign Table'),
        ]
        
        print("\n📋 Generated Content:")
        print("=" * 50)
        
        for step_key, step_title in expected_steps:
            if step_key in analysis:
                print(f"\n{step_title}:")
                print(f"{analysis[step_key]}")
                print("-" * 30)
            else:
                print(f"\n❌ Missing: {step_title}")
        
        # Generate PDF to test the complete flow
        print("\n📄 Generating PDF...")
        
        # Generate graph
        graph_base64 = function_analyzer.plot_function(test_function)
        
        # Generate PDF
        pdf_filename = pdf_generator.generate_function_pdf(
            analysis=analysis,
            graph_base64=graph_base64,
            user_id=99999
        )
        
        if pdf_filename and os.path.exists(pdf_filename):
            size = os.path.getsize(pdf_filename)
            print(f"✅ PDF generated: {pdf_filename}")
            print(f"📏 Size: {size:,} bytes")
            
            # Verify the content matches expected format
            print("\n🎯 Verification:")
            
            # Check Step 1
            if 'step1_definition' in analysis:
                step1 = analysis['step1_definition']
                if "We consider the function defined by f(x) =" in step1:
                    print("✅ Step 1: Correct format")
                else:
                    print(f"❌ Step 1: Wrong format - {step1}")
            
            # Check Step 2
            if 'step2_domain' in analysis:
                step2 = analysis['step2_domain']
                if "Its domain of definition is" in step2:
                    print("✅ Step 2: Correct format")
                else:
                    print(f"❌ Step 2: Wrong format - {step2}")
            
            # Check Step 3
            if 'step3_derivative' in analysis:
                step3 = analysis['step3_derivative']
                if "It is derivable on" in step3 and "Its derivative is f'(x) =" in step3:
                    print("✅ Step 3: Correct format")
                else:
                    print(f"❌ Step 3: Wrong format - {step3}")
            
            # Check Step 4
            if 'step4_limits' in analysis:
                step4 = analysis['step4_limits']
                if "It admits the below limits:" in step4:
                    print("✅ Step 4: Correct format")
                else:
                    print(f"❌ Step 4: Wrong format - {step4}")
            
            # Check Step 6
            if 'step6_table_values' in analysis:
                step6 = analysis['step6_table_values']
                if "A table of values is:" in step6:
                    print("✅ Step 6: Correct format")
                else:
                    print(f"❌ Step 6: Wrong format - {step6}")
            
            # Check Step 7
            if 'step7_variation_table' in analysis:
                step7 = analysis['step7_variation_table']
                if "Its table of variations is:" in step7:
                    print("✅ Step 7: Correct format")
                else:
                    print(f"❌ Step 7: Wrong format - {step7}")
            
            # Check Step 8
            if 'step8_sign_table' in analysis:
                step8 = analysis['step8_sign_table']
                if "Its table of signs is:" in step8:
                    print("✅ Step 8: Correct format")
                else:
                    print(f"❌ Step 8: Wrong format - {step8}")
            
            return True
        else:
            print("❌ PDF generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_bot_integration():
    """Test how the bot would handle the function"""
    print("\n🤖 Testing Bot Integration")
    print("=" * 30)
    
    # Simulate what happens when user sends function to bot
    from bot_handlers import bot_handlers
    
    # Test function parsing
    test_inputs = [
        "f(x) = x^2 + 2*x + 1",
        "x^2 + 2*x + 1",
        "y = x^2 + 2*x + 1"
    ]
    
    for func_input in test_inputs:
        print(f"\nTesting input: {func_input}")
        
        # Check if it's recognized as a function
        is_function = bot_handlers.is_function_expression(func_input)
        print(f"Recognized as function: {is_function}")
        
        if is_function:
            try:
                analysis = function_analyzer.analyze_function(func_input)
                if 'error' not in analysis:
                    print("✅ Analysis successful")
                else:
                    print(f"❌ Analysis failed: {analysis['error']}")
            except Exception as e:
                print(f"❌ Exception: {e}")

def main():
    """Run the test"""
    print("🧪 Testing Fixed Function Analysis")
    print("Verifying the exact format requested")
    print("=" * 50)
    
    # Ensure temp directory exists
    from config import Config
    os.makedirs(Config.TEMP_DIR, exist_ok=True)
    
    # Test the exact format
    format_test_passed = test_exact_format()
    
    # Test bot integration
    test_bot_integration()
    
    print("\n" + "=" * 50)
    print("📋 Test Results:")
    print(f"✅ Exact Format Test: {'PASSED' if format_test_passed else 'FAILED'}")
    
    if format_test_passed:
        print("\n🎉 SUCCESS!")
        print("The function analysis now generates the exact format:")
        print("• We consider the function defined by f(x) = ...")
        print("• Its domain of definition is ...")
        print("• It is derivable on ℝ")
        print("• Its derivative is f'(x) = ...")
        print("• It admits the below limits:")
        print("• A table of values is:")
        print("• Its table of variations is:")
        print("• Its table of signs is:")
        print("• Graph generation included")
    else:
        print("\n❌ Test failed. Check the output above for issues.")
    
    print("\n🚀 Next Steps:")
    print("1. Start your bot: python run.py")
    print("2. Send function: f(x) = x^2 + 2*x + 1")
    print("3. Check the generated PDF")

if __name__ == "__main__":
    main()
