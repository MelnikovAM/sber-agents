import logging
import os
from pathlib import Path
from config import config

logger = logging.getLogger(__name__)

# Глобальная переменная для кэширования модели openai-whisper
_whisper_model = None


async def transcribe_audio(audio_file_path: str) -> str:
    """
    Транскрибирует аудиофайл в текст.
    Автоматически выбирает провайдера на основе config.STT_PROVIDER.
    
    Args:
        audio_file_path: Путь к аудиофайлу (OGG, WAV, MP3)
    
    Returns:
        str: Транскрибированный текст
    
    Raises:
        ValueError: Если провайдер STT неизвестен
        Exception: Если транскрибация не удалась
    """
    logger.info(f"Transcribing audio file: {audio_file_path}, provider: {config.STT_PROVIDER}")
    
    if config.STT_PROVIDER == "openai":
        return await _transcribe_openai(audio_file_path)
    elif config.STT_PROVIDER == "local":
        return await _transcribe_local(audio_file_path)
    else:
        raise ValueError(f"Unknown STT provider: {config.STT_PROVIDER}")


async def _transcribe_openai(audio_file_path: str) -> str:
    """Транскрибация через OpenAI Whisper API."""
    from openai import AsyncOpenAI
    
    try:
        # Используем отдельные настройки для STT
        client = AsyncOpenAI(
            api_key=config.STT_API_KEY,
            base_url=config.STT_BASE_URL
        )
        
        with open(audio_file_path, "rb") as audio_file:
            logger.info(f"Sending audio to OpenAI Whisper API at {config.STT_BASE_URL} (file size: {os.path.getsize(audio_file_path)} bytes)")
            
            transcript = await client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="ru"  # Указываем русский для лучшего качества
            )
        
        text = transcript.text.strip()
        logger.info(f"OpenAI Whisper API transcription result: {text[:200]}...")
        return text
    
    except Exception as e:
        logger.error(f"Error transcribing audio with OpenAI Whisper API: {e}", exc_info=True)
        raise


async def _transcribe_local(audio_file_path: str) -> str:
    """Транскрибация через openai-whisper (локально на Mac)."""
    global _whisper_model
    
    try:
        # Импортируем openai-whisper
        import whisper
        import asyncio
        
        # Инициализируем модель только один раз (кэширование)
        if _whisper_model is None:
            model_name = config.STT_MODEL  # "tiny", "base", "small", "medium", "large"
            
            logger.info(f"Loading openai-whisper model '{model_name}' (first run will download ~{_get_model_size(model_name)})...")
            
            # Загружаем модель в отдельном потоке, чтобы не блокировать event loop
            _whisper_model = await asyncio.to_thread(whisper.load_model, model_name)
            
            logger.info(f"openai-whisper model '{model_name}' loaded successfully")
        
        logger.info(f"Transcribing audio locally with openai-whisper (file size: {os.path.getsize(audio_file_path)} bytes)")
        
        # Транскрибируем аудио в отдельном потоке
        result = await asyncio.to_thread(
            _whisper_model.transcribe,
            audio_file_path,
            language="ru",
            fp16=False  # Отключаем fp16 для CPU (Intel Mac не поддерживает)
        )
        
        text = result["text"].strip()
        logger.info(f"openai-whisper transcription result (detected language: {result.get('language', 'unknown')}): {text[:200]}...")
        
        return text
    
    except ImportError as e:
        logger.error(f"openai-whisper not installed: {e}")
        logger.error("Install with: pip install openai-whisper")
        raise RuntimeError("openai-whisper not installed. Run: pip install openai-whisper")
    except Exception as e:
        logger.error(f"Error transcribing audio with openai-whisper: {e}", exc_info=True)
        raise


def _get_model_size(model_name: str) -> str:
    """Возвращает примерный размер модели для информации."""
    sizes = {
        "tiny": "75 MB",
        "base": "142 MB",
        "small": "466 MB",
        "medium": "1.5 GB",
        "large": "2.9 GB"
    }
    return sizes.get(model_name, "unknown size")

