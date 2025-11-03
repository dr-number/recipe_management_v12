import traceback
from typing import Tuple, Union

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from main.models import User, Recipe, RecipeCategory
from app.helpers import telegram_bot_send_msg
from app.settings import (
    DEBUG, ERRORS_CHAT_ID, HOST, IS_SEND_TO_DEBUG_EMAILS, DEBUG_EMAILS, DEBUG_EMAIL, 
    DEFAULT_FROM_EMAIL
)
from app.help_logger import logger

def get_user_params(data: dict) -> Union[User, None]:
    return User.objects.filter(**data).first()

def get_recipe_params(data: dict) -> Union[Recipe, None]:
    return Recipe.objects.filter(**data).first()

def get_recipe_category_params(data: dict) -> Union[RecipeCategory, None]:
    return RecipeCategory.objects.filter(**data).first()

def save_file(text: str, save_file: str) -> bool:
    try:
        with open(save_file, "w") as file:
            file.write(text)
        return True
    except Exception as e:
        logger.error(f"Error saving text: {e}")
        return False

def send_two_email_service(
    subject_text: str, 
    letter: str, 
    send_to: list[str],
    attachments: list[dict] = None,
) -> Tuple[bool, str, str]:
    """
    Отправляет письмо с возможностью прикрепления нескольких файлов через два почтовых сервиса.
    
    :param subject_text: Тема письма
    :param letter: Текст письма (HTML)
    :param send_to: Список получателей
    :param attachments: Список вложений в формате [{'filename': 'file.txt', 'content': 'file content', 'mimetype': 'text/plain'}]
    :return: Кортеж (успех отправки, ошибки, список получателей)
    """
    error_send = ""
    send_to_str = ''
    is_send_email = False
    attachments = attachments or []

    if DEBUG:
        save_file(letter, 'debug.letter.html')

    if DEBUG and IS_SEND_TO_DEBUG_EMAILS and DEBUG_EMAILS:
        send_to = DEBUG_EMAILS
        print(f'Send letter to debug emails:\n{DEBUG_EMAILS}')
    elif False and DEBUG:
        send_to = [DEBUG_EMAIL]
        print(f'Send letter to debug email:\n{DEBUG_EMAIL}')

    filtered_send_to = [item for item in send_to if '@' in item]
    if not filtered_send_to:
        error_send += '\n🛑 Error two_email_service empty filtered_send_to!'
        return is_send_email, error_send, send_to_str
 
    send_to_str = "\n".join(filtered_send_to)
    try:
        msg = EmailMultiAlternatives(
            subject=subject_text,
            from_email=DEFAULT_FROM_EMAIL,
            body=letter,
            to=filtered_send_to
        )
        msg.content_subtype = 'html'
        
        for attachment in attachments:
            msg.attach(
                filename=attachment['filename'],
                content=attachment['content'],
                mimetype=attachment.get('mimetype')
            )
        
        msg.send()
        is_send_email = True
        return is_send_email, error_send, send_to_str

    except Exception as e:
        error_send += (
            '\n🛑 Error two_email_service [from default email service (0)]:\n'
            f'send_to: {send_to_str}\n'
            f'subject_text: {subject_text}\n\n'
            f'{e}\n{traceback.format_exc()}'
        )

    return is_send_email, error_send, send_to_str

def send_email_code(user: User) -> Tuple[bool, str, str]:
    is_send_email, error_send, send_to_str = send_two_email_service(
        subject_text='Подтверждение',
        letter=render_to_string(f'confirm_email_code.html', context={
            'header': 'Код-подтверждение электронной почты:',
            'code': user.new_confirmation_code_email(),
            'footer': 'Спасибо, что вы с нами!'
        }),
        send_to=[user.email]
    )

    if not is_send_email:
        telegram_bot_send_msg(
            text=(
                f'<b>[Recipe]</b> Error send_email_code\n'
                f'is send email: <b>{is_send_email}</b>\n'
                f'Send to: <b>{send_to_str}</b>\n'
                f'Is staff: <b>{user.is_staff}</b>\n'
                f'{HOST}/admin/main/user/{user.id}/change/'
                f'{error_send}'
                f'\n#Отправка_писем'
            ),
            chat_id=ERRORS_CHAT_ID,
            html=True
        )
    return is_send_email, error_send, send_to_str
