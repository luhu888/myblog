"""
Django settings for myblog project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import datetime
import os
import time
import logging
import django.utils.log
import logging.handlers
import json


def read_config():
    """"读取配置"""
    with open("./setting.json", encoding='utf-8') as json_file:
        return dict(json.load(json_file))
        # print(config)
ret = read_config()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k-)efxao!irze6^i2u@cryrysw&q4h2qn(zts6-r6d1*4@rh4@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']   # 加星表示任何域名都可以访问
SIMPLEUI_HOME_INFO = False

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'DjangoUeditor',   # 注册APP应用
    'new_user',
    'rest_framework',
    # 'rest_framework.authtoken',  # 后台显示token
    'rest_auth',
    'corsheaders',
    'myAPI',
    'templatetest',
    # 'debug_toolbar',
]
# INTERNAL_IPS = [
#     # ...
#     '127.0.0.1',
# ]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'myblog.urls'
# DEBUG_TOOLBAR_CONFIG = {
#     "JQUERY_URL": '//cdn.bootcss.com/jquery/2.2.4/jquery.min.js',
# }
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 没了这句，
        # 会显示django.template.exceptions.TemplateDoesNotExist: menu2.html
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

WSGI_APPLICATION = 'myblog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': ret["NAME"],
        'USER': ret["USER"],
        'PASSWORD': ret["PASSWORD"],
        'HOST': ret["HOST"],
        'PORT': ret["PORT"],
        }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
LOGIN_URL = '/new_user/login.html'
STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
TEMPLATE_DIRS = (os.path.join(BASE_DIR,  'templates'),)
AUTH_USER_MODEL = 'new_user.MyUser'   # 指定新的用户model
# REST_USE_JWT = True
cur_path = os.path.dirname(os.path.realpath(__file__))  # log_path是存放日志的路径
log_path = os.path.join(os.path.dirname(cur_path), 'logs')
if not os.path.exists(log_path):
    os.mkdir(log_path)  # 如果不存在这个logs文件夹，就自动创建一个

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAdminUser',
        # 'rest_framework.permissions.DjangoObjectPermissions',
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        # 'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.IsAuthenticatedOrReadOnly',

    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',   # 不加这个迁移数据库会有警告
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',

    'PAGE_SIZE': 5,
    "DEFAULT_AUTHENTICATION_CLASSES": (
       # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
       # 'rest_framework.authentication.SessionAuthentication',
       # 'rest_framework.authentication.BasicAuthentication',  # token认证
       ),
    'EXCEPTION_HANDLER': 'myAPI.exceptions.custom_exception_handler',
}

#配置自定义的认证
# AUTHENTICATION_BACKENDS = [
#     # 默认值：['django.contrib.auth.backends.ModelBackend']
#     ['new_user.views.UserPhoneEmailAuthBackend',]
# ]

JWT_AUTH = {
    # jwt_token的有效期
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),  # days=1 代表 token时效为1天
    # jwt是否自动刷新
    'JWT_ALLOW_REFRESH': True,
    'JWT_VERIFY': True,    # 如果密码错误，它将引发一个jwt.DecodeError
    'JWT_VERIFY_EXPIRATION': True,    # 将过期设置为True，这意味着令牌将在一段时间后过期。 默认时间是五分钟
    'JWT_AUTH_HEADER_PREFIX': 'JWT',   # 需要与令牌一起发送的Authorization标头值前缀。默认值为JWT
    # 配置自定义的jwt返回内容路径(登录成功的返回)
    # 'JWT_RESPONSE_PAYLOAD_HANDLER': 'new_user.views.jwt_response_payload_handler',
    # 登陆失败时自定义的返回结构
    'JWT_RESPONSE_PAYLOAD_ERROR_HANDLER': 'new_user.views.jwt_response_payload_error_handler',

            }


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        # 日志格式
        'standard': {
            'format': '[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] '
                      '[%(levelname)s]- %(message)s'},
        'simple': {  # 简单格式
            'format': '%(levelname)s %(message)s'
        },
    },
    # 过滤
    'filters': {
    },
    # 定义具体处理日志的方式
    'handlers': {
        # 默认记录所有日志
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_path, 'all-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码，否则打印出来汉字乱码
        },
        # 输出错误日志
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_path, 'error-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码
        },
        # 控制台输出
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        # 输出info日志
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_path, 'info-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',  # 设置默认编码
        },
    },
    # 配置用哪几种 handlers 来处理日志
    'loggers': {
        # 类型 为 django 处理所有类型的日志， 默认调用
        'django': {
            'handlers': ['default', 'console'],
            'level': 'INFO',
            'propagate': True
        },
        # log 调用时需要当作参数传入
        'log': {
            'handlers': ['error', 'info', 'console', 'default'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}
