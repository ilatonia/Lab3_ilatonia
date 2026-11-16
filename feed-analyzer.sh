#!/bin/bash
if [ -z "$1" ]; then
  echo "Usage: bash feed-analyzer.sh twitter_dataset.csv"
  exit 1
fi

if [ ! -f "$1" ]; then
  echo "Error: File '$1' not found."
  exit 1
fi

echo "=== Top 5 Most Active Users ==="
tail -n +2 "$1" | cut -d',' -f2 | sort | uniq -c | sort -nr | head -5
