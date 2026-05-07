#!/usr/bin/env python3
"""
YouTube Subtitle Downloader – دانلود، ترجمه و رمزگذاری زیرنویس
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional

import yt_dlp

from translator import translate_srt
from zip_protector import create_encrypted_zip


def get_video_info(video_url: str) -> Dict[str, Any]:
    """دریافت اطلاعات ویدیو و زیرنویس‌های موجود"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(video_url, download=False)


def list_all_subs(info: dict) -> List[str]:
    """بازگرداندن فهرست تمام زبان‌های زیرنویس (دستی و خودکار)"""
    subs = set()
    for key in ('subtitles', 'automatic_captions'):
        if key in info and info[key]:
            subs.update(info[key].keys())
    return list(subs)


def download_subtitle(
    video_url: str,
    lang: str,
    output_dir: str,
    video_title: str
) -> str:
    """دانلود زیرنویس به فرمت SRT و بازگرداندن مسیر فایل"""
    outtmpl = os.path.join(output_dir, f'{video_title}.%(ext)s')
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'writeautomaticsub': True,
        'writesubtitles': True,
        'subtitleslangs': [lang],
        'convertsubs': 'srt',
        'outtmpl': outtmpl,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    # پیدا کردن فایل SRT تولیدشده
    for fname in os.listdir(output_dir):
        if fname.endswith('.srt') and lang in fname:
            return os.path.join(output_dir, fname)
    raise FileNotFoundError(
        f"فایل زیرنویس برای زبان '{lang}' پس از دانلود یافت نشد."
    )


def sanitize_filename(name: str) -> str:
    """حذف کاراکترهای غیرمجاز از نام فایل"""
    return "".join(c for c in name if c.isalnum() or c in ' _-').strip()


def process_subtitle(
    video_url: str,
    lang: str,
    zip_password: str,
    output_dir: str
) -> None:
    """کل فرایند را اجرا می‌کند (قابل تست مجزا)"""
    os.makedirs(output_dir, exist_ok=True)

    print("📡 دریافت اطلاعات ویدیو...")
    info = get_video_info(video_url)
    title_raw = info.get('title', 'unknown_video')
    safe_title = sanitize_filename(title_raw)
    available_subs = list_all_subs(info)

    with open('video_info.json', 'w', encoding='utf-8') as f:
        json.dump({
            'title': safe_title,
            'available_subs': available_subs
        }, f)

    print(f"زبان‌های موجود: {available_subs}")

    srt_file: str

    if lang in available_subs:
        print(f"⬇️ دانلود مستقیم زیرنویس {lang}...")
        srt_file = download_subtitle(video_url, lang, output_dir, safe_title)
    elif lang == 'fa':
        if 'en' not in available_subs:
            print(
                "❌ خطا: زیرنویس انگلیسی برای ترجمه به فارسی موجود نیست.",
                file=sys.stderr
            )
            sys.exit(1)
        print("🔄 فارسی موجود نیست – دانلود انگلیسی و ترجمه...")
        eng_srt = download_subtitle(video_url, 'en', output_dir, safe_title)
        fa_srt = os.path.join(output_dir, f'{safe_title}.fa.srt')
        translate_srt(eng_srt, fa_srt)
        os.remove(eng_srt)
        srt_file = fa_srt
    else:
        print(
            f"❌ زبان '{lang}' در زیرنویس‌های ویدیو پیدا نشد.",
            file=sys.stderr
        )
        sys.exit(1)

    file_size = os.path.getsize(srt_file)
    print(f"📏 حجم فایل: {file_size} بایت")

    output_file = srt_file
    is_zip = False
    password_used: Optional[str] = None

    THRESHOLD = 100 * 1024 * 1024  # 100 MB

    if file_size > THRESHOLD:
        if not zip_password:
            print(
                "❌ حجم فایل بیش از ۱۰۰ مگابایت است و رمز عبور ZIP ارائه نشده.",
                file=sys.stderr
            )
            sys.exit(1)
        zip_path = os.path.join(
            output_dir,
            f'{safe_title}.{lang}.zip'
        )
        print(f"🔐 ساخت ZIP رمزگذاری‌شده: {zip_path}")
        create_encrypted_zip(srt_file, zip_path, zip_password)
        os.remove(srt_file)
        output_file = zip_path
        is_zip = True
        password_used = zip_password
    else:
        # اگر فایل در محل نهایی نباشد، جابجا شود
        if not srt_file.startswith(output_dir):
            dest = os.path.join(output_dir, os.path.basename(srt_file))
            os.rename(srt_file, dest)
            output_file = dest

    # ذخیره اطلاعات خروجی برای استفاده در workflow
    with open('final_output_info.json', 'w', encoding='utf-8') as f:
        json.dump({
            'output_file': output_file,
            'is_zip': is_zip,
            'password': password_used or ''
        }, f)

    print(f"✅ فایل نهایی: {output_file}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="دانلود و محافظت از زیرنویس یوتیوب"
    )
    parser.add_argument('--video-url', required=True)
    parser.add_argument('--lang', required=True, choices=['en', 'fa'])
    parser.add_argument('--zip-password', default='')
    parser.add_argument('--output-dir', default='subtitles')
    args = parser.parse_args()

    process_subtitle(
        video_url=args.video_url,
        lang=args.lang,
        zip_password=args.zip_password,
        output_dir=args.output_dir
    )


if __name__ == '__main__':
    main()
