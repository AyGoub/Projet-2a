import pandas as pd
from datetime import datetime
import json

def process_followers(data):
    if 'relationships_followers' in data:
        followers = []
        for follower in data['relationships_followers']:
            user_data = follower['string_list_data'][0]
            timestamp = datetime.fromtimestamp(user_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            followers.append({
                'timestamp': timestamp,
                'username': user_data['value'],
                'profile_url': user_data['href']
            })
        return pd.DataFrame(followers)
    return pd.DataFrame()

def process_following(data):
    if 'relationships_following' in data:
        following = []
        for follow in data['relationships_following']:
            user_data = follow['string_list_data'][0]
            timestamp = datetime.fromtimestamp(user_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            following.append({
                'timestamp': timestamp,
                'username': user_data['value'],
                'profile_url': user_data['href']
            })
        return pd.DataFrame(following)
    return pd.DataFrame()

def process_unfollowed(data):
    if 'relationships_unfollowed_users' in data:
        unfollowed = []
        for unfollow in data['relationships_unfollowed_users']:
            user_data = unfollow['string_list_data'][0]
            timestamp = datetime.fromtimestamp(user_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            unfollowed.append({
                'timestamp': timestamp,
                'username': user_data['value'],
                'profile_url': user_data['href']
            })
        return pd.DataFrame(unfollowed)
    return pd.DataFrame()

def process_follow_requests(data):
    if 'relationships_follow_requests_sent' in data:
        requests = []
        for request in data['relationships_follow_requests_sent']:
            user_data = request['string_list_data'][0]
            timestamp = datetime.fromtimestamp(user_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            requests.append({
                'timestamp': timestamp,
                'username': user_data['value'],
                'profile_url': user_data['href']
            })
        return pd.DataFrame(requests)
    return pd.DataFrame()

def analyze_connections(uploaded_files):
    connections_data = {
        'followers': None,
        'following': None,
        'unfollowed': None,
        'follow_requests': None
    }

    for file in uploaded_files:
        try:
            content = file.read()
            data = json.loads(content)
            
            file_name = file.name.lower()
            
            if 'followers' in file_name:
                connections_data['followers'] = process_followers(data)
            elif 'following' in file_name:
                connections_data['following'] = process_following(data)
            elif 'unfollowed' in file_name:
                connections_data['unfollowed'] = process_unfollowed(data)
            elif 'follow_requests' in file_name:
                connections_data['follow_requests'] = process_follow_requests(data)
            
            file.seek(0)  # Reset file pointer
            
        except Exception as e:
            print(f"Error processing {file.name}: {str(e)}")
            continue

    return connections_data