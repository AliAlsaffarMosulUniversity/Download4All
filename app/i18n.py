"""Very small translation layer: English strings are the keys, Arabic is the translation."""

LANG = "en"

AR = {
    # toolbar / tray
    "Add URL": "إضافة رابط",
    "Resume": "استئناف",
    "Pause": "إيقاف مؤقت",
    "Pause All": "إيقاف الكل",
    "Delete": "حذف",
    "Scheduler": "الجدولة",
    "Settings": "الإعدادات",
    "Open Folder": "فتح المجلد",
    "Browser": "المتصفح",
    "About": "حول",
    "Donate": "تبرّع",
    "Show JDM": "إظهار البرنامج",
    "Add URL…": "إضافة رابط…",
    "Exit": "خروج",
    # columns
    "File Name": "اسم الملف",
    "Size": "الحجم",
    "Progress": "التقدم",
    "Speed": "السرعة",
    "Time Left": "الوقت المتبقي",
    "Status": "الحالة",
    "Connections": "الاتصالات",
    "Added": "تاريخ الإضافة",
    "Action": "إجراء",
    # statuses
    "Queued": "في الانتظار",
    "Downloading": "جارٍ التحميل",
    "Paused": "متوقف",
    "Completed": "مكتمل",
    "Error": "خطأ",
    "Scheduled": "مجدول",
    "Unknown": "غير معروف",
    # row buttons / menu
    "Open": "فتح",
    "Play": "تشغيل",
    "View": "عرض",
    "Play in JDM": "تشغيل داخل البرنامج",
    "Open with default program": "فتح بالبرنامج الافتراضي",
    "Download Again": "تحميل مرة أخرى",
    "Move to Schedule": "نقل إلى الجدولة",
    "Copy URL": "نسخ الرابط",
    "Show Error": "عرض الخطأ",
    "File not found. It may have been moved or deleted.": "الملف غير موجود، ربما نُقل أو حُذف.",
    # add dialog
    "Add Download": "إضافة تحميل",
    "URL:": "الرابط:",
    "File name:": "اسم الملف:",
    "Save to:": "الحفظ في:",
    "Connections:": "عدد الاتصالات:",
    "Video quality:": "جودة الفيديو:",
    "Browse…": "استعراض…",
    "Automatic (from server)": "تلقائي (من الخادم)",
    "Taken from the video title": "يؤخذ من عنوان الفيديو",
    "Video page detected – JDM will download the video itself.":
        "تم اكتشاف صفحة فيديو – سيحمّل البرنامج الفيديو نفسه.",
    "Download Now": "تحميل الآن",
    "Add to Schedule": "إضافة للجدولة",
    "Add Paused": "إضافة متوقفاً",
    "Cancel": "إلغاء",
    "Please enter a valid http:// or https:// URL.": "يرجى إدخال رابط صحيح يبدأ بـ http:// أو https://",
    "Best quality": "أعلى جودة",
    "Audio only (M4A)": "صوت فقط (M4A)",
    # settings
    "Language:": "اللغة:",
    "Default folder:": "مجلد التحميل:",
    "Download folder": "مجلد التحميل",
    "Connections per file:": "الاتصالات لكل ملف:",
    "Simultaneous downloads:": "التحميلات المتزامنة:",
    "Speed limit:": "حد السرعة:",
    "Unlimited": "غير محدود",
    "Show 'Add Download' window for browser downloads": "إظهار نافذة الإضافة عند التحميل من المتصفح",
    "Notify when a download completes": "التنبيه عند اكتمال التحميل",
    "Closing the window keeps JDM running in the tray": "إبقاء البرنامج يعمل بجانب الساعة عند إغلاق النافذة",
    "Restart JDM now to apply the new language?": "إعادة تشغيل البرنامج الآن لتطبيق اللغة الجديدة؟",
    "Choose the program language": "اختر لغة البرنامج",
    # scheduler
    "Enable scheduler": "تفعيل الجدولة",
    "Stop (pause) downloads at:": "إيقاف التحميلات عند:",
    "Downloads marked 'Scheduled' start automatically": "التحميلات المجدولة تبدأ تلقائياً",
    "Start at:": "البدء عند:",
    "Days:": "الأيام:",
    "Tip: right-click a download → 'Move to Schedule'.": "تلميح: انقر بالزر الأيمن على تحميل ← نقل إلى الجدولة.",
    "Mon": "الإثنين", "Tue": "الثلاثاء", "Wed": "الأربعاء", "Thu": "الخميس",
    "Fri": "الجمعة", "Sat": "السبت", "Sun": "الأحد",
    "Scheduler: scheduled downloads started": "الجدولة: بدأت التحميلات المجدولة",
    "Scheduler: downloads stopped": "الجدولة: توقفت التحميلات",
    # delete
    "Remove {n} download(s) from the list?": "حذف {n} من القائمة؟",
    "Also delete the file(s) from disk": "حذف الملفات من القرص أيضاً",
    # status bar
    "{n} active": "{n} نشط",
    "No speed limit": "بدون حد للسرعة",
    "Limit: {n} KB/s": "الحد: {n} KB/s",
    "Browser bridge port is busy – browser capture disabled.": "منفذ ربط المتصفح مشغول – التقاط المتصفح معطّل.",
    # notifications
    "Download complete": "اكتمل التحميل",
    "Download added:": "تمت إضافة التحميل:",
    "JDM is still running in the tray.": "البرنامج ما زال يعمل بجانب الساعة.",
    "Made in Mosul, Iraq": "صُنع في الموصل، العراق",
    # donate
    "Support free service software": "ادعم تصميم البرامج الخدمية المجانية",
    "JDM is free. If it helped you, you can support the design of more free service software.":
        "هذا البرنامج مجاني. إذا أفادك، يمكنك دعم تصميم المزيد من البرامج الخدمية المجانية.",
    "MasterCard number:": "رقم الماستر كارد:",
    "Copy number": "نسخ الرقم",
    "Copied": "تم النسخ",
    "Thank you for your support": "شكراً لدعمك",
    "Close": "إغلاق",
    # about / extension help
    "Email:": "البريد الإلكتروني:",
    "found": "موجود",
    "not found": "غير موجود",
    "Free download manager – no serial, no activation.": "برنامج تحميل مجاني – بدون رقم تسلسلي أو تفعيل.",
    "Multi-connection downloads, pause/resume, scheduler, speed limiter, browser capture, video downloads and a built-in media player.":
        "تحميل متعدد الاتصالات، إيقاف واستئناف، جدولة، تحديد السرعة، التقاط من المتصفح، تحميل الفيديو، ومشغّل وسائط مدمج.",
    "Add JDM to Chrome / Edge": "إضافة البرنامج إلى Chrome و Edge",
    "Open Chrome": "فتح Chrome",
    "Open Edge": "فتح Edge",
    "EXT_HELP": (
        "<b>تركيب إضافة المتصفح (مرة واحدة فقط):</b><ol>"
        "<li>ستُفتح صفحة الإضافات في المتصفح.</li>"
        "<li>فعّل خيار <b>Developer mode</b> في الأعلى.</li>"
        "<li>اضغط <b>Load unpacked</b>.</li>"
        "<li>الصق مسار هذا المجلد (تم نسخه) ثم اضغط <b>Select Folder</b>:<br>"
        "<code>{path}</code></li></ol>"
        "بعدها تنتقل التحميلات وفيديوهات يوتيوب إلى البرنامج تلقائياً."),
    # player
    "Media Player": "مشغّل الوسائط",
    "Fullscreen": "ملء الشاشة",
    "Fit": "ملاءمة",
    "Actual size": "الحجم الأصلي",
    "This file can't be played here. Open it with the default program?":
        "لا يمكن تشغيل هذا الملف هنا. هل تريد فتحه بالبرنامج الافتراضي؟",
    "Volume": "الصوت",
}

EN = {
    "EXT_HELP": (
        "<b>Install the JDM browser extension (one time only):</b><ol>"
        "<li>The browser will open the <b>Extensions</b> page.</li>"
        "<li>Turn on <b>Developer mode</b> (top-right).</li>"
        "<li>Click <b>Load unpacked</b>.</li>"
        "<li>Paste this folder path (already copied) and click <b>Select Folder</b>:<br>"
        "<code>{path}</code></li></ol>"
        "After that, downloads and YouTube videos go to JDM automatically."),
}


def set_language(lang):
    global LANG
    LANG = "ar" if lang == "ar" else "en"


def is_rtl():
    return LANG == "ar"


def T(text, **kw):
    """Translate `text` (English key) into the current language."""
    if LANG == "ar":
        out = AR.get(text, EN.get(text, text))
    else:
        out = EN.get(text, text)
    return out.format(**kw) if kw else out
