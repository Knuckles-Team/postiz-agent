from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class PostizIntegrationCustomer(BaseModel):
    id: str
    name: str


class PostizIntegration(BaseModel):
    id: str
    name: str
    identifier: str
    picture: Optional[str] = None
    disabled: bool = False
    profile: Optional[str] = None
    customer: Optional[PostizIntegrationCustomer] = None
    # legacy fields for compatibility
    type: Optional[str] = None
    connected: Optional[bool] = None
    settings: Optional[Dict[str, Any]] = None


class PostizTag(BaseModel):
    value: str
    label: str


class PostizMedia(BaseModel):
    id: str
    path: str


class PostizPostPart(BaseModel):
    content: str
    id: Optional[str] = None
    image: List[PostizMedia] = Field(default_factory=list)


class PostizPostItem(BaseModel):
    integration: Dict[str, str] = Field(
        description="Integration ID e.g., {'id': '...'} "
    )
    value: List[PostizPostPart]
    group: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class PostizCreatePostRequest(BaseModel):
    type: str = "schedule"  # 'draft', 'schedule', 'now'
    date: str
    shortLink: bool = False
    order: Optional[str] = None
    inter: Optional[int] = None
    tags: List[PostizTag] = Field(default_factory=list)
    posts: Optional[List[PostizPostItem]] = None


class PostizPostIntegration(BaseModel):
    id: str
    providerIdentifier: str
    name: str
    picture: Optional[str] = None


class PostizPost(BaseModel):
    id: str
    content: str
    publishDate: str
    releaseURL: Optional[str] = None
    state: str  # QUEUE, PUBLISHED, ERROR, DRAFT
    integration: PostizPostIntegration


class PostizPostsResponse(BaseModel):
    posts: List[PostizPost]


class PostizNotification(BaseModel):
    id: str
    content: str
    link: Optional[str] = None
    createdAt: str


class PostizNotificationsResponse(BaseModel):
    notifications: List[PostizNotification]
    total: int
    page: int
    limit: int
    hasMore: bool


class PostizAnalyticsDataItem(BaseModel):
    total: str
    date: str


class PostizAnalyticsData(BaseModel):
    label: str
    data: List[PostizAnalyticsDataItem]
    percentageChange: Optional[float] = None


class PostizUploadResponse(BaseModel):
    id: str
    path: str
    name: Optional[str] = None
    organizationId: Optional[str] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None


class PostizMissingContentItem(BaseModel):
    id: str
    url: str


class PostizVideoGenerationRequest(BaseModel):
    type: str  # 'image-text-slides', 'veo3'
    output: str  # 'vertical', 'horizontal'
    customParams: Dict[str, Any]


class PostizVideoGenerationResponseItem(BaseModel):
    id: str
    path: str


class PostizVideoFunctionRequest(BaseModel):
    functionName: str
    identifier: str
    params: Optional[Dict[str, Any]] = None


class PostizVoice(BaseModel):
    id: str
    name: str


class PostizVideoFunctionResponse(BaseModel):
    voices: Optional[List[PostizVoice]] = None
