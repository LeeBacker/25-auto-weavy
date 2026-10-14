"""Seedance 2.5 / 720p / true AUTO duration adapter for Replicate Cog.

Fal's original US reference-to-video endpoint does the actual generation.
This file only exposes a Weavy-friendly input schema and forwards the call.
"""

from tempfile import NamedTemporaryFile
from typing import Optional

import requests
from cog import BasePredictor, Input, Path, Secret

FAL_ENDPOINT = "bytedance/seedance-2.5/us/reference-to-video"


def build_arguments(prompt, duration, aspect_ratio, generate_audio, image_urls, video_urls):
    """Pure helper: makes the actual API payload; useful for testing."""
    if not prompt.strip():
        raise ValueError("Prompt cannot be empty")
    if duration not in ("Auto", "30"):
        raise ValueError("Duration must be Auto or 30")

    args = {
        "prompt": prompt,
        "task": "reference",
        "resolution": "720p",
        "duration": "auto" if duration == "Auto" else "30",
        "aspect_ratio": aspect_ratio,
        "generate_audio": generate_audio,
    }
    if image_urls:
        args["image_urls"] = image_urls
    if video_urls:
        args["video_urls"] = video_urls
    return args


class Predictor(BasePredictor):
    def predict(
        self,
        prompt: str = Input(description="Prompt. Refer to images as @Image1, @Image2, etc."),
        fal_api_key: Secret = Input(description="Your own fal.ai API key (secret input; not saved in source code)"),
        duration: str = Input(
            description="Auto = let Seedance choose 4–30 seconds; 30 = exactly 30 seconds",
            default="Auto",
            choices=["Auto", "30"],
        ),
        aspect_ratio: str = Input(
            description="Video aspect ratio",
            default="16:9",
            choices=["16:9", "9:16", "21:9", "4:3", "3:4", "1:1", "auto"],
        ),
        generate_audio: bool = Input(description="Include generated sounds", default=True),
        image_1: Optional[Path] = Input(description="Reference image 1", default=None),
        image_2: Optional[Path] = Input(description="Reference image 2", default=None),
        image_3: Optional[Path] = Input(description="Reference image 3", default=None),
        image_4: Optional[Path] = Input(description="Reference image 4", default=None),
        image_5: Optional[Path] = Input(description="Reference image 5", default=None),
        image_6: Optional[Path] = Input(description="Reference image 6", default=None),
        video_1: Optional[Path] = Input(description="Optional motion/video reference", default=None),
    ) -> Path:
        import fal_client

        key = fal_api_key.get_secret_value().strip()
        if not key:
            raise ValueError("fal.ai API key is required")

        # A per-request client prevents credentials leaking across predictions.
        fal = fal_client.SyncClient(key=key)
        images = [fal.upload_file(str(item)) for item in
                  (image_1, image_2, image_3, image_4, image_5, image_6) if item is not None]
        videos = [fal.upload_file(str(video_1))] if video_1 is not None else []

        args = build_arguments(prompt, duration, aspect_ratio, generate_audio, images, videos)
        result = fal.subscribe(FAL_ENDPOINT, arguments=args)
        url = result.get("video", {}).get("url")
        if not isinstance(url, str) or not url.startswith("https://"):
            raise RuntimeError("fal.ai did not return an HTTPS video URL")

        # Return actual video data as Cog Path, so Weavy sees a video output.
        with NamedTemporaryFile(suffix=".mp4", delete=False) as target:
            with requests.get(url, stream=True, timeout=(20, 180)) as response:
                response.raise_for_status()
                for chunk in response.iter_content(chunk_size=2 * 1024 * 1024):
                    if chunk:
                        target.write(chunk)
            return Path(target.name)
