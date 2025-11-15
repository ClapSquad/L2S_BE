from pathlib import Path
import yt_dlp


def download_youtube_video(youtube_id: str, output_path: Path, quality: str = "720p") -> tuple[str, str]:
    youtube_url = f"https://www.youtube.com/watch?v={youtube_id}"
    output_template = str(output_path / f"{youtube_id}.%(ext)s")

    # 화질별 포맷 매핑
    quality_formats = {
        "360p": "best[height<=360][ext=mp4]/best[height<=360]",
        "480p": "best[height<=480][ext=mp4]/best[height<=480]",
        "720p": "best[height<=720][ext=mp4]/best[height<=720]",
        "1080p": "best[height<=1080][ext=mp4]/best[height<=1080]",
    }

    ydl_opts = {
        'format': quality_formats.get(quality, "best[ext=mp4]/best"),
        'outtmpl': output_template,
        'quiet': True,
        'no_warnings': True,
        'no_progress': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            video_title = info.get('title', 'Unknown')

            # 다운로드
            ydl.download([youtube_url])

            # 다운로드된 파일 찾기
            downloaded_files = list(output_path.glob(f"{youtube_id}.*"))
            if downloaded_files:
                actual_file = downloaded_files[0]
                return str(actual_file), video_title
            else:
                raise ValueError("Downloaded file not found")

    except Exception as e:
        raise ValueError(f"Failed to download video: {str(e)}")
