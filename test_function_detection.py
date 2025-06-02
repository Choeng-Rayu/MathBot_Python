#!/usr/bin/env python3
"""
Test the fixed function detection to ensure x^2 + 2*x + 1 is detected as a function
"""

from bot_handlers import BotHandlers

def test_function_detection():
    """Test that function detection works correctly"""
    print("🔍 Testing Function Detection Fix")
    print("=" * 50)
    
    # Create bot handlers instance
    bot_handlers = BotHandlers()
    
    # Test cases
    test_cases = [
        # Should be detected as FUNCTIONS
        ("x^2 + 2*x + 1", True, "Main test case"),
        ("f(x) = x^2 + 2*x + 1", True, "Explicit function notation"),
        ("y = x^2 + 3*x + 2", True, "Y equals notation"),
        ("x^3 - 3*x + 2", True, "Cubic function"),
        ("2*x + 5", True, "Linear function"),
        ("x^2", True, "Simple quadratic"),
        ("sin(x) + cos(x)", True, "Trigonometric function"),
        ("x + 1", True, "Simple linear"),
        
        # Should be detected as MATH EXPRESSIONS (not functions)
        ("2 + 3 * 4", False, "Pure arithmetic"),
        ("sin(30) + cos(45)", False, "Trig with numbers"),
        ("sqrt(16) + log(10)", False, "Functions with numbers"),
        ("(5 + 3) * 2", False, "Parentheses with numbers"),
        
        # Should be detected as NEITHER (handled by AI)
        ("Hello world", False, "Regular text"),
        ("What is the weather?", False, "Question"),
        ("12:30", False, "Time format"),
    ]
    
    print("Testing function detection:")
    print("-" * 30)
    
    all_passed = True
    
    for test_input, expected_is_function, description in test_cases:
        is_function = bot_handlers.is_function_expression(test_input)
        is_math = bot_handlers.is_math_expression(test_input)
        
        # Determine what the bot would do
        if is_function:
            action = "ANALYZE FUNCTION"
        elif is_math:
            action = "SOLVE MATH"
        else:
            action = "AI CHAT"
        
        # Check if result matches expectation
        passed = is_function == expected_is_function
        status = "✅" if passed else "❌"
        
        print(f"{status} '{test_input}' -> {action}")
        print(f"    Expected: {'FUNCTION' if expected_is_function else 'NOT FUNCTION'}")
        print(f"    Got: {'FUNCTION' if is_function else 'NOT FUNCTION'}")
        print(f"    Description: {description}")
        print()
        
        if not passed:
            all_passed = False
    
    print("=" * 50)
    print(f"Overall result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    return all_passed

def test_specific_case():
    """Test the specific case that was failing"""
    print("\n🎯 Testing Specific Case: x^2 + 2*x + 1")
    print("=" * 50)
    
    bot_handlers = BotHandlers()
    test_input = "x^2 + 2*x + 1"
    
    is_function = bot_handlers.is_function_expression(test_input)
    is_math = bot_handlers.is_math_expression(test_input)
    
    print(f"Input: {test_input}")
    print(f"is_function_expression(): {is_function}")
    print(f"is_math_expression(): {is_math}")
    print()
    
    if is_function:
        print("✅ SUCCESS! Bot will ANALYZE FUNCTION")
        print("   User will get comprehensive function analysis PDF")
    elif is_math:
        print("❌ PROBLEM! Bot will SOLVE MATH EXPRESSION")
        print("   User will get simple expression evaluation")
    else:
        print("❌ PROBLEM! Bot will use AI CHAT")
        print("   User will get conversational response")
    
    return is_function

def test_priority_order():
    """Test that function detection has priority over math expression detection"""
    print("\n🔄 Testing Priority Order")
    print("=" * 30)
    
    bot_handlers = BotHandlers()
    
    # Test cases that could be both function and math expression
    ambiguous_cases = [
        "x^2 + 2*x + 1",
        "x^3 - 3*x + 2",
        "2*x + 5",
        "x + 1"
    ]
    
    all_correct = True
    
    for case in ambiguous_cases:
        is_function = bot_handlers.is_function_expression(case)
        is_math = bot_handlers.is_math_expression(case)
        
        print(f"Testing: {case}")
        print(f"  Function: {is_function}, Math: {is_math}")
        
        if is_function:
            print(f"  ✅ Will be handled as FUNCTION (correct)")
        elif is_math:
            print(f"  ❌ Will be handled as MATH (wrong)")
            all_correct = False
        else:
            print(f"  ❌ Will be handled as AI CHAT (wrong)")
            all_correct = False
        print()
    
    return all_correct

def main():
    """Run all tests"""
    print("🧪 Function Detection Fix Test Suite")
    print("Ensuring x^2 + 2*x + 1 is detected as a function")
    print("=" * 60)
    
    # Test 1: General function detection
    test1_passed = test_function_detection()
    
    # Test 2: Specific failing case
    test2_passed = test_specific_case()
    
    # Test 3: Priority order
    test3_passed = test_priority_order()
    
    print("\n" + "=" * 60)
    print("📋 Test Results Summary:")
    print(f"✅ General Detection: {'PASSED' if test1_passed else 'FAILED'}")
    print(f"✅ Specific Case (x^2 + 2*x + 1): {'PASSED' if test2_passed else 'FAILED'}")
    print(f"✅ Priority Order: {'PASSED' if test3_passed else 'FAILED'}")
    
    overall_success = test1_passed and test2_passed and test3_passed
    
    if overall_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("The bot will now correctly detect x^2 + 2*x + 1 as a function!")
        print("\n🚀 What happens now:")
        print("1. User sends: x^2 + 2*x + 1")
        print("2. Bot detects it as a FUNCTION (not math expression)")
        print("3. Bot generates comprehensive function analysis PDF")
        print("4. User gets the complete step-by-step analysis you requested")
    else:
        print("\n❌ Some tests failed. Check the output above.")
    
    print("\n🔧 Next Steps:")
    print("1. Restart your bot: python run.py")
    print("2. Test with: x^2 + 2*x + 1")
    print("3. Verify you get function analysis (not math expression)")

if __name__ == "__main__":
    main()
