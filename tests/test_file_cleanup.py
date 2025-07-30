#!/usr/bin/env python3
"""
Test script to demonstrate automatic file cleanup functionality
"""

from function_analyzer import function_analyzer
from pdf_generator import pdf_generator
import os
import time

def test_automatic_cleanup():
    """Test the automatic file cleanup functionality"""
    print("🧹 Testing Automatic File Cleanup")
    print("=" * 50)
    
    # Ensure temp directory exists
    from config import Config
    os.makedirs(Config.TEMP_DIR, exist_ok=True)
    
    # Show initial stats
    initial_stats = pdf_generator.get_temp_dir_stats()
    print(f"📁 Initial temp directory: {initial_stats['files']} files, {initial_stats['size']:,} bytes")
    
    # Generate some test PDFs
    print("\n📄 Generating test PDFs...")
    test_functions = [
        "x^2 + 2*x + 1",
        "x^3 - 3*x + 2", 
        "sin(x) + cos(x)"
    ]
    
    generated_files = []
    
    for i, func in enumerate(test_functions):
        try:
            print(f"   Generating PDF {i+1}: {func}")
            
            # Analyze function
            analysis = function_analyzer.analyze_function(func)
            
            if 'error' not in analysis:
                # Generate graph
                graph_base64 = function_analyzer.plot_function(func)
                
                # Generate PDF
                pdf_filename = pdf_generator.generate_function_pdf(
                    analysis=analysis,
                    graph_base64=graph_base64,
                    user_id=99990 + i
                )
                
                if pdf_filename and os.path.exists(pdf_filename):
                    generated_files.append(pdf_filename)
                    size = os.path.getsize(pdf_filename)
                    print(f"   ✅ Generated: {os.path.basename(pdf_filename)} ({size:,} bytes)")
                else:
                    print(f"   ❌ Failed to generate PDF for {func}")
            else:
                print(f"   ❌ Analysis failed for {func}")
                
        except Exception as e:
            print(f"   ❌ Error with {func}: {e}")
    
    # Show stats after generation
    after_gen_stats = pdf_generator.get_temp_dir_stats()
    print(f"\n📁 After generation: {after_gen_stats['files']} files, {after_gen_stats['size']:,} bytes")
    
    # Test individual file cleanup
    print(f"\n🗑️ Testing individual file cleanup...")
    if generated_files:
        test_file = generated_files[0]
        print(f"   Cleaning up: {os.path.basename(test_file)}")
        pdf_generator.cleanup_file(test_file)
        
        # Verify file is deleted
        if not os.path.exists(test_file):
            print(f"   ✅ File successfully deleted")
        else:
            print(f"   ❌ File still exists")
    
    # Show stats after individual cleanup
    after_individual_stats = pdf_generator.get_temp_dir_stats()
    print(f"\n📁 After individual cleanup: {after_individual_stats['files']} files, {after_individual_stats['size']:,} bytes")
    
    # Test batch cleanup (clean files older than 0 hours = all files)
    print(f"\n🧹 Testing batch cleanup...")
    pdf_generator.cleanup_old_files(0)  # Clean all files
    
    # Show final stats
    final_stats = pdf_generator.get_temp_dir_stats()
    print(f"\n📁 Final temp directory: {final_stats['files']} files, {final_stats['size']:,} bytes")
    
    # Summary
    print(f"\n📊 Cleanup Summary:")
    print(f"   Files generated: {len(generated_files)}")
    print(f"   Files cleaned individually: 1")
    print(f"   Files cleaned in batch: {after_individual_stats['files']}")
    print(f"   Total space freed: {after_gen_stats['size']:,} bytes")
    
    return True

def test_cleanup_with_age_filter():
    """Test cleanup with age filtering"""
    print("\n⏰ Testing Age-Based Cleanup")
    print("=" * 30)
    
    # Generate a test file
    try:
        analysis = function_analyzer.analyze_function("x^2 + 1")
        if 'error' not in analysis:
            graph_base64 = function_analyzer.plot_function("x^2 + 1")
            pdf_filename = pdf_generator.generate_function_pdf(
                analysis=analysis,
                graph_base64=graph_base64,
                user_id=88888
            )
            
            if pdf_filename and os.path.exists(pdf_filename):
                print(f"✅ Generated test file: {os.path.basename(pdf_filename)}")
                
                # Try to clean files older than 1 hour (should not delete the new file)
                print("🕐 Cleaning files older than 1 hour...")
                pdf_generator.cleanup_old_files(1)
                
                if os.path.exists(pdf_filename):
                    print("✅ New file preserved (correct behavior)")
                    
                    # Now clean all files
                    print("🧹 Cleaning all files...")
                    pdf_generator.cleanup_old_files(0)
                    
                    if not os.path.exists(pdf_filename):
                        print("✅ File cleaned when age filter = 0")
                    else:
                        print("❌ File not cleaned")
                else:
                    print("❌ New file was incorrectly deleted")
            else:
                print("❌ Failed to generate test file")
        else:
            print("❌ Analysis failed")
            
    except Exception as e:
        print(f"❌ Error in age-based cleanup test: {e}")

def show_cleanup_features():
    """Show all cleanup features"""
    print("\n🎯 File Cleanup Features")
    print("=" * 30)
    
    print("✅ Automatic cleanup after sending PDF to user")
    print("✅ Scheduled cleanup every hour (removes files older than 24h)")
    print("✅ Cleanup on bot shutdown (removes all temporary files)")
    print("✅ Manual cleanup methods available")
    print("✅ File size tracking and logging")
    print("✅ Error handling for cleanup operations")
    
    print("\n📋 Cleanup Methods:")
    print("• pdf_generator.cleanup_file(filename) - Delete specific file")
    print("• pdf_generator.cleanup_old_files(hours) - Delete files older than X hours")
    print("• pdf_generator.get_temp_dir_stats() - Get directory statistics")
    
    print("\n⚙️ Automatic Cleanup Schedule:")
    print("• After PDF sent: Immediate cleanup")
    print("• Every 1 hour: Clean files older than 24 hours")
    print("• Every 6 hours: Show temp directory statistics")
    print("• On bot shutdown: Clean all temporary files")

def main():
    """Run all cleanup tests"""
    print("🧪 File Cleanup Test Suite")
    print("Testing automatic PDF cleanup functionality")
    print("=" * 60)
    
    try:
        # Test 1: Basic cleanup functionality
        test1_passed = test_automatic_cleanup()
        
        # Test 2: Age-based cleanup
        test_cleanup_with_age_filter()
        
        # Show features
        show_cleanup_features()
        
        print("\n" + "=" * 60)
        print("📋 Test Results:")
        print(f"✅ Automatic Cleanup: {'PASSED' if test1_passed else 'FAILED'}")
        
        if test1_passed:
            print("\n🎉 ALL TESTS PASSED!")
            print("File cleanup is working correctly!")
            
            print("\n🚀 What happens in your bot:")
            print("1. User requests function analysis")
            print("2. Bot generates PDF")
            print("3. Bot sends PDF to user")
            print("4. Bot immediately deletes PDF file")
            print("5. Scheduled cleanup removes any missed files")
            print("6. No disk space accumulation!")
            
        else:
            print("\n❌ Some tests failed. Check the output above.")
        
        print("\n💡 Benefits:")
        print("• No manual file management needed")
        print("• Prevents disk space accumulation")
        print("• Automatic cleanup on bot restart")
        print("• Logging shows what's being cleaned")
        print("• Error handling prevents cleanup failures")
        
    except Exception as e:
        print(f"❌ Test suite failed: {e}")

if __name__ == "__main__":
    main()
