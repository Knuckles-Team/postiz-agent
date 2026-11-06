"""Surface contracts: tool use, links, data locations and business roles."""

from scion_sdk.surface_contracts import (
    BusinessRole,
    DataLocation,
    Refusal,
    SurfaceLink,
    ToolStep,
    ToolUseContract,
)

CONTRACTS = (
    ToolUseContract(
        task="verify-connection",
        description="Confirm the credential reaches Postiz and identify the acting user.",
        steps=(
            ToolStep(
                tool="postiz_check_connection",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="NOT_FOUND", when="the requested record does not exist"
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_get_me",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="NOT_FOUND", when="the requested record does not exist"
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_get_account_overview",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="NOT_FOUND", when="the requested record does not exist"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="manage-channels",
        description="List connected channels, read their health and posting rules, connect or remove one.",
        steps=(
            ToolStep(
                tool="postiz_list_groups",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="NOT_FOUND", when="the requested record does not exist"
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_list_integrations",
                params=("group",),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="NOT_FOUND", when="the requested record does not exist"
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_get_channel_health",
                params=("include_deleted",),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="NOT_FOUND", when="the requested record does not exist"
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_get_integration_settings",
                params=("integration_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="NOT_FOUND", when="the requested record does not exist"
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_get_integration_url",
                params=(
                    "integration",
                    "refresh",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="NOT_FOUND", when="the requested record does not exist"
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_trigger_integration_tool",
                params=(
                    "data",
                    "integration_id",
                    "method_name",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="INVALID_ARGUMENT",
                        when="the upstream system rejects the input",
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_delete_channel",
                params=(
                    "confirm",
                    "integration_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="INVALID_ARGUMENT",
                        when="the upstream system rejects the input",
                    ),
                    Refusal(
                        code="CONFIRMATION_REQUIRED",
                        when="the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="upload-campaign-media",
        description="Upload or reuse the images and videos a campaign post needs.",
        steps=(
            ToolStep(
                tool="postiz_list_media",
                params=(
                    "page",
                    "search",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="NOT_FOUND", when="the requested record does not exist"
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_upload_file",
                params=("file_path",),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="INVALID_ARGUMENT",
                        when="the upstream system rejects the input",
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_upload_file_content",
                params=(
                    "content_base64",
                    "file_name",
                    "mime_type",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="INVALID_ARGUMENT",
                        when="the upstream system rejects the input",
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_upload_from_url",
                params=("url",),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="INVALID_ARGUMENT",
                        when="the upstream system rejects the input",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="draft-and-schedule-post",
        description="Draft a post on a channel, preview it, find a slot and schedule it after approval.",
        steps=(
            ToolStep(
                tool="postiz_list_integrations",
                params=("group",),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="NOT_FOUND", when="the requested record does not exist"
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_get_integration_settings",
                params=("integration_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="NOT_FOUND", when="the requested record does not exist"
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_create_post",
                params=("request",),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="INVALID_ARGUMENT",
                        when="the upstream system rejects the input",
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_get_post_preview",
                params=("post_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="NOT_FOUND", when="the requested record does not exist"
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_find_slot",
                params=("integration_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="NOT_FOUND", when="the requested record does not exist"
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_change_post_status",
                params=(
                    "post_id",
                    "status",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="INVALID_ARGUMENT",
                        when="the upstream system rejects the input",
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_update_post_settings",
                params=(
                    "post_id",
                    "settings",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="INVALID_ARGUMENT",
                        when="the upstream system rejects the input",
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_update_release_id",
                params=(
                    "post_id",
                    "release_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="INVALID_ARGUMENT",
                        when="the upstream system rejects the input",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="review-post-comments",
        description="Collect and answer review comments on a post.",
        steps=(
            ToolStep(
                tool="postiz_list_post_comments",
                params=("post_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="NOT_FOUND", when="the requested record does not exist"
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_create_post_comment",
                params=(
                    "content",
                    "display_name",
                    "parent_id",
                    "post_id",
                    "recaptcha_token",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="INVALID_ARGUMENT",
                        when="the upstream system rejects the input",
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_get_missing_content",
                params=("post_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="NOT_FOUND", when="the requested record does not exist"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="read-content-calendar",
        description="Read the posts of a date window with their states.",
        steps=(
            ToolStep(
                tool="postiz_list_posts",
                params=(
                    "customer",
                    "end_date",
                    "start_date",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="NOT_FOUND", when="the requested record does not exist"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="cancel-post",
        description="Move a scheduled post back to draft or delete it.",
        steps=(
            ToolStep(
                tool="postiz_list_posts",
                params=(
                    "customer",
                    "end_date",
                    "start_date",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="NOT_FOUND", when="the requested record does not exist"
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_delete_post",
                params=(
                    "confirm",
                    "post_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="INVALID_ARGUMENT",
                        when="the upstream system rejects the input",
                    ),
                    Refusal(
                        code="CONFIRMATION_REQUIRED",
                        when="the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_delete_post_by_group",
                params=(
                    "confirm",
                    "group",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="INVALID_ARGUMENT",
                        when="the upstream system rejects the input",
                    ),
                    Refusal(
                        code="CONFIRMATION_REQUIRED",
                        when="the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="generate-video-and-clips",
        description="Generate a video or cut clips from a long video for a campaign.",
        steps=(
            ToolStep(
                tool="postiz_video_function",
                params=("request",),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="INVALID_ARGUMENT",
                        when="the upstream system rejects the input",
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_generate_video",
                params=("request",),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="INVALID_ARGUMENT",
                        when="the upstream system rejects the input",
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_start_clipping",
                params=(
                    "clips",
                    "fit",
                    "integrations",
                    "url",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="INVALID_ARGUMENT",
                        when="the upstream system rejects the input",
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_list_clippings",
                params=("page",),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="NOT_FOUND", when="the requested record does not exist"
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_get_clipping",
                params=("clipping_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="NOT_FOUND", when="the requested record does not exist"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="report-engagement",
        description="Read channel and post engagement and notifications after publishing.",
        steps=(
            ToolStep(
                tool="postiz_get_analytics",
                params=(
                    "date",
                    "integration_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="NOT_FOUND", when="the requested record does not exist"
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_get_post_analytics",
                params=(
                    "date",
                    "post_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="NOT_FOUND", when="the requested record does not exist"
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_list_notifications",
                params=("page",),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="NOT_FOUND", when="the requested record does not exist"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="audit-organisation",
        description="Audit users, organisation activity and a single post's lifecycle; reset credits with approval.",
        steps=(
            ToolStep(
                tool="postiz_list_users",
                params=("name",),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="NOT_FOUND", when="the requested record does not exist"
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_get_org_activity",
                params=(
                    "from_date",
                    "include_deleted",
                    "to_date",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="NOT_FOUND", when="the requested record does not exist"
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_get_post_timeline",
                params=("post_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="NOT_FOUND", when="the requested record does not exist"
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_reset_credits",
                params=("type",),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="INVALID_ARGUMENT",
                        when="the upstream system rejects the input",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="mirror-social-data-to-graph",
        description="Land channels, posts and engagement in the knowledge graph.",
        steps=(
            ToolStep(
                tool="postiz_ingest_integrations",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="INVALID_ARGUMENT",
                        when="the upstream system rejects the input",
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_ingest_posts",
                params=(
                    "customer",
                    "end_date",
                    "start_date",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="INVALID_ARGUMENT",
                        when="the upstream system rejects the input",
                    ),
                ),
            ),
            ToolStep(
                tool="postiz_ingest_analytics",
                params=(
                    "date",
                    "integration_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        code="ACCESS_DENIED",
                        when="the credential lacks access to the operation",
                    ),
                    Refusal(
                        code="INVALID_ARGUMENT",
                        when="the upstream system rejects the input",
                    ),
                ),
            ),
        ),
    ),
)

LINKS = (
    SurfaceLink(
        task="verify-connection",
        tools=(
            "postiz_check_connection",
            "postiz_get_me",
            "postiz_get_account_overview",
        ),
        prompts=(
            "postiz-operator",
            "postiz-channel-administrator",
        ),
        skills=(
            "postiz-channel-management",
            "postiz-account-administration",
            "postiz-agent-operations",
        ),
    ),
    SurfaceLink(
        task="manage-channels",
        tools=(
            "postiz_list_groups",
            "postiz_list_integrations",
            "postiz_get_channel_health",
            "postiz_get_integration_settings",
            "postiz_get_integration_url",
            "postiz_trigger_integration_tool",
            "postiz_delete_channel",
        ),
        prompts=(
            "postiz-operator",
            "postiz-channel-administrator",
        ),
        skills=("postiz-channel-management",),
    ),
    SurfaceLink(
        task="upload-campaign-media",
        tools=(
            "postiz_list_media",
            "postiz_upload_file",
            "postiz_upload_file_content",
            "postiz_upload_from_url",
        ),
        prompts=(
            "postiz-operator",
            "social_media_manager",
        ),
        skills=(
            "postiz-campaign-post-from-asset",
            "postiz-content-scheduling",
        ),
    ),
    SurfaceLink(
        task="draft-and-schedule-post",
        tools=(
            "postiz_list_integrations",
            "postiz_get_integration_settings",
            "postiz_create_post",
            "postiz_get_post_preview",
            "postiz_find_slot",
            "postiz_change_post_status",
            "postiz_update_post_settings",
            "postiz_update_release_id",
        ),
        prompts=(
            "postiz-operator",
            "social_media_manager",
        ),
        skills=(
            "postiz-campaign-post-from-asset",
            "postiz-content-scheduling",
        ),
    ),
    SurfaceLink(
        task="review-post-comments",
        tools=(
            "postiz_list_post_comments",
            "postiz_create_post_comment",
            "postiz_get_missing_content",
        ),
        prompts=(
            "postiz-operator",
            "social_media_manager",
        ),
        skills=(
            "postiz-content-scheduling",
            "postiz-campaign-post-from-asset",
        ),
    ),
    SurfaceLink(
        task="read-content-calendar",
        tools=("postiz_list_posts",),
        prompts=(
            "postiz-operator",
            "social_media_manager",
        ),
        skills=(
            "postiz-content-scheduling",
            "postiz-audience-analytics",
        ),
    ),
    SurfaceLink(
        task="cancel-post",
        tools=(
            "postiz_list_posts",
            "postiz_delete_post",
            "postiz_delete_post_by_group",
        ),
        prompts=(
            "postiz-operator",
            "social_media_manager",
        ),
        skills=("postiz-content-scheduling",),
    ),
    SurfaceLink(
        task="generate-video-and-clips",
        tools=(
            "postiz_video_function",
            "postiz_generate_video",
            "postiz_start_clipping",
            "postiz_list_clippings",
            "postiz_get_clipping",
        ),
        prompts=(
            "postiz-operator",
            "social_media_manager",
        ),
        skills=("postiz-content-scheduling",),
    ),
    SurfaceLink(
        task="report-engagement",
        tools=(
            "postiz_get_analytics",
            "postiz_get_post_analytics",
            "postiz_list_notifications",
        ),
        prompts=(
            "postiz-operator",
            "social_media_manager",
        ),
        skills=("postiz-audience-analytics",),
    ),
    SurfaceLink(
        task="audit-organisation",
        tools=(
            "postiz_list_users",
            "postiz_get_org_activity",
            "postiz_get_post_timeline",
            "postiz_reset_credits",
        ),
        prompts=(
            "postiz-operator",
            "postiz-channel-administrator",
        ),
        skills=("postiz-account-administration",),
    ),
    SurfaceLink(
        task="mirror-social-data-to-graph",
        tools=(
            "postiz_ingest_integrations",
            "postiz_ingest_posts",
            "postiz_ingest_analytics",
        ),
        prompts=(
            "postiz-operator",
            "postiz-channel-administrator",
        ),
        skills=(
            "postiz-audience-analytics",
            "postiz-channel-management",
        ),
    ),
)

LOCATIONS = (
    DataLocation(
        name="postiz-channels",
        holds=("System",),
        instance="POSTIZ_URL",
        read_tool="postiz_list_integrations",
    ),
    DataLocation(
        name="postiz-media",
        holds=("MediaItem",),
        instance="POSTIZ_URL",
        read_tool="postiz_list_media",
    ),
    DataLocation(
        name="postiz-notifications",
        holds=("Message",),
        instance="POSTIZ_URL",
        read_tool="postiz_list_notifications",
    ),
    DataLocation(
        name="postiz-posts",
        holds=("CreativeWork",),
        instance="POSTIZ_URL",
        read_tool="postiz_list_posts",
    ),
)

ROLES = (
    BusinessRole(
        name="social-media-manager",
        tasks=(
            "upload-campaign-media",
            "draft-and-schedule-post",
            "review-post-comments",
            "read-content-calendar",
            "cancel-post",
            "generate-video-and-clips",
            "report-engagement",
        ),
        description="Plans, previews, schedules and cancels campaign posts and reads their engagement.",
    ),
    BusinessRole(
        name="channel-administrator",
        tasks=(
            "verify-connection",
            "manage-channels",
            "audit-organisation",
            "mirror-social-data-to-graph",
        ),
        description="Keeps the connected social channels healthy, connected and audited.",
    ),
)
