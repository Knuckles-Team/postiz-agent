"""Postiz Agent graph configuration — tag prompts and env var mappings.

Standardized graph configuration to support hierarchical and specialized domain routing.
"""

TAG_PROMPTS: dict[str, str] = {
    "integrations": "You are a Postiz Integration specialist. You can list connected social media channels and check their connection status.",
    "posts": "You are a Postiz Content specialist. You can list existing posts, create/schedule new posts across multiple platforms, and delete posts.",
    "uploads": "You are a Postiz Media specialist. You can upload images and videos to the platform for use in posts.",
    "analytics": "You are a Postiz Analytics specialist. You can retrieve performance data for the entire platform or for specific published posts.",
    "notifications": "You are a Postiz Notification specialist. You can list system and post-related notifications for the user.",
}


TAG_ENV_VARS: dict[str, str] = {
    "integrations": "INTEGRATIONSTOOL",
    "posts": "POSTSTOOL",
    "uploads": "UPLOADSTOOL",
    "analytics": "ANALYTICSTOOL",
    "notifications": "NOTIFICATIONSTOOL",
}
