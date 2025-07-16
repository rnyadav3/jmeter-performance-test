#!/bin/bash

# Local JMeter test runner script
# Usage: ./scripts/run-local-test.sh [threads] [duration] [ramp-up]

THREADS=${1:-10}
DURATION=${2:-60}
RAMP_UP=${3:-5}

echo "Starting JMeter Performance Test..."
echo "Threads: $THREADS"
echo "Duration: $DURATION seconds"
echo "Ramp-up: $RAMP_UP seconds"

# Create results directory
mkdir -p test-results

# Run Docker container
docker-compose down
THREADS=$THREADS DURATION=$DURATION RAMP_UP=$RAMP_UP docker-compose up --build

echo "Test completed. Results available in test-results/"
echo "HTML Report: test-results/html-report/index.html"