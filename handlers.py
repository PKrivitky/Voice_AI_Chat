import time
from aiogram import Router
from aiogram.types import Message, FSInputFile
from utils import stt, tts, ask_gpt

router = Router()

@router.message()
async def handle_voice_message(message: Message, **kwargs):
    bot = kwargs["bot"]  # Получаем бота из контекста диспетчера

    chat_id = message.chat.id
    file_id = message.voice.file_id
    unique_name = f"{int(time.time())}.ogg"

    # Загружаем голосовое сообщение
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, unique_name)

    try:
        speech_text = await stt(unique_name)
    except Exception as e:
        await message.reply(f"Ошибка при распознавании: {e}")
        return

    gpt_answer = await ask_gpt(speech_text)

    # Генерируем голосовой ответ
    response_audio = f"{int(time.time())}.ogg"
    await tts(gpt_answer, response_audio)

    audio_file = FSInputFile(response_audio)
    await bot.send_voice(chat_id=chat_id, voice=audio_file)

def register_handlers(dp):
    dp["bot"] = dp["bot"]  # Добавляем бота в контекст диспетчера
    dp.include_router(router)
