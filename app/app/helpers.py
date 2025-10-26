import json
import traceback
from typing import Optional, Union
from app.help_logger import logger
import telebot
from telebot.formatting import escape_markdown
from app.settings import (
    DEBUG, BOT_TOKEN, ERRORS_CHAT_ID,
    
)
from main.const import CodesErrors
from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed

def get_headers(request, ignore_keys=['password']):
    array_headers = []
    try:
        headers = request.META
        for key, value in headers.items():
            if key.startswith('HTTP_'):
                # Убираем префикс 'HTTP_' и приводим к виду заголовков HTTP
                header_name = key.replace('HTTP_', '').replace('_', '-').title()
                if header_name not in ignore_keys:
                    array_headers.append(f'{header_name}: {value}')
    except:
        pass

    return json.dumps(array_headers, indent=4)


def get_data(request, ignore_keys=['password']) -> str:
    try:
        request_data = request.data.copy()
        for key in ignore_keys:
            request_data.pop(key, None)
        return json.dumps(request_data, indent=4)
    except:
        pass

def get_admin_user_info(request, user) -> str:
    try:
        user_info = ""
        request_info = ""
        if user:
            user_info = (
                f"<b>username:</b> {user.username}\n"
                f"<b>is_active:</b> {user.is_active}\n"
                f"<b>is_staff:</b> {user.is_staff}\n\n"
            )
        if request:
            request_info = (
                f"<b>{request.method}</b> :: {request.build_absolute_uri()}\n"
                f"<b>headers:</b> {get_headers(request)}\n"
                f"<b>data:</b> {get_data(request)}\n\n"
            )

        return (
            f"[<b>Recipe</b>]\n{request_info}{user_info}"
            f"<b>date:</b> {datetime.now().strftime('%d-%m-%Y (%A) %H:%M:%S')}\n"
        )
    except:
        return ''

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    request = context['request']
   
    user_info = ''
    if not request.user.is_anonymous:
        _user = request.user
        user_info = (
           'User:\n'
           f'id: {_user.id}\n'
           f'is_active: {_user.is_active}\n'
           f'is_staff: {_user.is_staff}\n'
           f'identifier: {_user.username}\n'
        )

    url = request.build_absolute_uri()
    token = request.META.get('HTTP_AUTHORIZATION', '')
    _type = type(exc)
    
    logger.error(
        f"custom_exception_handler error: {exc}\n_type error: {_type}\n"
        f"{request.method} :: {url}\n"
        f"Authorization: {token}\n{user_info}\n"
        f"Headers:\n{get_headers(request)}\n\n"
        f"Request data:\n{get_data(request)}\n\n"
        f"{traceback.format_exc()}"
    )

    _text_error = "Произошла непредвиденная ошибка. Пожалуйста, попробуйте позднее!"

    is_authentication_failed = isinstance(exc, AuthenticationFailed)
    if is_authentication_failed:
        _text_error = "Некорректные учетные данные. Пользователь неактивен или удален" 


    if response and response.data:
        if not response.data.get('errorText', ''):
            response.data['errorText'] = _text_error

        if is_authentication_failed:
            response.data['errorCode'] = CodesErrors.AUTHENTICATION_FAILED

        response.data['undefined_error'] = _text_error
        return Response(
            response.data,
            status=response.status_code,
        )

    return Response(
        {
            "code": 500,
            "undefined_error": _text_error,
            "errorText": _text_error
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

def telegram_bot_send_msg(chat_id,
                          text: str = None,
                          document: Optional[Union[str, bytes]] = None,
                          photo: Optional[bytes] = None,
                          chats=None,
                          silent=False,
                          preview=False,
                          markdown=False,
                          html=False,
                          keyboard=None,
                          document_name='',
                          bot_token=BOT_TOKEN):
    try:
        MAX_CAPTION_LENGTH = 1024
        MAX_TEXT_LENGTH = 4096

        if not text and not document:
            raise Exception('Either text or document could be provided')

        if bot_token is None:
            return logger.error(f'no BOT_TOKEN set, MESSAGE TO BE SENT TO TELEGRAM:\n{text}')

        if not document_name:
            document_name = 'error.log'

        bot = telebot.TeleBot(token=bot_token)
        send_to = [chat_id] if chat_id else (chats or [ERRORS_CHAT_ID])
        parse_mode = (
            'Markdown' if markdown else 
            'html' if html else 
            None
        )
        text = escape_markdown(text) if markdown else text
        for chat_id in send_to:
            if document:
                if isinstance(document, str):
                    document = document.encode()

                return bot.send_document(
                    chat_id,
                    document,
                    caption=text[:MAX_CAPTION_LENGTH],
                    disable_notification=silent,
                    visible_file_name=document_name,
                    parse_mode=parse_mode,
                )

            if photo:
                return bot.send_photo(
                    chat_id, 
                    photo,
                    caption=text[:MAX_CAPTION_LENGTH],
                    parse_mode=parse_mode
                )

            if len(text) > MAX_TEXT_LENGTH:
                for i in range(0, len(text), MAX_TEXT_LENGTH):
                    bot.send_message(
                        chat_id=chat_id,
                        text=text[i: i + MAX_TEXT_LENGTH],
                        disable_web_page_preview=not preview,
                        disable_notification=silent,
                        parse_mode=parse_mode,
                    )
            else:
                bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    disable_web_page_preview=not preview,
                    disable_notification=silent,
                    parse_mode=parse_mode,
                    reply_markup=keyboard
                )
    except Exception as e:
        if DEBUG:
            print(f'error telegram_bot_send_msg: {e}\n{traceback.format_exc()}')

    
