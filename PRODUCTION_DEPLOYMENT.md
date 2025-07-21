# Production Deployment Guide

## 🚀 Pre-Deployment Checklist

### ✅ Core Requirements
- [ ] All dependencies installed and tested
- [ ] Environment variables configured
- [ ] API keys and secrets secured
- [ ] Database/Storage configured (if applicable)
- [ ] Monitoring and logging setup
- [ ] Security measures implemented

### 🔧 Environment Setup

#### Required Environment Variables
```bash
# AI Services
ANTHROPIC_API_KEY=your_anthropic_key
OPENROUTER_API_KEY=your_openrouter_key
AGENT_MODEL=claude-3.5-sonnet

# Authentication (Optional)
CLERK_PUBLISHABLE_KEY=your_clerk_key
CLERK_SECRET_KEY=your_clerk_secret

# Cloud Services (Optional)
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=us-east-1
S3_BUCKET=your_s3_bucket

# Modal Cloud Training (Optional)
MODAL_TOKEN_ID=your_modal_token
MODAL_TOKEN_SECRET=your_modal_secret

# GitHub Deployment (Optional)
GITHUB_TOKEN=your_github_token

# Production Settings
DEBUG=false
LOG_LEVEL=INFO
API_TIMEOUT=30
MAX_RETRIES=3
```

#### Installation
```bash
# Install from PyPI
pip install exponent-ml

# Or install from source
git clone https://github.com/yourusername/exponent-ml.git
cd exponent-ml
pip install -e .
```

## 🏃‍♂️ Quick Start

### 1. Initial Setup
```bash
# Run setup wizard
exponent setup

# Verify installation
exponent status
```

### 2. Test Core Functionality
```bash
# Test CLI
exponent --help

# Test API server
python -m exponent.api.run_server &
exponent train --project-id test --dataset data.csv
```

### 3. Verify AI Integration
```bash
# Test AI agent
exponent ask "analyze my dataset"
```

## 🔒 Security Considerations

### API Key Management
- Use environment variables for all API keys
- Never commit secrets to version control
- Use secret management services in production
- Rotate keys regularly

### Network Security
- Use HTTPS in production
- Implement rate limiting
- Add request validation
- Monitor for suspicious activity

### Data Protection
- Encrypt sensitive data at rest
- Use secure file uploads
- Implement data retention policies
- Follow GDPR/privacy regulations

## 📊 Monitoring & Logging

### Application Logs
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('exponent.log'),
        logging.StreamHandler()
    ]
)
```

### Health Checks
```bash
# API health check
curl http://localhost:5000/health

# CLI health check
exponent status
```

### Performance Monitoring
- Monitor API response times
- Track training job completion rates
- Monitor resource usage
- Set up alerts for failures

## 🚨 Error Handling

### Common Issues & Solutions

#### 1. API Connection Issues
```bash
# Check API server status
python -m exponent.api.run_server --debug

# Verify environment variables
exponent status
```

#### 2. Training Job Failures
```bash
# Check job status
exponent train --status <job_id>

# View logs
exponent train --logs <job_id>
```

#### 3. Authentication Problems
```bash
# Re-authenticate
exponent login

# Check auth status
exponent status
```

## 🔄 Deployment Strategies

### Development Environment
```bash
# Local development
python -m exponent.api.run_server --debug
exponent --help
```

### Staging Environment
```bash
# Staging setup
export DEBUG=false
export LOG_LEVEL=INFO
python -m exponent.api.run_server
```

### Production Environment
```bash
# Production setup
export DEBUG=false
export LOG_LEVEL=WARNING
export API_TIMEOUT=60
export MAX_RETRIES=5

# Run with process manager
gunicorn -w 4 -b 0.0.0.0:5000 exponent.api.server:create_app()
```

## 📈 Scaling Considerations

### Horizontal Scaling
- Use load balancers for API servers
- Implement connection pooling
- Add caching layers
- Use distributed training

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Use GPU instances for training
- Implement async processing

## 🛠️ Maintenance

### Regular Tasks
- [ ] Update dependencies monthly
- [ ] Review and rotate API keys
- [ ] Monitor disk space usage
- [ ] Check log file sizes
- [ ] Verify backup systems

### Backup Strategy
- Backup configuration files
- Backup user projects
- Backup training models
- Test restore procedures

## 🆘 Support & Troubleshooting

### Getting Help
1. Check the documentation
2. Review error logs
3. Test with minimal setup
4. Contact support team

### Debug Mode
```bash
# Enable debug mode
export DEBUG=true
export LOG_LEVEL=DEBUG

# Run with verbose output
exponent --help --verbose
```

## ✅ Post-Deployment Verification

### Functionality Tests
```bash
# Test core commands
exponent setup
exponent status
exponent analyze test.csv
exponent train --project-id test --dataset test.csv

# Test API endpoints
curl http://localhost:5000/health
curl http://localhost:5000/api/v1/training/jobs
```

### Performance Tests
- Test with large datasets
- Verify training job completion
- Check memory usage
- Monitor response times

### Security Tests
- Verify API key protection
- Test authentication flows
- Check file upload security
- Validate error handling

## 🎯 Success Metrics

### Technical Metrics
- API response time < 2 seconds
- Training job success rate > 95%
- System uptime > 99.9%
- Error rate < 1%

### User Metrics
- Successful project creation rate
- Training completion rate
- User satisfaction scores
- Support ticket volume

---

**Ready for Production!** 🚀

The Exponent-ML tool is now configured for production deployment with proper security, monitoring, and error handling. 