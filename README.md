# Lab 3: The Social Media Data Detective

## How to run
1. Download `twitter_dataset.csv` from Kaggle and put it in this folder.
2. Python: `python data-detective.py`
3. Shell: `bash feed-analyzer.sh twitter_dataset.csv`

## What it does
- Quest 1: Removes tweets with missing Text, fixes empty Likes/Retweets to 0.
- Quest 2: Finds viral tweet with highest Likes using a loop (no max()).
- Quest 3: Bubble Sort by Likes descending, shows Top 10 (no sort()).
- Quest 4: Searches keyword, builds a new list, prints len() of matches.
- Shell: Uses cut / sort / uniq -c / sort -nr / head to show Top 5 users.
