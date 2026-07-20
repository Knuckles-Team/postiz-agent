from typing import Any

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
    id: str
    path: str


class PostizPostPart(BaseModel):
    content: str
    id: str | None = None
    image: list[PostizMedia] = Field(default_factory=list)


class PostizPostItem(BaseModel):
    integration: dict[str, str] = Field(
        description="Integration ID e.g., {'id': '...'} "
    )
    value: list[PostizPostPart]
    group: str | None = None
    settings: dict[str, Any] | None = None


class PostizCreatePostRequest(BaseModel):
    type: str = "schedule"  # 'draft', 'schedule', 'now'
    date: str
    shortLink: bool = False
    order: str | None = None
    inter: int | None = None
    tags: list[PostizTag] = Field(default_factory=list)
    posts: list[PostizPostItem] | None = None


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
