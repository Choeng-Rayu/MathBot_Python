#!/usr/bin/env python3
"""
Debug the parsing issue
"""

import re

def debug_parse_function(func_str: str):
    """Debug version of parse_function"""
    print(f"Input: '{func_str}'")
    
    # Handle common function formats first (before cleaning spaces)
    original_str = func_str
    func_str_lower = func_str.lower()
    
    print(f"Lowercase: '{func_str_lower}'")
    
    if 'f(x)=' in func_str_lower:
        print("Found f(x)= pattern")
        func_str = func_str.split('=')[1].strip()
        print(f"After split: '{func_str}'")
    elif 'y=' in func_str_lower:
        print("Found y= pattern")
        func_str = func_str.split('=')[1].strip()
        print(f"After split: '{func_str}'")
    elif 'g(x)=' in func_str_lower:
        print("Found g(x)= pattern")
        func_str = func_str.split('=')[1].strip()
        print(f"After split: '{func_str}'")
    elif 'h(x)=' in func_str_lower:
        print("Found h(x)= pattern")
        func_str = func_str.split('=')[1].strip()
        print(f"After split: '{func_str}'")
    else:
        print("No function pattern found")
    
    # Replace mathematical notation
    func_str = func_str.replace('^', '**')
    print(f"After ^ replacement: '{func_str}'")
    
    func_str = func_str.replace('π', 'pi')
    print(f"After π replacement: '{func_str}'")
    
    # Handle implicit multiplication (2x -> 2*x, 3x^2 -> 3*x^2, etc.)
    # Replace patterns like 2x, 3x, 10x with 2*x, 3*x, 10*x
    func_str = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', func_str)
    print(f"After number*letter: '{func_str}'")
    
    # Replace patterns like x2, x3 with x**2, x**3 (in case ^ was missed)
    func_str = re.sub(r'([a-zA-Z])(\d+)', r'\1**\2', func_str)
    print(f"After letter**number: '{func_str}'")
    
    # Clean up extra spaces
    func_str = func_str.replace(' ', '')
    print(f"After space removal: '{func_str}'")
    
    return func_str

def main():
    test_cases = [
        "x^2 + 2x + 1",
        "f(x) = x^2 + 2x + 1",
        "y = x^2 + 2x + 1",
    ]
    
    for case in test_cases:
        print("=" * 50)
        result = debug_parse_function(case)
        print(f"Final result: '{result}'")
        print()

if __name__ == "__main__":
    main()
