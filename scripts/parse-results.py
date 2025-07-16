#!/usr/bin/env python3
"""
JMeter Results Parser
Parses JTL files and generates performance metrics
"""

import csv
import sys
import json
from datetime import datetime
import statistics

def parse_jtl_file(file_path):
    """Parse JTL file and extract performance metrics"""
    results = []
    
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                results.append({
                    'timestamp': int(row['timeStamp']),
                    'elapsed': int(row['elapsed']),
                    'label': row['label'],
                    'success': row['success'] == 'true',
                    'response_code': row['responseCode'],
                    'bytes': int(row['bytes']) if row['bytes'] else 0
                })
    except Exception as e:
        print(f"Error reading JTL file: {e}")
        return None
    
    return results

def calculate_metrics(results):
    """Calculate performance metrics from results"""
    if not results:
        return None
    
    total_requests = len(results)
    successful_requests = sum(1 for r in results if r['success'])
    failed_requests = total_requests - successful_requests
    success_rate = (successful_requests / total_requests) * 100
    
    response_times = [r['elapsed'] for r in results]
    avg_response_time = statistics.mean(response_times)
    median_response_time = statistics.median(response_times)
    min_response_time = min(response_times)
    max_response_time = max(response_times)
    
    # Calculate percentiles
    p90_response_time = statistics.quantiles(response_times, n=10)[8]  # 90th percentile
    p95_response_time = statistics.quantiles(response_times, n=20)[18]  # 95th percentile
    p99_response_time = statistics.quantiles(response_times, n=100)[98]  # 99th percentile
    
    total_bytes = sum(r['bytes'] for r in results)
    
    metrics = {
        'total_requests': total_requests,
        'successful_requests': successful_requests,
        'failed_requests': failed_requests,
        'success_rate': round(success_rate, 2),
        'avg_response_time': round(avg_response_time, 2),
        'median_response_time': round(median_response_time, 2),
        'min_response_time': min_response_time,
        'max_response_time': max_response_time,
        'p90_response_time': round(p90_response_time, 2),
        'p95_response_time': round(p95_response_time, 2),
        'p99_response_time': round(p99_response_time, 2),
        'total_bytes': total_bytes,
        'throughput': round(total_requests / ((max(r['timestamp'] for r in results) - min(r['timestamp'] for r in results)) / 1000), 2)
    }
    
    return metrics

def main():
    if len(sys.argv) != 2:
        print("Usage: python parse-results.py <jtl_file>")
        sys.exit(1)
    
    jtl_file = sys.argv[1]
    results = parse_jtl_file(jtl_file)
    
    if not results:
        print("Failed to parse results")
        sys.exit(1)
    
    metrics = calculate_metrics(results)
    
    # Print results
    print("Performance Test Results")
    print("=" * 50)
    print(f"Total Requests: {metrics['total_requests']}")
    print(f"Successful Requests: {metrics['successful_requests']}")
    print(f"Failed Requests: {metrics['failed_requests']}")
    print(f"Success Rate: {metrics['success_rate']}%")
    print(f"Average Response Time: {metrics['avg_response_time']}ms")
    print(f"Median Response Time: {metrics['median_response_time']}ms")
    print(f"90th Percentile: {metrics['p90_response_time']}ms")
    print(f"95th Percentile: {metrics['p95_response_time']}ms")
    print(f"99th Percentile: {metrics['p99_response_time']}ms")
    print(f"Min Response Time: {metrics['min_response_time']}ms")
    print(f"Max Response Time: {metrics['max_response_time']}ms")
    print(f"Throughput: {metrics['throughput']} requests/second")
    print(f"Total Data: {metrics['total_bytes']} bytes")
    
    # Save to JSON
    output_file = jtl_file.replace('.jtl', '_metrics.json')
    with open(output_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"\nDetailed metrics saved to: {output_file}")

if __name__ == "__main__":
    main()