import csv
import sys
import os

def load_raw_data(filename):
    """
    Loads the CSV file into a list of dictionaries exactly as it is (messy).
    """
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    raw_tweets = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Skip completely empty rows
            if row is None or len(row) == 0:
                continue
            if all((v is None or str(v).strip() == "") for v in row.values()):
                continue
            raw_tweets.append(row)

    return raw_tweets

def get_value(tweet, *names):
    # Find a column even if header is 'Text' or 'Tweet Text'
    for key in tweet.keys():
        if key is None:
            continue
        low = key.strip().lower()
        for n in names:
            if low == n.lower():
                return tweet[key]
    return None

def to_int(value):
    try:
        if value is None or str(value).strip() == "":
            return 0
        return int(float(str(value).strip()))
    except:
        return 0

def clean_data(tweets):
    """
    QUEST 1: Handle missing fields.
    Check for missing text, and replace empty likes/retweets with 0.
    Return a clean list of tweets.
    """
    clean = []
    bad = 0
    for tweet in tweets:
        text = get_value(tweet, "Text", "Tweet Text", "Tweet", "Content")
        if text is None or str(text).strip() == "":
            bad = bad + 1
            continue
        # Fix empty Likes / Retweets to 0
        for key in list(tweet.keys()):
            if key and key.strip().lower() in ("likes", "like"):
                tweet[key] = str(to_int(get_value(tweet, "Likes")))
            if key and key.strip().lower() in ("retweets", "retweet"):
                tweet[key] = str(to_int(get_value(tweet, "Retweets")))
        clean.append(tweet)
    print(f"Quest 1: {bad} bad row(s) fixed/removed.")
    print(f"Clean tweets: {len(clean)}\n")
    return clean

def find_viral_tweet(tweets):
    """
    QUEST 2: Loop through the list to find the tweet with the highest 'Likes'.
    """
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
    """
    QUEST 3: Implement Bubble Sort to sort the list
    by 'Likes' in descending order.
    """
    sorted_list = tweets[:]
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
    """
    QUEST 4: Search for a keyword and extract matching tweets into a new list.
    """
    results = []
    keyword = keyword.lower()
    for tweet in tweets:
        text = get_value(tweet, "Text", "Tweet Text")
        if text is not None and keyword in str(text).lower():
            results.append(tweet)
    return results

if __name__ == "__main__":
    # Load the messy data
    dataset = load_raw_data("twitter_dataset.csv")
    print(f"Loaded {len(dataset)} raw tweets.\n")

    # Quest 1
    clean_dataset = clean_data(dataset)

    # Quest 2
    find_viral_tweet(clean_dataset)

    # Quest 3
    sorted_tweets = custom_sort_by_likes(clean_dataset)
    print("=== Quest 3: Top 10 Most Liked Tweets ===")
    top10 = sorted_tweets[:10]
    for i in range(len(top10)):
        t = top10[i]
        print(f"{i+1}. @{get_value(t, 'Username')} - {to_int(get_value(t, 'Likes'))} likes")
        print(f"   {get_value(t, 'Text', 'Tweet Text')}")
    print()

    # Quest 4
    keyword = input("Quest 4: Enter a search word (e.g. Python): ").strip()
    if keyword == "":
        print("No keyword entered.")
    else:
        matches = search_tweets(clean_dataset, keyword)
        print(f"\nFound {len(matches)} tweet(s) containing '{keyword}':")
        for tweet in matches:
            print(f"- @{get_value(tweet, 'Username')}: {get_value(tweet, 'Text', 'Tweet Text')}")
