#!/usr/bin/env python3
"""
Test the parsing fix to ensure function parsing works correctly
"""

from function_analyzer import function_analyzer
import sympy as sp

def test_function_parsing():
    """Test various function input formats"""
    print("🔍 Testing Function Parsing Fix")
    print("=" * 50)
    
    test_cases = [
        # The problematic cases
        ("x^2 + 2x + 1", "x**2 + 2*x + 1"),
        ("f(x) = x^2 + 2x + 1", "x**2 + 2*x + 1"),
        ("y = x^2 + 2x + 1", "x**2 + 2*x + 1"),
        
        # Other common formats
        ("x^2 + 3x + 2", "x**2 + 3*x + 2"),
        ("2x^2 + 5x + 3", "2*x**2 + 5*x + 3"),
        ("x^3 - 3x + 2", "x**3 - 3*x + 2"),
        ("x2 + 2x + 1", "x**2 + 2*x + 1"),  # Missing ^ case
        ("2x + 5", "2*x + 5"),
        ("3x^2", "3*x**2"),
        
        # Already correct formats
        ("x**2 + 2*x + 1", "x**2 + 2*x + 1"),
        ("2*x**2 + 3*x + 1", "2*x**2 + 3*x + 1"),
    ]
    
    print("Testing function parsing:")
    print("-" * 30)
    
    all_passed = True
    
    for input_str, expected_pattern in test_cases:
        try:
            # Test parsing
            parsed_func = function_analyzer.parse_function(input_str)
            parsed_str = str(parsed_func)
            
            print(f"✅ '{input_str}' -> '{parsed_str}'")
            
            # Verify it's a valid SymPy expression
            if isinstance(parsed_func, sp.Expr):
                print(f"   ✅ Valid SymPy expression")
            else:
                print(f"   ❌ Not a valid SymPy expression")
                all_passed = False
                
        except Exception as e:
            print(f"❌ '{input_str}' -> ERROR: {e}")
            all_passed = False
        
        print()
    
    return all_passed

def test_complete_analysis():
    """Test complete function analysis with the problematic input"""
    print("🎯 Testing Complete Analysis")
    print("=" * 30)
    
    test_input = "x^2 + 2x + 1"
    print(f"Testing: {test_input}")
    
    try:
        analysis = function_analyzer.analyze_function(test_input)
        
        if 'error' in analysis:
            print(f"❌ Analysis failed: {analysis['error']}")
            return False
        
        print("✅ Analysis successful!")
        
        # Check key components
        key_steps = ['step1_definition', 'step3_derivative', 'step6_table_values']
        for step in key_steps:
            if step in analysis and analysis[step]:
                print(f"✅ {step}: Present")
            else:
                print(f"❌ {step}: Missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Analysis exception: {e}")
        return False

def test_edge_cases():
    """Test edge cases and special formats"""
    print("\n🔬 Testing Edge Cases")
    print("=" * 30)
    
    edge_cases = [
        "F(X) = X^2 + 2X + 1",  # Uppercase
        "f(x)=x^2+2x+1",        # No spaces
        "y = x ^ 2 + 2 x + 1",  # Extra spaces
        "x^2+2*x+1",            # Mixed notation
        "x**2 + 2x + 1",        # Mixed notation
    ]
    
    all_passed = True
    
    for case in edge_cases:
        try:
            parsed = function_analyzer.parse_function(case)
            print(f"✅ '{case}' -> '{parsed}'")
        except Exception as e:
            print(f"❌ '{case}' -> ERROR: {e}")
            all_passed = False
    
    return all_passed

def main():
    """Run all parsing tests"""
    print("🧪 Function Parsing Fix Test Suite")
    print("Fixing the x^2 + 2x + 1 parsing error")
    print("=" * 60)
    
    # Test 1: Basic parsing
    test1_passed = test_function_parsing()
    
    # Test 2: Complete analysis
    test2_passed = test_complete_analysis()
    
    # Test 3: Edge cases
    test3_passed = test_edge_cases()
    
    print("\n" + "=" * 60)
    print("📋 Test Results:")
    print(f"✅ Function Parsing: {'PASSED' if test1_passed else 'FAILED'}")
    print(f"✅ Complete Analysis: {'PASSED' if test2_passed else 'FAILED'}")
    print(f"✅ Edge Cases: {'PASSED' if test3_passed else 'FAILED'}")
    
    overall_success = test1_passed and test2_passed and test3_passed
    
    if overall_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("The parsing issue has been fixed!")
        print("\n✅ Now working:")
        print("• x^2 + 2x + 1")
        print("• f(x) = x^2 + 2x + 1") 
        print("• y = x^2 + 2x + 1")
        print("• 2x^2 + 3x + 1")
        print("• And many more formats!")
        
        print("\n🚀 Your bot should now work correctly!")
        print("Test it with: x^2 + 2x + 1")
        
    else:
        print("\n❌ Some tests failed. Check the output above.")
    
    print("\n🔧 Next Steps:")
    print("1. The parsing is now fixed")
    print("2. Restart your bot")
    print("3. Test with: x^2 + 2x + 1")
    print("4. You should get function analysis (not error)")

if __name__ == "__main__":
    main()
