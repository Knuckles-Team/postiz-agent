from agent_utilities.api_utilities import require_auth

from postiz_agent.api.api_client_base import BaseApiClient
from postiz_agent.postiz_models import (
    PostizCreatePostRequest,
    PostizMissingContentItem,
    PostizPost,
)


class PostsClient(BaseApiClient):
    @require_auth
    def list_posts(
        self,
        start_date: str,
        end_date: str,
        customer: str | None = None,
    ) -> list[PostizPost]:
        params = {"startDate": start_date, "endDate": end_date}
        if customer:
            params["customer"] = customer
        response = self.session.get(f"{self.base_url}/posts", params=params)
        response.raise_for_status()
        data = response.json()
        if "posts" in data:
            return [PostizPost(**p) for p in data["posts"]]
        return []

    @require_auth
    def create_post(self, request: PostizCreatePostRequest) -> list[dict[str, str]]:
        # In case the request is passed as a dict, parse it
        if isinstance(request, dict):
            request = PostizCreatePostRequest(**request)
        response = self.session.post(
            f"{self.base_url}/posts", json=request.model_dump(exclude_none=True)
        )
        response.raise_for_status()
        return response.json()

    @require_auth
    def delete_post(self, post_id: str) -> dict[str, str]:
        response = self.session.delete(f"{self.base_url}/posts/{post_id}")
        response.raise_for_status()
        return response.json()

    @require_auth
    def delete_post_by_group(self, group: str) -> dict[str, str]:
        response = self.session.delete(f"{self.base_url}/posts/group/{group}")
        response.raise_for_status()
        return response.json()

    @require_auth
    def get_missing_content(self, post_id: str) -> list[PostizMissingContentItem]:
        response = self.session.get(f"{self.base_url}/posts/{post_id}/missing")
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return [PostizMissingContentItem(**i) for i in data]
        return []

    @require_auth
    def update_release_id(self, post_id: str, release_id: str) -> dict[str, str]:
        response = self.session.put(
            f"{self.base_url}/posts/{post_id}/release-id",
            json={"releaseId": release_id},
        )
        response.raise_for_status()
        return response.json()

    # MCP action-routed aliases
    postiz_list_posts = list_posts
    postiz_create_post = create_post
    postiz_delete_post = delete_post
    postiz_delete_post_by_group = delete_post_by_group
    postiz_get_missing_content = get_missing_content
    postiz_update_release_id = update_release_id
