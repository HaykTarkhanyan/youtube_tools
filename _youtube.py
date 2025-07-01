from typing import List
from datetime import datetime
from pytubefix import YouTube
from dataclasses import dataclass

@dataclass()
class VideoInfo:
    video_id: str
    title: str
    keywords: List[str]
    publish_date: str  
    length_seconds: int
    
    @staticmethod
    def get_days_since_publish(publish_date) -> int:
        if isinstance(publish_date, datetime):
            publish_date = publish_date.strftime("%Y-%m-%d")
        publish_date = datetime.strptime(publish_date, "%Y-%m-%d")
        current_date = datetime.now()
        return (current_date - publish_date).days
        
        
    def __post_init__(self):
        if not isinstance(self.video_id, str):
            raise ValueError("video_id must be a string")
        if not isinstance(self.length_seconds, int):
            raise ValueError("length_seconds must be an integer")
        
        self.days_since_publish = self.get_days_since_publish(self.publish_date)
        
        
class YouTubeVideo:
    def __init__(self, url: str):
        self.video = YouTube(url)

    def get_metadata(self) -> VideoInfo:
        return VideoInfo(
            video_id=self.video.video_id,
            title=self.video.title, 
            keywords=self.video.keywords,
            publish_date=self.video.publish_date,
            length_seconds=self.video.length
        )
    
    def get_transcript(self, language: str = "a.hy", return_srt: bool = True) -> str:
        captions = self.video.captions.get(language)
        if not captions:
            print(f"Only the following languages are available: {self.video.captions.keys()}")
            raise ValueError(f"No captions available for language: {language}")
        if return_srt:
            self.text = captions.generate_srt_captions()
        else:
            self.text = captions.generate_txt_captions()
        return self.text
    
    def download_transcript(self, language: str = "de", title: str = "transcript", output_path: str = "transcript.txt") -> None:
        captions = self.video.captions.get(language)
        if not captions:
            raise ValueError(f"No captions available for language: {language}")
        captions.download(title=title, output_path=output_path)
    
    def download_audio(self, output_path=None) -> None:
        """Download the audio stream of the YouTube video.

        Args:
            output_path (_type_, optional): _description_. Defaults to None.

        Raises:
            ValueError: _description_
        """
        if output_path is None:
            output_path = self.video.video_id
        
        audio_stream = self.video.streams.get_audio_only()
        if not audio_stream:
            raise ValueError("No audio stream available")
        audio_stream.download(output_path=output_path)
        
    def download_video(self, output_path=None) -> None:
        if output_path is None:
            output_path = self.video.video_id
        
        video_stream = self.video.streams.get_lowest_resolution()
        if not video_stream:
            raise ValueError("No video stream available")
        video_stream.download(output_path=output_path)