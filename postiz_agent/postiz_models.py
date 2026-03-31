from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class PostizIntegration(BaseModel):
    id: str
    name: str
    identifier: str
    type: str
    connected: bool
    disabled: bool
    settings: Optional[Dict[str, Any]] = None


class PostizPostPart(BaseModel):
    content: str
    image: Optional[List[Dict[str, str]]] = Field(default_factory=list)


class PostizPost(BaseModel):
    integration: Dict[str, str]
    value: List[PostizPostPart]
    settings: Optional[Dict[str, Any]] = None


class PostizCreatePostRequest(BaseModel):
    type: str = "schedule"                       
    date: Optional[str] = None
    shortLink: bool = False
    tags: List[str] = Field(default_factory=list)
    posts: List[PostizPost]


class PostizPostResponse(BaseModel):
    id: str
    group: str
    date: str
    state: str
    integration: str


class PostizNotification(BaseModel):
    id: str
    content: str
    type: str
    read: bool
    createdAt: str


class PostizAnalytics(BaseModel):
    total: int
    data: List[Dict[str, Any]]


class PostizUploadResponse(BaseModel):
    id: str
    path: str
    filename: str
    mimetype: str
