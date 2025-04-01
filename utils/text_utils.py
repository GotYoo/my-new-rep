# src/utils/text_utils.py
import re

def clean_response(text):
    return re.sub(r'<[^>]+>|[^\w\u4e00-\u9fa5/]', '', text)

def split_sentences(text):
    return re.split(r'(?<=[。！？])', text)