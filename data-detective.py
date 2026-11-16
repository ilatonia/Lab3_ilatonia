import csv
import sys
import os

def load_raw_data(filename):
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
    raw_tweets = []
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            if reader.fieldnames is None:
                print("Error: CSV file is empty.")
                return []
            for row in reader:
                # Skip completely empty rows
                if row is None or len(row) == 0:
                    continue
                if all((v is None or str(v).strip() == "") for v in row.values()):
                    continue
                raw_tweets.append(row)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    return raw_tweets

def get_value(tweet, *names):
    # CSV headers can be 'Text' or 'Tweet Text' etc. - find any match
    for key in tweet.keys():
        if key is None:
            continue
        low = key.strip().lower()
        for n in names:
            if low == n.lower():
                return tweet[key]
    return None

def to_int(value):
    # Safely convert Likes/Retweets to int, bad -> 0
    try:
        if value is None or str(value).strip() == "":
            return 0
        return int(float(str(value).strip()))
    except:
        return 0

def clean_data(tweets):
    """QUEST 1: Remove tweets with no Text, fix empty Likes/Retweets to 0."""
    clean = []
    bad = 0
    for tweet in tweets:
        text = get_value(tweet, "Text", "Tweet Text", "Tweet", "Content")
        if text is None or str(text).strip() == "":
            bad = bad + 1
            continue
        # Fix Likes / Retweets
        likes = get_value(tweet, "Likes", "Like", "Likes Count")
        retweets = get_value(tweet, "Retweets", "Retweet", "Retweet Count")
        # Write back using the real keys found in the file
        for key in list(tweet.keys()):
            if key and key.strip().lower() in ("likes", "like"):
                tweet[key] = str(to_int(likes))
            if key and key.strip().lower() in ("retweets", "retweet"):
                tweet[key] = str(to_int(retweets))
        clean.append(tweet)
    print(f"Quest 1: Cleaned data. {bad} bad row(s) fixed/removed.")
    print(f"Clean tweets: {len(clean)}\n")
    return clean

def find_viral_tweet(tweets):
    """QUEST 2: Loop to find highest Likes. No max() allowed."""
    if len(tweets) == 0:
        print("Quest 2: No tweets to check.")
        return None
    viral = tweets[0]
    viral_likes = to_int(get_value(viral, "Likes"))
    for tweet in tweets:
        likes = to_int(get_value(tweet, "Likes"))
        if likes > viral_likes:
            viral = tweet
            viral_likes = likes
    print("=== Quest 2: Viral Post (Most Likes) ===")
    print(f"Username: {get_value(viral, 'Username', 'User', 'Name')}")
    print(f"Likes: {viral_likes}")
    print(f"Text: {get_value(viral, 'Text', 'Tweet Text')}\n")
    return viral

def custom_sort_by_likes(tweets):
    """QUEST 3: Bubble Sort descending by Likes."""
    sorted_list = tweets[:]  # copy, don't change original
    n = len(sorted_list)
    for i in range(n):
        for j in range(0, n - i - 1):
            likes_j = to_int(get_value(sorted_list[j], "Likes"))
            likes_next = to_int(get_value(sorted_list[j + 1], "Likes"))
            if likes_j < likes_next:
                temp = sorted_list[j]
                sorted_list[j] = sorted_list[j + 1]
                sorted_list[j + 1] = temp
    return sorted_list

def search_tweets(tweets, keyword):
    """QUEST 4: Build a NEW list with matching tweets."""
    results = []
    keyword = keyword.lower()
    for tweet in tweets:
        text = get_value(tweet, "Text", "Tweet Text")
        if text is not None and keyword in str(text).lower():
            results.append(tweet)
    return results

if __name__ == "__main__":
    dataset = load_raw_data("twitter_dataset.csv")
    print(f"Loaded {len(dataset)} raw tweets.\n")

    if len(dataset) == 0:
        print("CSV is empty. Nothing to do.")
        sys.exit(0)

    clean_dataset = clean_data(dataset)

    find_viral_tweet(clean_dataset)

    sorted_tweets = custom_sort_by_likes(clean_dataset)
    print("=== Quest 3: Top 10 Most Liked Tweets ===")
    top10 = sorted_tweets[:10]
    for i in range(len(top10)):
        t = top10[i]
        print(f"{i+1}. @{get_value(t, 'Username')} - {to_int(get_value(t, 'Likes'))} likes")
        print(f"   {get_value(t, 'Text', 'Tweet Text')}")
    print()

    keyword = input("Quest 4: Enter a search word (e.g. Python): ").strip()
    if keyword == "":
        print("No keyword entered.")
    else:
        matches = search_tweets(clean_dataset, keyword)
        print(f"\nFound {len(matches)} tweet(s) containing '{keyword}':")
        for tweet in matches:
            print(f"- @{get_value(tweet, 'Username')}: {get_value(tweet, 'Text', 'Tweet Text')}")
