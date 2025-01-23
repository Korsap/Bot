import os, re, pymupdf
from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.types import FSInputFile
from config import FOLDER_PATH
from logger import *
from messages import *
import sqlite3 as db

folder_path = FOLDER_PATH
router = Router()  # Для регистрации хендлеров
con = db.connect('messages.db')
log = logger

@router.message(Command("start"))  # Фильтр команды /start
async def start_command_handler(message: types.Message):
    first_name = message.from_user.first_name or "Гость"
    last_name = message.from_user.last_name or ""
    id = message.from_user.id
    await message.answer("Привет, " + first_name + last_name + "! Что ищем?")

@router.message()  # Обрабатываем все текстовые сообщения
async def find_text_in_pdfs(message: types.Message):
    search_text = message.text.strip()
    log(f"Поисковой запрос от пользователя '{id}':", search_text)
    if not search_text:
        await message.answer("Вы не ввели текст для поиска.")
        return

    # Создаем регулярное выражение для поиска только целого слова
    search_pattern = re.compile(rf'\b{re.escape(search_text)}\b', re.IGNORECASE)
    find_docs = []

    for root, _, files in os.walk(folder_path):  # Рекурсивный поиск по всем подпапкам
        log(OPEN_FOLDER, root)
        for file_name in files:
            log(OPERATE, file_name)
            if file_name.endswith('.pdf'):  # Проверяем, что файл — это PDF
                pdf_path = os.path.join(root, file_name)
                log(READ_FILE, pdf_path)

                try:
                    doc = pymupdf.open(pdf_path)
                    for page in doc:  # Итерация по страницам
                        text = page.get_text()  # Извлекаем текст со страницы
                        if search_pattern.search(text):  # Используем регулярное выражение
                            find_docs.append(pdf_path)  # Добавляем документ в список
                            break  # Прекращаем поиск в этом документе
                except Exception as e:
                    log(ERROR_FILE, pdf_path, ":", str(e))
                finally:
                    if 'doc' in locals():
                        doc.close()

    if find_docs:
        for doc_path in find_docs:
            try:
                log(CHECK_FILE, doc_path)
                with open(doc_path, 'rb') as f:
                    log(READ_AWALIABLE, doc_path)
                # Отправляем PDF файл
                await message.answer_document(FSInputFile(doc_path),timeout=240)
                log(FILE_SEND, doc_path)
            except Exception as e:
                log(SEND_FAULT, doc_path,":", str(e))
    else:
        await message.answer(f"Ничего не найдено для запроса: '{search_text}'.")
    await message.answer(SEARCH_FINISH)
    log(SEARCH_FINISH)