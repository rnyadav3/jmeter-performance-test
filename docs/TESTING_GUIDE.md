# Performance Testing Guide

## Table of Contents
1. [Overview](#overview)
2. [Test Environment Setup](#test-environment-setup)
3. [Test Execution](#test-execution)
4. [Results Analysis](#results-analysis)
5. [Performance Metrics](#performance-metrics)
6. [CI/CD Integration](#cicd-integration)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)
9. [FAQ](#faq)

---

## Overview

This guide provides comprehensive instructions for running performance tests using our automated JMeter pipeline. The testing framework supports both local execution and CI/CD integration.

### Test Scope
- **Login API Performance**: Tests authentication endpoint response times
- **Lead Assignment API**: Validates capacity management API performance
- **Load Testing**: Simulates concurrent user behavior
- **Stress Testing**: Identifies system breaking points

### Key Features
- Automated test execution via GitHub Actions
- Docker containerization for consistent environments
- HTML reporting with detailed metrics
- Configurable load patterns
- Performance threshold validation

---

## Test Environment Setup

### Prerequisites

#### Local Development
```bash
# Required software
- Docker Desktop
- Git
- Python 3.8+ (for results parsing)
- Web browser (for viewing reports)

# Optional
- JMeter GUI (for test plan modifications)
- VS Code with JMeter extension
```

#### CI/CD Environment
```bash
# GitHub repository settings
- Actions enabled
- Secrets configured (if needed)
- Branch protection rules (optional)
```

### Initial Setup

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd PerformanceJmeter
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Verify Setup**
   ```bash
   docker --version
   docker-compose --version
   ./scripts/run-local-test.sh --help
   ```

---

## Test Execution

### Local Testing

#### Basic Test Run
```bash
# Default settings (10 threads, 60 seconds)
./scripts/run-local-test.sh

# Custom parameters
./scripts/run-local-test.sh 20 120 10
# Parameters: threads, duration(s), ramp-up(s)
```

#### Docker Compose Method
```bash
# Set environment variables
export THREADS=15
export DURATION=90
export RAMP_UP=5

# Run tests
docker-compose up --build

# Clean up
docker-compose down
```

#### Manual Docker Run
```bash
# Build container
docker build -t jmeter-perf-test .

# Run with custom parameters
docker run -v $(pwd)/test-results:/results \
  -e THREADS=10 \
  -e DURATION=60 \
  jmeter-perf-test
```

### CI/CD Testing

#### Automatic Triggers
Tests run automatically on:
- Push to `main` or `develop` branches
- Pull request creation/updates
- Scheduled runs (if configured)

#### Manual Triggers
1. Navigate to **Actions** tab in GitHub
2. Select **Performance Tests** workflow
3. Click **Run workflow**
4. Configure parameters:
   - **Test Duration**: 60-300 seconds
   - **Thread Count**: 1-100 users
   - **Branch**: Select target branch

#### Workflow Parameters
```yaml
# Available inputs
test_duration: "60"     # Test duration in seconds
thread_count: "10"      # Number of concurrent users
```

---

## Results Analysis

### HTML Reports

#### Accessing Reports
```bash
# Local testing
open test-results/html-report/index.html

# CI/CD artifacts
# Download from GitHub Actions > Artifacts > performance-report
```

#### Report Sections
1. **Dashboard**: Overall test summary
2. **Aggregate Report**: Per-request statistics
3. **View Results Tree**: Individual request details
4. **Response Times Over Time**: Performance timeline
5. **Throughput Over Time**: Request rate analysis

### Raw Data Analysis

#### JTL File Structure
```csv
timeStamp,elapsed,label,responseCode,responseMessage,threadName,dataType,success,failureMessage,bytes,sentBytes,grpThreads,allThreads,URL,Filename,latency,connect,encoding,sampleCount,errorCount,hostname,idleTime
```

#### Python Results Parser
```bash
# Parse results
python3 scripts/parse-results.py test-results/results.jtl

# Output includes:
# - Success rate
# - Response time percentiles
# - Throughput metrics
# - Error analysis
```

### GitHub Actions Summary

#### Metrics Displayed
- Total/Failed requests
- Success rate percentage
- Average response time
- Performance trend indicators

#### Status Indicators
- ✅ **Pass**: Success rate ≥ 95%
- ❌ **Fail**: Success rate < 95%
- ⚠️ **Warning**: Performance degradation detected

---

## Performance Metrics

### Key Performance Indicators (KPIs)

#### Response Time Metrics
```
- Average Response Time: Overall mean response time
- Median Response Time: 50th percentile
- 90th Percentile: 90% of requests complete within this time
- 95th Percentile: 95% of requests complete within this time
- 99th Percentile: 99% of requests complete within this time
```

#### Throughput Metrics
```
- Requests per Second: Number of requests processed per second
- Transactions per Second: Business transactions completed per second
- Bandwidth: Data transferred per second
```

#### Error Metrics
```
- Error Rate: Percentage of failed requests
- Error Types: HTTP status codes and failure reasons
- Error Distribution: Errors by request type
```

### Performance Thresholds

#### Default Thresholds
```yaml
Success Rate: ≥ 95%
Average Response Time: ≤ 2000ms
95th Percentile: ≤ 3000ms
Error Rate: ≤ 5%
```

#### Custom Thresholds
```bash
# Edit .env file
SUCCESS_THRESHOLD=98
RESPONSE_TIME_THRESHOLD=1500
ERROR_RATE_THRESHOLD=2
```

### Baseline Performance

#### Login API Benchmarks
```
Expected Response Time: 200-500ms
Concurrent Users: 50-100
Success Rate: > 99%
```

#### Lead Assignment API Benchmarks
```
Expected Response Time: 100-300ms
Concurrent Users: 20-50
Success Rate: > 98%
```

---

## CI/CD Integration

### GitHub Actions Workflow

#### Workflow Triggers
```yaml
# Automatic triggers
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  
# Manual trigger
  workflow_dispatch:
    inputs:
      test_duration: "60"
      thread_count: "10"
```

#### Workflow Steps
1. **Environment Setup**: Install JMeter and dependencies
2. **Test Execution**: Run performance tests
3. **Results Processing**: Generate reports and metrics
4. **Artifact Upload**: Store results for download
5. **Validation**: Check performance thresholds

### Integration with Other Tools

#### Slack Notifications
```yaml
# Add to workflow
- name: Notify Slack
  if: always()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
```

#### Datadog Integration
```yaml
# Add to workflow
- name: Send metrics to Datadog
  run: |
    curl -X POST "https://api.datadoghq.com/api/v1/series" \
      -H "Content-Type: application/json" \
      -H "DD-API-KEY: ${{ secrets.DATADOG_API_KEY }}" \
      -d @metrics.json
```

---

## Troubleshooting

### Common Issues

#### Test Execution Failures

**Issue**: Tests fail to start
```bash
# Check Docker status
docker ps
docker logs <container-id>

# Verify test files
ls -la jmeter-performance-test/jmeter/
```

**Issue**: Connection timeouts
```bash
# Check network connectivity
ping v3-staging.internal-fp.com
curl -I https://v3-staging.internal-fp.com/api/v4/login

# Verify firewall rules
# Contact network administrator if needed
```

#### Results Analysis Issues

**Issue**: Empty or corrupted JTL files
```bash
# Check file permissions
ls -la test-results/
chmod 755 test-results/

# Verify JMeter configuration
grep -n "filename" jmeter-performance-test/jmeter/*.jmx
```

**Issue**: HTML report generation fails
```bash
# Check JMeter version compatibility
jmeter --version

# Verify output directory
mkdir -p test-results/html-report
```

#### CI/CD Pipeline Issues

**Issue**: GitHub Actions workflow fails
```bash
# Check workflow syntax
yamllint .github/workflows/performance-test.yml

# Verify secrets and variables
# GitHub Settings > Secrets and Variables
```

**Issue**: Artifact upload problems
```bash
# Check artifact size limits
du -sh test-results/

# Verify upload permissions
# Check repository settings
```

### Debugging Steps

#### Local Debugging
```bash
# Enable verbose logging
export JMETER_OPTS="-Dlog4j.configuration=log4j2.xml"

# Run with debug output
docker-compose up --build --verbose

# Check container logs
docker logs jmeter-performance-test
```

#### CI/CD Debugging
```bash
# Add debug steps to workflow
- name: Debug Environment
  run: |
    echo "Current directory: $(pwd)"
    ls -la
    docker --version
    jmeter --version
```

### Performance Issues

#### High Response Times
1. Check target server load
2. Verify network latency
3. Review test configuration
4. Consider gradual load increase

#### Low Throughput
1. Increase thread count gradually
2. Check connection pooling
3. Verify keep-alive settings
4. Review server capacity

---

## Best Practices

### Test Design

#### Load Pattern Design
```bash
# Gradual ramp-up
RAMP_UP=30  # For 100 users over 30 seconds

# Sustained load
DURATION=300  # 5 minutes of steady state

# Realistic user behavior
# Include think time between requests
```

#### Test Data Management
```bash
# Use parameterized data
# Store test data in CSV files
# Implement data rotation
# Clean up after tests
```

### Performance Testing Strategy

#### Test Types
1. **Smoke Tests**: Basic functionality with minimal load
2. **Load Tests**: Expected production load
3. **Stress Tests**: Beyond normal capacity
4. **Spike Tests**: Sudden load increases

#### Test Scheduling
```bash
# Development: On every commit
# Staging: Daily automated runs
# Production: Weekly scheduled tests
# Release: Full test suite before deployment
```

### Monitoring and Alerting

#### Key Metrics to Monitor
- Response time trends
- Error rate changes
- Throughput variations
- Resource utilization

#### Alert Thresholds
```yaml
Critical: Success rate < 90%
Warning: Response time > 150% of baseline
Info: Throughput deviation > 20%
```

### Test Environment Management

#### Environment Isolation
- Use dedicated test environments
- Avoid production data
- Implement proper cleanup
- Monitor resource usage

#### Version Control
```bash
# Tag test configurations
git tag -a v1.0-perf-test -m "Performance test baseline"

# Track test results
# Store baseline metrics
# Version test data
```

---

## FAQ

### General Questions

**Q: How often should performance tests run?**
A: Run smoke tests on every commit, full load tests daily, and comprehensive stress tests weekly or before major releases.

**Q: What's the difference between load and stress testing?**
A: Load testing validates performance under expected conditions, while stress testing identifies breaking points and system limits.

**Q: How do I determine the right number of threads?**
A: Start with expected concurrent users, then gradually increase to find optimal performance and breaking points.

### Technical Questions

**Q: Can I run tests against production?**
A: Only run read-only tests against production, and ensure proper monitoring and safeguards are in place.

**Q: How do I add new test scenarios?**
A: Create new JMX files in the jmeter directory, update docker-compose.yml, and modify the workflow if needed.

**Q: What if my test requires authentication?**
A: Update the JMX file with proper authentication headers, and store sensitive data in environment variables or secrets.

### Troubleshooting Questions

**Q: Tests are failing with 403 errors**
A: Check authentication credentials, API permissions, and rate limiting configuration.

**Q: Results show high response times**
A: Verify network connectivity, server capacity, and test configuration. Consider reducing load or increasing ramp-up time.

**Q: Docker container won't start**
A: Check Docker daemon status, available resources, and container logs for specific error messages.

---

## Support and Resources

### Documentation
- [JMeter User Manual](https://jmeter.apache.org/usermanual/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Compose Reference](https://docs.docker.com/compose/)

### Internal Resources
- Performance testing Slack channel: #performance-testing
- Wiki: Performance Testing Guidelines
- Monitoring dashboard: [Performance Metrics](internal-link)

### Contact Information
- Performance Team: performance-team@company.com
- DevOps Support: devops@company.com
- Emergency: On-call rotation (see PagerDuty)

---

*Last updated: $(date)*
*Version: 1.0*