#!/usr/bin/env python3
"""
ساخت فایل ZIP رمزنگاری‌شده با الگوریتم AES-256
"""

import pyzipper


def create_encrypted_zip(
    file_path: str,
    output_zip: str,
    password: str
) -> None:
    """
    فشرده‌سازی و رمزگذاری یک فایل با AES-256.
    فایل داخل بایگانی فقط با نام اصلی خود ذخیره می‌شود.
    """
    with pyzipper.AESZipFile(
        output_zip,
        'w',
        compression=pyzipper.ZIP_DEFLATED,
        encryption=pyzipper.WZ_AES
    ) as zf:
        zf.setpassword(password.encode('utf-8'))
        zf.write(file_path, arcname=file_path.rsplit('/', 1)[-1])
