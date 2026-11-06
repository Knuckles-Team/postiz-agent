from typing import Any, Literal

from pydantic import BaseModel, Field


class PostizIntegrationCustomer(BaseModel):
    id: str
    name: str


class PostizIntegration(BaseModel):
    id: str
    name: str
    identifier: str
    picture: str | None = None
    disabled: bool = False
    profile: str | None = None
    customer: PostizIntegrationCustomer | None = None


class PostizTag(BaseModel):
    value: str
    label: str


class PostizMedia(BaseModel):
    """One media-library item attached to a post part (from an upload)."""

    id: str = Field(description="Media id returned by an upload.")
    path: str = Field(description="Media path returned by an upload.")


class PostizPostPart(BaseModel):
    """One message of a thread: the first part is the post, later parts reply to it."""

    content: str = Field(
        description="Post text (HTML allowed for long-form providers)."
    )
    id: str | None = None
    image: list[PostizMedia] = Field(
        default_factory=list, description="Images or one video, from uploads."
    )


class PostizPostItem(BaseModel):
    integration: dict[str, str] = Field(
        description="Target channel, {'id': '<integration id>'}."
    )
    value: list[PostizPostPart] = Field(min_length=1)
    group: str | None = None
    settings: dict[str, Any] | None = Field(
        default=None,
        description=(
            "Provider settings with '__type' (for X: {'__type': 'x', "
            "'who_can_reply_post': 'everyone'}); required unless type is draft."
        ),
    )


class PostizCreatePostRequest(BaseModel):
    """A post group for one or more channels; ``draft`` is the safe default."""

    type: Literal["draft", "schedule", "now"] = Field(
        default="draft",
        description="draft = store only; schedule = queue for date; now = publish now.",
    )
    date: str = Field(description="Publish date, ISO-8601 UTC.")
    shortLink: bool = False
    order: str | None = None
    inter: int | None = None
    tags: list[PostizTag] = Field(default_factory=list)
    posts: list[PostizPostItem] = Field(min_length=1)


class PostizPostIntegration(BaseModel):
    id: str
    providerIdentifier: str
    name: str
    picture: str | None = None


class PostizPost(BaseModel):
    id: str
    content: str
    publishDate: str
    releaseURL: str | None = None
    state: str  # QUEUE, PUBLISHED, ERROR, DRAFT
    integration: PostizPostIntegration


class PostizPostsResponse(BaseModel):
    posts: list[PostizPost]


class PostizNotification(BaseModel):
    id: str
    content: str
    link: str | None = None
    createdAt: str


class PostizNotificationsResponse(BaseModel):
    notifications: list[PostizNotification]
    total: int
    page: int
    limit: int
    hasMore: bool


class PostizAnalyticsDataItem(BaseModel):
    total: str
    date: str


class PostizAnalyticsData(BaseModel):
    label: str
    data: list[PostizAnalyticsDataItem]
    percentageChange: float | None = None


class PostizUploadResponse(BaseModel):
    id: str
    path: str
    name: str | None = None
    originalName: str | None = None
    thumbnail: str | None = None
    status: str | None = None
    organizationId: str | None = None
    createdAt: str | None = None
    updatedAt: str | None = None


class PostizMissingContentItem(BaseModel):
    id: str
    url: str


class PostizVideoGenerationRequest(BaseModel):
    type: str  # 'image-text-slides', 'veo3'
    output: str  # 'vertical', 'horizontal'
    customParams: dict[str, Any]


class PostizVideoGenerationResponseItem(BaseModel):
    id: str
    path: str


class PostizVideoFunctionRequest(BaseModel):
    functionName: str
    identifier: str
    params: dict[str, Any] | None = None


class PostizVoice(BaseModel):
    id: str
    name: str


class PostizVideoFunctionResponse(BaseModel):
    voices: list[PostizVoice] | None = None
