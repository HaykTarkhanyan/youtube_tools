import wordcloud
import pandas as pd
from pathlib import Path
from pytubefix import YouTube

class Transcript:
    def __init__(self, video_url: str, language: str = "en"):
        self.video_url = video_url
        self.video = YouTube(video_url)

        # -------- Setting language --------
        self.available_languages = self.get_available_languages()
        if language in self.available_languages:
            print(f"Using {language} subtitles.")
            self.language = language
        elif (language == "en") and ("a.en" in self.available_languages):
            print("Using automatic English subtitles.")
            self.language = "a.en"
        else:
            raise ValueError(f"Language '{language}' not supported. "
                             f"Use one of the following: {self.available_languages}")

        # -------- Setting title --------
        self.title = self.video.title
        self.title_no_special_chars = ''.join(e for e in self.title 
                                              if e.isalnum() or e.isspace()).replace(" ", "_")
        print(f"Video Title: {self.title_no_special_chars}")
    
        self.get_transcript(language=self.language)
    @staticmethod
    def srt_to_csv(srt_text: str) -> pd.DataFrame:
        """
        Convert SRT text to a DataFrame.
        """
        lines = srt_text.strip().split('\n')
        data = []
        for i in range(0, len(lines), 4):
            if i + 3 < len(lines):
                index = lines[i].strip()
                time_range = lines[i + 1].strip()
                text = lines[i + 2].strip()
                data.append({"index": index, "time_range": time_range, "text": text})
        return pd.DataFrame(data)
    
    @staticmethod
    def transcript_info(text: str) -> dict:
        """
        Extracts information from the transcript text.
        Returns a dictionary with the number of words and characters.
        """
        words = text.split()
        num_sentences = text.count('.') + text.count('!') + text.count('?')
        num_words = len(words)
        num_chars = len(text)
        
        return {
            "num_sentences": num_sentences,
            "num_words": num_words,
            "num_chars": num_chars
        }
    
    def get_available_languages(self):
        languages_available = self.video.captions.keys()
        if "a.hy" in languages_available:
            print("Automatic armenian subtitles are available.")
        if "en" in languages_available:
            print("English subtitles are available.")
        if "a.en" in languages_available:
            print("Automatic English subtitles are available.")
        return languages_available
        

    def get_transcript(self, language = None, generate_wordcloud: bool = False):
        if language is None:
            language = self.language

        self.caption = self.video.captions[language]
        self.text = self.caption.generate_txt_captions()
        self.srt = self.caption.generate_srt_captions()
        print(f"Transcript for '{language}' language has been generated.")
        print(f"Transcript info: {self.transcript_info(self.text)}")
        
        Path.mkdir(Path("videos", self.title_no_special_chars), exist_ok=True)
        
        filename = Path("videos", self.title_no_special_chars, self.title_no_special_chars)
        with open(f"{filename}.txt", "w", encoding="utf-8") as f:
            f.write(self.text)
        
        with open(f"{filename}.srt", "w", encoding="utf-8") as f:
            f.write(self.srt)
        print(f"Transcript saved to {filename}.txt and {filename}.srt")
        
        # Save srt to CSV
        self.srt_df = self.srt_to_csv(self.srt)
        csv_filename = f"{filename}.csv"
        self.srt_df.to_csv(csv_filename, index=False, encoding="utf-8")
        print(f"SRT converted to CSV and saved to {csv_filename}")

        if generate_wordcloud:
            # Generate word cloud
            wordcloud_filename = f"{filename}_wordcloud.png"
            wordcloud_image = wordcloud.WordCloud(width=800, height=400, background_color='white')
            wordcloud_image.generate(self.text)
            wordcloud_image.to_file(wordcloud_filename)
            print(f"Word cloud generated and saved to {wordcloud_filename}")
        
        return self.text, self.srt, self.srt_df    
