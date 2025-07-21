# 🧪 Exponent-ML Beta Testing Guide

## 🚀 Quick Start for Beta Testers

### Installation

```bash
# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ exponent-ml

# Or install from source
git clone https://github.com/3d3n-ops/exponent-0.1.git
cd exponent-0.1
pip install -e .
```

### First-Time Setup

```bash
# Run the setup wizard
exponent setup

# Verify installation
exponent status
```

## 🎯 What to Test

### 1. **Basic Functionality**
```bash
# Test CLI commands
exponent --help
exponent status
exponent version
```

### 2. **AI Agent Integration**
```bash
# Test AI agent
exponent ask "help me analyze a dataset"
exponent ask "create a project for sentiment analysis"
```

### 3. **Dataset Analysis**
```bash
# Test dataset analysis (you'll need a CSV file)
exponent analyze your_dataset.csv
exponent analyze your_dataset.csv --prompt "Show me the data distribution"
```

### 4. **Project Creation**
```bash
# Test project creation
exponent init quick "classify emails as spam or not spam" --dataset emails.csv
```

### 5. **Training Pipeline**
```bash
# Test training (requires Modal setup)
exponent train --project-id your_project --dataset your_data.csv
```

### 6. **Deployment**
```bash
# Test GitHub deployment (requires GitHub token)
exponent deploy --project-id your_project
```

## 📊 Test Scenarios

### Scenario 1: New User Experience
1. Install the package
2. Run `exponent setup`
3. Follow the setup wizard
4. Test basic commands
5. Report any issues

### Scenario 2: Dataset Analysis
1. Prepare a CSV dataset
2. Run `exponent analyze dataset.csv`
3. Test with custom prompts
4. Check output quality
5. Report findings

### Scenario 3: End-to-End Workflow
1. Create a project
2. Upload a dataset
3. Generate training code
4. Train the model
5. Deploy to GitHub
6. Report the complete experience

### Scenario 4: Error Handling
1. Test with invalid inputs
2. Test with missing files
3. Test with network issues
4. Test with invalid API keys
5. Report error messages and recovery

## 🐛 Bug Reporting

### What to Include
- **Environment**: OS, Python version, package version
- **Steps**: Exact commands run
- **Expected**: What should happen
- **Actual**: What actually happened
- **Error Messages**: Full error output
- **Logs**: Any relevant log files

### Report Format
```
**Environment:**
- OS: Windows 10
- Python: 3.11.0
- Package: exponent-ml 0.1.2-beta

**Steps to Reproduce:**
1. Run `exponent setup`
2. Enter API key
3. Run `exponent analyze data.csv`

**Expected Behavior:**
Dataset analysis should complete successfully

**Actual Behavior:**
Error: "API key invalid"

**Error Message:**
[Include full error output]

**Additional Notes:**
[Any other relevant information]
```

## 📈 Feedback Categories

### 1. **Usability**
- Is the CLI intuitive?
- Are error messages helpful?
- Is the setup process clear?

### 2. **Functionality**
- Does the AI agent work correctly?
- Is dataset analysis accurate?
- Does training work as expected?

### 3. **Performance**
- How fast are responses?
- Does it handle large datasets?
- Are there memory issues?

### 4. **Reliability**
- Does it work consistently?
- Are there crashes or hangs?
- How does it handle errors?

### 5. **Documentation**
- Is the help text clear?
- Are examples helpful?
- Is the README comprehensive?

## 🎁 Beta Tester Benefits

### What You Get
- Early access to new features
- Direct feedback to the development team
- Recognition in the project
- Free access to premium features (when available)

### How to Contribute
1. **Test Regularly**: Use the tool for your ML projects
2. **Report Issues**: Submit detailed bug reports
3. **Suggest Features**: Share ideas for improvements
4. **Share Feedback**: Tell us what works and what doesn't

## 📞 Support

### Getting Help
- **GitHub Issues**: Report bugs and feature requests
- **Discussions**: Ask questions and share feedback
- **Email**: Contact the development team directly

### Community
- Join our Discord server (link coming soon)
- Follow us on Twitter for updates
- Star the repository to stay updated

## 🏆 Beta Tester Recognition

### Recognition Levels
- **Bronze**: 5+ bug reports or feature suggestions
- **Silver**: 10+ contributions or significant testing
- **Gold**: 20+ contributions or major feature testing

### Benefits
- Name in project acknowledgments
- Early access to new releases
- Direct communication with development team
- Special beta tester badge

---

**Thank you for helping make Exponent-ML better!** 🚀

Your feedback is invaluable in creating a tool that truly helps ML developers. 