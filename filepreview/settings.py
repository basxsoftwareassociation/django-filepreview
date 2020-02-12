INSTALLED_APPS = []
DEBUG = True
USE_TZ = True
USE_I18N = True
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
MIDDLEWARE_CLASSES = ()
SECRET_KEY = "test"  # nosec
