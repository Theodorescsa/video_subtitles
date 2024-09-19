# tasks.py
import pytube
from pytube. innertube import _default_clients
from pytube import cipher
from src.constant import VIDEOS_PATH
from src.utils.utils import extract_audio, transcribe, generate_subtitle_file, add_subtitle_to_video, get_throttling_function_name
from celery_app import app


# config
_default_clients["ANDROID"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["ANDROID_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_MUSIC"]["context"]["client"]["clientVersion"] = "6.41"
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

cipher.get_throttling_function_name = get_throttling_function_name


def download_video(url):
    yt = pytube.YouTube(url)
    yt_id = yt.video_id
    yt.streams.filter(progressive=True, file_extension='mp4').order_by(
        'resolution').desc().first().download(output_path=VIDEOS_PATH, filename=yt_id)
    return {"title": yt.title, "id": yt_id, "status": "completed"}


def extract_audio_task(yt_id):
    audio_extract = extract_audio(yt_id)
    return audio_extract, yt_id


def transcribe_task(audio_extract, yt_id, dest):
    language, segments,translated_text_list = transcribe(audio_extract, dest)
    serializable_segments = []
    for segment in segments:
        serializable_segments.append({
            'start': segment.start,
            'end': segment.end,
            'text': segment.text,
            'translated_text_list': translated_text_list

        })
    return language, serializable_segments, yt_id


def generate_subtitle_file_task(language, segments_data, yt_id):
    subtitle_file = generate_subtitle_file(yt_id, language, segments_data)
    return subtitle_file, language, yt_id

def add_subtitle_to_video_task(subtitle_file, language, yt_id):
  
    add_subtitle_to_video(yt_id, subtitle_file, language)
    return f"Subtitle for {yt_id} added"
