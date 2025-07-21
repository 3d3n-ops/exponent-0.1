#!/usr/bin/env python3
"""
Script to publish Exponent-ML to PyPI
"""

import subprocess
import sys
import os
from pathlib import Path

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

def check_prerequisites():
    """Check if required tools are installed"""
    print("🔍 Checking prerequisites...")
    
    # Check if build tools are installed
    try:
        import build
        print("✅ build package is installed")
    except ImportError:
        print("❌ build package not found. Installing...")
        run_command("pip install build", "Installing build package")
    
    # Check if twine is installed
    try:
        import twine
        print("✅ twine package is installed")
    except ImportError:
        print("❌ twine package not found. Installing...")
        run_command("pip install twine", "Installing twine package")

def build_package():
    """Build the package"""
    print("🔨 Building package...")
    
    # Clean previous builds
    run_command("rm -rf dist/ build/ *.egg-info/", "Cleaning previous builds")
    
    # Build the package
    result = run_command("python -m build", "Building package")
    if result is None:
        return False
    
    # Check if build was successful
    dist_dir = Path("dist")
    if not dist_dir.exists():
        print("❌ Build failed - dist directory not created")
        return False
    
    files = list(dist_dir.glob("*.whl")) + list(dist_dir.glob("*.tar.gz"))
    if not files:
        print("❌ Build failed - no package files created")
        return False
    
    print(f"✅ Package built successfully: {[f.name for f in files]}")
    return True

def test_package():
    """Test the built package"""
    print("🧪 Testing package...")
    
    # Install the package in a test environment
    result = run_command("pip install dist/*.whl --force-reinstall", "Installing package for testing")
    if result is None:
        return False
    
    # Test basic import
    try:
        import exponent
        print("✅ Package imports successfully")
    except ImportError as e:
        print(f"❌ Package import failed: {e}")
        return False
    
    # Test CLI command
    result = run_command("exponent --help", "Testing CLI command")
    if result is None:
        return False
    
    print("✅ Package testing completed successfully")
    return True

def publish_to_test_pypi():
    """Publish to TestPyPI"""
    print("🚀 Publishing to TestPyPI...")
    
    # Check if TWINE_USERNAME and TWINE_PASSWORD are set
    if not os.getenv("TWINE_USERNAME") or not os.getenv("TWINE_PASSWORD"):
        print("❌ TWINE_USERNAME and TWINE_PASSWORD environment variables must be set")
        print("💡 Set them with:")
        print("   export TWINE_USERNAME=your_username")
        print("   export TWINE_PASSWORD=your_password")
        return False
    
    # Upload to TestPyPI
    result = run_command(
        "twine upload --repository testpypi dist/*",
        "Uploading to TestPyPI"
    )
    
    if result is None:
        return False
    
    print("✅ Package published to TestPyPI successfully!")
    print("🔗 TestPyPI URL: https://test.pypi.org/project/exponent-ml/")
    return True

def publish_to_pypi():
    """Publish to PyPI"""
    print("🚀 Publishing to PyPI...")
    
    # Check if TWINE_USERNAME and TWINE_PASSWORD are set
    if not os.getenv("TWINE_USERNAME") or not os.getenv("TWINE_PASSWORD"):
        print("❌ TWINE_USERNAME and TWINE_PASSWORD environment variables must be set")
        return False
    
    # Upload to PyPI
    result = run_command(
        "twine upload dist/*",
        "Uploading to PyPI"
    )
    
    if result is None:
        return False
    
    print("✅ Package published to PyPI successfully!")
    print("🔗 PyPI URL: https://pypi.org/project/exponent-ml/")
    return True

def main():
    """Main publishing workflow"""
    print("🚀 Exponent-ML Publishing Script")
    print("=" * 50)
    
    # Check prerequisites
    check_prerequisites()
    
    # Build package
    if not build_package():
        print("❌ Build failed. Exiting.")
        sys.exit(1)
    
    # Test package
    if not test_package():
        print("❌ Package testing failed. Exiting.")
        sys.exit(1)
    
    # Ask user which repository to publish to
    print("\n📋 Publishing Options:")
    print("1. TestPyPI (recommended for testing)")
    print("2. PyPI (production)")
    print("3. Both")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    success = True
    
    if choice == "1":
        success = publish_to_test_pypi()
    elif choice == "2":
        success = publish_to_pypi()
    elif choice == "3":
        success = publish_to_test_pypi() and publish_to_pypi()
    else:
        print("❌ Invalid choice. Exiting.")
        sys.exit(1)
    
    if success:
        print("\n🎉 Publishing completed successfully!")
        print("\n📝 Next steps:")
        print("1. Test the package: pip install --index-url https://test.pypi.org/simple/ exponent-ml")
        print("2. Share with testers")
        print("3. Monitor for issues")
        print("4. Publish to main PyPI when ready")
    else:
        print("\n❌ Publishing failed. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 