import httpx
import asyncio
from typing import Dict, Any, Optional
from src.core.config import settings

class InstagramPublisher:
    """
    Official Meta Instagram Graph API Content Publisher.
    Handles Container Creation, Status Polling, and Direct Publishing
    for Single Images, Carousels, and Video Reels.
    """
    def __init__(
        self,
        access_token: Optional[str] = None,
        instagram_account_id: Optional[str] = None
    ):
        self.access_token = access_token or settings.META_USER_ACCESS_TOKEN
        self.account_id = instagram_account_id or settings.INSTAGRAM_ACCOUNT_ID
        self.base_url = "https://graph.facebook.com/v21.0"

    async def create_reel_container(
        self,
        video_url: str,
        caption: str,
        cover_url: Optional[str] = None
    ) -> str:
        """
        Creates a Reel media container via official Graph API.
        """
        if not self.access_token or not self.account_id:
            raise ValueError("Meta credentials (access_token / instagram_account_id) not set.")

        url = f"{self.base_url}/{self.account_id}/media"
        params = {
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption,
            "access_token": self.access_token
        }
        if cover_url:
            params["cover_url"] = cover_url

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, data=params)
            data = resp.json()
            if resp.status_code != 200 or "id" not in data:
                raise RuntimeError(f"Failed to create Reel container: {data}")
            return data["id"]

    async def wait_for_media_processing(
        self,
        creation_id: str,
        max_attempts: int = 15,
        delay_seconds: int = 5
    ) -> bool:
        """
        Polls Instagram Graph API until container status is 'FINISHED' and ready for publish.
        """
        url = f"{self.base_url}/{creation_id}"
        params = {
            "fields": "status_code",
            "access_token": self.access_token
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            for _ in range(max_attempts):
                resp = await client.get(url, params=params)
                data = resp.json()
                status = data.get("status_code")
                if status == "FINISHED":
                    return True
                elif status == "ERROR":
                    raise RuntimeError(f"Instagram media processing failed: {data}")
                await asyncio.sleep(delay_seconds)

        return False

    async def publish_container(self, creation_id: str) -> str:
        """
        Final step: Publishes the finished container directly to @scrriber feed/reels.
        """
        url = f"{self.base_url}/{self.account_id}/media_publish"
        params = {
            "creation_id": creation_id,
            "access_token": self.access_token
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, data=params)
            data = resp.json()
            if resp.status_code != 200 or "id" not in data:
                raise RuntimeError(f"Failed to publish media: {data}")
            return data["id"] # Published Instagram Media ID
