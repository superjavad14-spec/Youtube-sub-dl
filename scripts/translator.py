#!/usr/bin/env python3
"""
ترجمه زیرنویس SRT از انگلیسی به فارسی با پشتیبانی از تلاش مجدد
"""

import re
from typing import List

from deep_translator import GoogleTranslator
from tenacity import retry, stop_after_attempt, wait_exponential


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def translate_text(text: str, source: str = 'en', target: str = 'fa') -> str:
    """ترجمه یک متن با منطق تلاش مجدد"""
    if not text.strip():
        return text
    return GoogleTranslator(source=source, target=target).translate(text)


def translate_srt(input_path: str, output_path: str) -> None:
    """خواندن فایل SRT و ترجمه قسمت‌های متنی آن"""
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    translated_lines: List[str] = []
    text_buffer: List[str] = []
    in_text = False

    for line in lines:
        stripped = line.strip()
        # شماره، زمان یا خط خالی
        if (
            re.match(r'^\d+$', stripped)
            or '-->' in stripped
            or stripped == ''
        ):
            if in_text and text_buffer:
                original = '\n'.join(text_buffer)
                translated = translate_text(original)
                translated_lines.append(translated + '\n')
                text_buffer = []
                in_text = False
            translated_lines.append(line)
        else:
            if not in_text:
                in_text = True
            text_buffer.append(stripped)

    # بلوک متنی انتهای فایل
    if in_text and text_buffer:
        original = '\n'.join(text_buffer)
        translated = translate_text(original)
        translated_lines.append(translated + '\n')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(translated_lines)
