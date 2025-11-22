from django import template
from main.aes import aes_decrypt
from app.settings import IMG_PASSWORD

register = template.Library()

@register.filter
def decrypt(text):
    return aes_decrypt(text=text, password=IMG_PASSWORD)
