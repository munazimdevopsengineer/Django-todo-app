from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'dev-secret-key-change-me' # OK for local dev only
DEBUG = True
ALLOWED_HOSTS: list[str] = []


INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',


# our app
'todos',
]


MIDDLEWARE = [
'django.middleware.security.SecurityMiddleware',
'django.contrib.sessions.middleware.SessionMiddleware',
'django.middleware.common.CommonMiddleware',
'django.middleware.csrf.CsrfViewMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'django.contrib.messages.middleware.MessageMiddleware',
'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'mysite.urls'


TEMPLATES = [
{
'BACKEND': 'django.template.backends.django.DjangoTemplates',
'DIRS': [BASE_DIR / 'templates'], # so we can use templates/base.html
'APP_DIRS': True,
'OPTIONS': {
'context_processors': [
'django.template.context_processors.debug',
'django.template.context_processors.request',
'django.contrib.auth.context_processors.auth',
'django.contrib.messages.context_processors.messages',
],
},
},
]


WSGI_APPLICATION = 'mysite.wsgi.application'


DATABASES = {
'default': {
'ENGINE': 'django.db.backends.sqlite3',
'NAME': BASE_DIR / 'db.sqlite3',
}
}


AUTH_PASSWORD_VALIDATORS = [] # simplify dev


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata' # set to your local TZ
USE_I18N = True
USE_TZ = True


STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'todo_list'
LOGOUT_REDIRECT_URL = 'login'

SESSION_COOKIE_AGE = 60*60*24*30  # 30 days
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

