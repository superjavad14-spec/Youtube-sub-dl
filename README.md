# 🎬 YouTube Subtitle Downloader & Protector | دانلودر و محافظ زیرنویس یوتیوب

[🇬🇧 English] · [🇮🇷 فارسی]

---

## 🇬🇧 English

### Features
- Download YouTube subtitles in **SRT** format.
- Select **English (en)** or **Persian (fa)** language.
- If Persian is not available, automatically translate the **English** subtitle to Persian.
- If the subtitle file exceeds **100 MB**, it is compressed into a password-protected **ZIP (AES-256)**.
- Fully automated via **GitHub Actions** (`workflow_dispatch`).

### How to Use (After Fork)
1. Fork this repository.
2. Go to your fork → **Settings** → **Secrets and variables** → **Actions**.
3. Add a secret named `GH_PAT` containing a **Personal Access Token** with `repo` or `workflow` scope.
4. Go to the **Actions** tab → Select **YouTube Subtitle Downloader & Protector**.
5. Click **Run workflow** and fill in:
   - `video_url`: YouTube video link
   - `subtitle_language`: `en` or `fa`
   - `zip_password`: (optional) password for ZIP if file > 100 MB.
6. After completion, the subtitle file (or protected ZIP) will be committed to the `subtitles/` folder.
7. The **Job Summary** will show the direct download link and, if encrypted, the password.

### Example
Run with this public video (English subtitles available, no Persian):  
`video_url`: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`  
`subtitle_language`: `fa`

Expected output:
- `subtitles/Rick_Astley_Never_Gonna_Give_You_Up.fa.srt` (translated)

---

## 🇮🇷 فارسی

### امکانات
- دانلود زیرنویس یوتیوب با فرمت **SRT**
- انتخاب زبان **انگلیسی (en)** یا **فارسی (fa)**
- در صورت نبود زیرنویس فارسی، ترجمه خودکار از انگلیسی به فارسی
- اگر حجم فایل زیرنویس بیشتر از **۱۰۰ مگابایت** شد، به صورت **ZIP رمزگذاری شده با AES-256** ذخیره می‌شود
- اجرای کاملاً خودکار از طریق **GitHub Actions**

### راهنمای استفاده (پس از Fork)
1. مخزن را Fork کنید.
2. به مسیر **Settings** → **Secrets and variables** → **Actions** بروید.
3. یک Secret جدید با نام `GH_PAT` و مقدار یک **Personal Access Token** (با دسترسی `repo` یا `workflow`) ایجاد کنید.
4. به تب **Actions** رفته و **YouTube Subtitle Downloader & Protector** را انتخاب کنید.
5. روی **Run workflow** کلیک کرده و مقادیر زیر را وارد کنید:
   - `video_url`: لینک ویدیوی یوتیوب
   - `subtitle_language`: `en` یا `fa`
   - `zip_password`: (اختیاری) رمز عبور برای فایل ZIP در صورت نیاز
6. پس از پایان کار، فایل نهایی (SRT یا ZIP) در پوشه `subtitles/` ذخیره شده و در **Job Summary** لینک دانلود نمایش داده می‌شود.
7. چنانچه فایل ZIP ایجاد شده باشد، رمز عبور **تنها در خلاصه اکشن** نمایش داده می‌شود.

### مثال
اجرا با این ویدیوی عمومی (زیرنویس انگلیسی دارد ولی فارسی ندارد):  
`video_url`: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`  
`subtitle_language`: `fa`

خروجی مورد انتظار:
- فایل `subtitles/Rick_Astley_Never_Gonna_Give_You_Up.fa.srt` (ترجمه‌شده)

---

## تست‌ها
برای اجرای تست‌ها:
```bash
pip install -r requirements.txt
pytest tests/
