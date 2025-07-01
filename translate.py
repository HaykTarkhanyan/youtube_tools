import deepl
import googletrans
from typing import List
from abc import ABC, abstractmethod
from googletrans import Translator


class BaseTranslator(ABC):
    @abstractmethod
    def translate(self, text: str, target_language: str) -> str:
        pass
    
    @abstractmethod
    def detect_language(self, text: str) -> str:
        pass
    
    @abstractmethod
    def get_supported_languages(self) -> List[str]:
        pass
# https://github.com/ssut/py-googletrans/tree/main
# https://stackoverflow.com/questions/55409641/asyncio-run-cannot-be-called-from-a-running-event-loop-when-using-jupyter-no

class GoogleTranslator(BaseTranslator):
    """Google Translate API implementation of BaseTranslator."""
    @staticmethod
    async def translate(text, target_lang):
        async with Translator() as translator:
            result = await translator.translate(text, dest=target_lang)
            return result.text        

    @staticmethod
    def detect_language(text: str) -> str:
        pass 
    
    @staticmethod   
    def get_supported_languages() -> List[str]:
        return googletrans.LANGUAGES 

class DeepLTranslator(BaseTranslator):
    def __init__(self, api_key) -> None:
        try:
            deepl_client = deepl.DeepLClient(api_key)
        except:
            raise ValueError("Invalid DeepL API key provided.")
        self._client = deepl_client # protected
    def translate(self, text: str, target_lang: str) -> str:
        result = self._client.translate_text(text, target_lang=target_lang)
        return result.text  
    
    def detect_language(self, text: str) -> str:
        pass 
    
    def get_supported_languages(self) -> List[str]:
        pass