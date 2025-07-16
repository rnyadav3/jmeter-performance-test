# JMeter Performance Test Automation

Automated performance testing pipeline using JMeter with GitHub Actions and Docker.

## Features

- ✅ Automated CI/CD pipeline with GitHub Actions
- 🐳 Docker containerization for consistent test environment
- 📊 HTML reports and detailed metrics
- 🔧 Configurable test parameters
- 📈 Performance threshold validation
- 🚀 Manual trigger support

## Quick Start

### Local Testing

1. **Clone and setup**:
   ```bash
   git clone <your-repo>
   cd PerformanceJmeter
   cp .env.example .env
   ```

2. **Run tests locally**:
   ```bash
   ./scripts/run-local-test.sh 10 60 5
   # Parameters: threads, duration(s), ramp-up(s)
   ```

3. **View results**:
   - HTML Report: `test-results/html-report/index.html`
   - Raw data: `test-results/results.jtl`

### CI/CD Pipeline

The pipeline automatically runs on:
- Push to `main` or `develop` branches
- Pull requests
- Manual trigger with custom parameters

**Manual trigger**:
1. Go to Actions tab in GitHub
2. Select "Performance Tests"
3. Click "Run workflow"
4. Set parameters (threads, duration)

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and modify:

```bash
THREADS=10          # Number of concurrent users
DURATION=60         # Test duration in seconds
RAMP_UP=5          # Ramp-up time in seconds
SUCCESS_THRESHOLD=95 # Minimum success rate (%)
```

### GitHub Secrets

Set these in your repository settings:

- `SLACK_WEBHOOK_URL` (optional) - For notifications
- `TEAMS_WEBHOOK_URL` (optional) - For notifications

## Test Structure

```
PerformanceJmeter/
├── .github/workflows/
│   └── performance-test.yml    # CI/CD pipeline
├── jmeter-performance-test/
│   └── jmeter/
│       └── login_lead_assignm.jmx  # JMeter test plan
├── scripts/
│   ├── run-local-test.sh       # Local test runner
│   └── parse-results.py        # Results parser
├── docker-compose.yml          # Docker configuration
├── Dockerfile                  # JMeter container
└── README.md
```

## Pipeline Features

### Automated Testing
- Runs JMeter tests in isolated containers
- Generates HTML reports and metrics
- Validates success rate thresholds
- Stores test artifacts

### Reporting
- **HTML Reports**: Visual performance dashboard
- **JTL Files**: Raw test data
- **Metrics**: Response times, throughput, success rates
- **GitHub Summary**: Quick results overview

### Failure Handling
- Fails build if success rate < 95%
- Uploads artifacts even on failure
- Detailed error reporting

## Test Customization

### Modifying Test Parameters

Edit your JMeter test plan to accept parameters:

```xml
<stringProp name="ThreadGroup.num_threads">${__P(threads,10)}</stringProp>
<stringProp name="ThreadGroup.ramp_time">${__P(rampup,5)}</stringProp>
```

### Adding New Tests

1. Create new `.jmx` files in `jmeter-performance-test/jmeter/`
2. Update `docker-compose.yml` to include new tests
3. Modify GitHub Actions workflow if needed

## Troubleshooting

### Common Issues

1. **Docker permission errors**:
   ```bash
   sudo chmod +x scripts/run-local-test.sh
   ```

2. **Test failures**:
   - Check `test-results/results.jtl` for detailed errors
   - Verify target endpoints are accessible
   - Review authentication parameters

3. **Pipeline failures**:
   - Check GitHub Actions logs
   - Verify environment variables
   - Ensure Docker image builds successfully

### Local Development

```bash
# Build container
docker build -t jmeter-test .

# Run specific test
docker run -v $(pwd)/test-results:/results jmeter-test

# Check results
python3 scripts/parse-results.py test-results/results.jtl
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add/modify tests as needed
4. Test locally before pushing
5. Submit a pull request

## License

MIT License - See LICENSE file for details