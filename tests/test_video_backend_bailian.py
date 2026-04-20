from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from lib.video_backends.bailian import BailianVideoBackend
from lib.video_backends.base import ReferenceMedia, VideoCapability, VideoGenerationRequest


@pytest.fixture
def backend():
    return BailianVideoBackend(api_key="test-key", model="wan2.7-r2v", base_url="https://test.example.com")


class TestBailianVideoBackendProperties:
    def test_capabilities_r2v(self, backend):
        caps = backend.capabilities
        assert VideoCapability.GENERATE_AUDIO in caps

    def test_supported_model_r2v(self, backend):
        assert backend.model == "wan2.7-r2v"


class TestBailianVideoBackendValidation:
    def test_validate_r2v_requires_reference_media(self, backend, tmp_path):
        request = VideoGenerationRequest(
            prompt="test",
            output_path=tmp_path / "out.mp4",
        )

        with pytest.raises(ValueError, match="至少一个参考素材"):
            backend._validate_request(request)

    def test_validate_r2v_too_many_videos(self, backend, tmp_path):
        request = VideoGenerationRequest(
            prompt="test",
            output_path=tmp_path / "out.mp4",
            reference_media=[
                ReferenceMedia(media_path=Path("v1.mp4"), media_type="video"),
                ReferenceMedia(media_path=Path("v2.mp4"), media_type="video"),
                ReferenceMedia(media_path=Path("v3.mp4"), media_type="video"),
                ReferenceMedia(media_path=Path("v4.mp4"), media_type="video"),
            ],
        )

        with pytest.raises(ValueError, match="参考视频数量不得超过 3 个"):
            backend._validate_request(request)

    def test_validate_r2v_too_many_total_media(self, backend, tmp_path):
        request = VideoGenerationRequest(
            prompt="test",
            output_path=tmp_path / "out.mp4",
            reference_media=[ReferenceMedia(media_path=Path(f"i{i}.png"), media_type="image") for i in range(6)],
        )

        with pytest.raises(ValueError, match="参考素材总数不得超过 5 个"):
            backend._validate_request(request)

    def test_validate_r2v_invalid_media_type(self, backend, tmp_path):
        request = VideoGenerationRequest(
            prompt="test",
            output_path=tmp_path / "out.mp4",
            reference_media=[ReferenceMedia(media_path=Path("a.mp3"), media_type="audio")],
        )

        with pytest.raises(ValueError, match="仅支持 image/video"):
            backend._validate_request(request)


class TestBailianVideoBackendPayload:
    @pytest.mark.asyncio
    async def test_build_payload_r2v_with_voice(self, backend, tmp_path):
        output = tmp_path / "out.mp4"
        request = VideoGenerationRequest(
            prompt="test prompt",
            output_path=output,
            duration_seconds=10,
            resolution="720p",
            aspect_ratio="16:9",
            reference_media=[
                ReferenceMedia(
                    media_path=Path("/tmp/image.png"), media_type="image", voice_path=Path("/tmp/voice.mp3")
                ),
                ReferenceMedia(media_path=Path("http://example.com/video.mp4"), media_type="video"),
            ],
        )
        headers = {"Authorization": "Bearer test"}

        async def fake_resolve(path, headers):
            raw = str(path)
            # 模拟 _resolve_media_url 的 URL 规范化逻辑
            if raw.startswith(("http:/", "https:/", "oss:/")):
                if raw.startswith("http:/") and not raw.startswith("http://"):
                    raw = raw.replace("http:/", "http://", 1)
                elif raw.startswith("https:/") and not raw.startswith("https://"):
                    raw = raw.replace("https:/", "https://", 1)
                elif raw.startswith("oss:/") and not raw.startswith("oss://"):
                    raw = raw.replace("oss:/", "oss://", 1)
                return raw
            headers["X-DashScope-OssResourceResolve"] = "enable"
            return f"oss://uploaded/{Path(path).name}"

        with patch.object(backend, "_resolve_media_url", new=fake_resolve):
            payload = await backend._build_payload(request, headers)

        assert payload["model"] == "wan2.7-r2v"
        assert payload["parameters"]["resolution"] == "720P"
        assert payload["parameters"]["ratio"] == "16:9"
        assert payload["parameters"]["duration"] == 10
        assert payload["input"]["prompt"] == "test prompt"
        assert payload["input"]["media"] == [
            {
                "type": "reference_image",
                "url": "oss://uploaded/image.png",
                "reference_voice": "oss://uploaded/voice.mp3",
            },
            {
                "type": "reference_video",
                "url": "http://example.com/video.mp4",
            },
        ]
        assert headers["X-DashScope-OssResourceResolve"] == "enable"

    @pytest.mark.asyncio
    async def test_resolve_media_url_keeps_http_and_marks_oss(self, backend):
        with patch("lib.video_backends.bailian.upload_file_and_get_url", new=AsyncMock()) as mock_upload:
            # HTTP URL 直接返回，不调用上传
            headers = {}
            http_url = await backend._resolve_media_url(Path("https://example.com/a.png"), headers)
            assert http_url == "https://example.com/a.png"
            assert "X-DashScope-OssResourceResolve" not in headers
            mock_upload.assert_not_called()

            # OSS URL 直接返回，设置 header，不调用上传
            oss_headers = {}
            oss_url = await backend._resolve_media_url(Path("oss://bucket/a.png"), oss_headers)
            assert oss_url == "oss://bucket/a.png"
            assert oss_headers["X-DashScope-OssResourceResolve"] == "enable"
            mock_upload.assert_not_called()

    @pytest.mark.asyncio
    async def test_resolve_media_url_uploads_local_file(self, backend, tmp_path):
        local_file = tmp_path / "a.png"
        local_file.write_bytes(b"png")
        headers = {}

        with patch(
            "lib.video_backends.bailian.upload_file_and_get_url", new=AsyncMock(return_value="oss://uploaded/a.png")
        ) as upload:
            url = await backend._resolve_media_url(local_file, headers)

        assert url == "oss://uploaded/a.png"
        assert headers["X-DashScope-OssResourceResolve"] == "enable"
        upload.assert_awaited_once()
