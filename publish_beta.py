#!/usr/bin/env python3
"""
Simple script to publish Exponent-ML to TestPyPI for beta testing
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return None

def main():
    """Main publishing workflow"""
    print("🚀 Exponent-ML Beta Publishing")
    print("=" * 40)
    
    # Check if we have the built package
    if not os.path.exists("dist"):
        print("❌ No dist directory found. Building package first...")
        result = run_command("python -m build", "Building package")
        if result is None:
            print("❌ Build failed. Exiting.")
            sys.exit(1)
    
    # Check for twine credentials
    if not os.getenv("TWINE_USERNAME") or not os.getenv("TWINE_PASSWORD"):
        print("❌ TWINE_USERNAME and TWINE_PASSWORD environment variables must be set")
        print("\n💡 To set them:")
        print("   # For TestPyPI:")
        print("   export TWINE_USERNAME=your_testpypi_username")
        print("   export TWINE_PASSWORD=your_testpypi_password")
        print("\n   # For PyPI:")
        print("   export TWINE_USERNAME=your_pypi_username")
        print("   export TWINE_PASSWORD=your_pypi_password")
        print("\n🔗 Get TestPyPI account: https://test.pypi.org/account/register/")
        print("🔗 Get PyPI account: https://pypi.org/account/register/")
        sys.exit(1)
    
    # Ask which repository to publish to
    print("\n📋 Publishing Options:")
    print("1. TestPyPI (recommended for beta testing)")
    print("2. PyPI (production)")
    
    choice = input("\nEnter your choice (1-2): ").strip()
    
    if choice == "1":
        # Publish to TestPyPI
        result = run_command(
            "twine upload --repository testpypi dist/*",
            "Uploading to TestPyPI"
        )
        
        if result:
            print("\n🎉 Successfully published to TestPyPI!")
            print("🔗 Package URL: https://test.pypi.org/project/exponent-ml/")
            print("\n📝 Installation command for testers:")
            print("   pip install --index-url https://test.pypi.org/simple/ exponent-ml")
            
    elif choice == "2":
        # Publish to PyPI
        result = run_command(
            "twine upload dist/*",
            "Uploading to PyPI"
        )
        
        if result:
            print("\n🎉 Successfully published to PyPI!")
            print("🔗 Package URL: https://pypi.org/project/exponent-ml/")
            print("\n📝 Installation command:")
            print("   pip install exponent-ml")
            
    else:
        print("❌ Invalid choice. Exiting.")
        sys.exit(1)
    
    if result:
        print("\n📋 Next Steps:")
        print("1. Share the installation command with testers")
        print("2. Monitor for issues and feedback")
        print("3. Update the package as needed")
        print("4. Publish to main PyPI when ready")
    else:
        print("\n❌ Publishing failed. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 