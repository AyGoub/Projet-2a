# Fichiers de connexions
CONNECTIONS_FILES = {
    'followers': 'connections/followers_and_following/followers_1.json',
    'following': 'connections/followers_and_following/following.json',
    'blocked_profiles': 'connections/followers_and_following/blocked_profiles.json',
    'close_friends': 'connections/followers_and_following/close_friends.json',
    'follow_requests_received': 'connections/followers_and_following/follow_requests_you\'ve_received.json',
    'hide_story_from': 'connections/followers_and_following/hide_story_from.json',
    'pending_follow_requests': 'connections/followers_and_following/pending_follow_requests.json',
    'recent_follow_requests': 'connections/followers_and_following/recent_follow_requests.json',
    'recently_unfollowed': 'connections/followers_and_following/recently_unfollowed_accounts.json',
    'removed_suggestions': 'connections/followers_and_following/removed_suggestions.json',
}

# Fichiers d'activité
ACTIVITY_FILES = {
    'liked_posts': 'your_instagram_activity/likes/liked_posts.json',
    'liked_comments': 'your_instagram_activity/likes/liked_comments.json',
    'post_comments': 'your_instagram_activity/comments/post_comments_1.json',
    'reels_comments': 'your_instagram_activity/comments/reels_comments.json',
}

# Fichiers de contenu
CONTENT_FILES = {
    'posts': 'your_instagram_activity/content/archived_posts.json',
    'stories': 'your_instagram_activity/content/stories.json',
    'profile': 'your_instagram_activity/content/profile_photos.json',
}


# Fichiers de messages
#MESSAGES_FILES = {
#    'inbox': 'your_instagram_activity/messages/inbox/inbox_1.json',
#    'message_requests': 'your_instagram_activity/messages/message_requests/message_requests_1.json',
#}

# Fichiers de préférences
PREFERENCES_FILES = {
    'recommended_topics': 'preferences/your_topics/recommended_topics.json',
    
}

# Tous les fichiers connus
ALL_FILES = {
    **CONNECTIONS_FILES,
    **ACTIVITY_FILES,
    **CONTENT_FILES,
    **PREFERENCES_FILES
}