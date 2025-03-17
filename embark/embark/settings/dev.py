__copyright__ = 'Copyright 2021-2025 Siemens Energy AG'
__author__ = 'Benedikt Kuehne'
__license__ = 'MIT'

from pathlib import Path
import os
import pytz

from dotenv import load_dotenv

from embark.helper import get_emba_modules, count_emba_modules, get_version_strings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=os.path.join(BASE_DIR.parent, '.env'))
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = ['*']

EMBA_ROOT = os.path.join(BASE_DIR.parent, 'emba')
EMBA_LOG_ROOT = os.path.join(BASE_DIR.parent, 'emba_logs')
EMBA_LOG_URL = 'emba_logs/'

DEBUG = True
DOMAIN = "embark.local"

EMAIL_ACTIVE = True
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR.parent, 'mail')


INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5',
    'django_tables2',
    'mod_wsgi.server',
    'django_apscheduler',
    'uploader',
    'users',
    'reporter',
    'dashboard',
    'tracker',
    'porter',
    'updater'
]

AUTH_USER_MODEL = 'users.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'embark.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', EMBA_LOG_ROOT],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'embark.context_processor.embark_version'
            ],
        },
    },
]

CSRF_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_HTTPONLY = False  # False since we will grab it via universal-cookies

SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False

WSGI_APPLICATION = 'embark.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get("DATABASE_PASSWORD"),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT'),
        'CONN_MAX_AGE': 300,
        'TEST': {'NAME': 'test_db'},
    },
}

# Logging stuff
# ERRORS/WARNINGS->console
# DEBUG->debug.log
# INFO->embark.log
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {process:d} {thread:d} {pathname} {levelname} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console_handler': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'debug_handler': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filters': ['require_debug_true'],
            'formatter': 'verbose',
            'filename': BASE_DIR / 'debug.log',
        },
        'info_handler': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename': BASE_DIR / 'embark.log',
        },
    },
    'loggers': {
        '': {
            'level': 'WARNING',
            'handlers': ['info_handler', 'console_handler'],
        },
        'updater': {
            'handlers': ['debug_handler', 'info_handler', 'console_handler'],
            'level': 'DEBUG',
        },
        'uploader': {
            'handlers': ['debug_handler', 'info_handler', 'console_handler'],
            'level': 'DEBUG',
        },
        'dashboard': {
            'handlers': ['debug_handler', 'info_handler', 'console_handler'],
            'level': 'DEBUG',
        },
        'users': {
            'handlers': ['debug_handler', 'info_handler', 'console_handler'],
            'level': 'DEBUG',
        },
        'reporter': {
            'handlers': ['debug_handler', 'info_handler', 'console_handler'],
            'level': 'DEBUG',
        },
        'porter': {
            'handlers': ['debug_handler', 'info_handler', 'console_handler'],
            'level': 'DEBUG',
        },
        'tracker': {
            'handlers': ['debug_handler', 'info_handler', 'console_handler'],
            'level': 'DEBUG',
        },
        'embark': {
            'handlers': ['debug_handler', 'info_handler', 'console_handler'],
            'level': 'DEBUG',
        },
        'requests': {
            'handlers': ['info_handler'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 4,
        },
    }
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.environ.get('TIME_ZONE', 'UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR.parent, 'static')
STATICFILES_DIRS = [
    BASE_DIR / 'static/'
]
# STATICFILES_STORAGE
# STATICFILES_FINDERS

# URL of Login-Page
LOGIN_URL = ''

# URL of Logout-Page
LOGOUT_REDIRECT_URL = ''

# Added for FIle storage to get the path to save Firmware images.
MEDIA_ROOT = os.path.join(BASE_DIR.parent, 'media')
MEDIA_URL = '/media/'

# Active Firmware
ACTIVE_FW = os.path.join(BASE_DIR.parent, 'uploadedFirmwareImages/active/')

REDIS_HOST = os.environ.get('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
ASGI_APPLICATION = 'embark.asgi_dev.application'

# Format string for displaying run time timestamps in the Django admin site. The default
# just adds seconds to the standard Django format, which is useful for displaying the timestamps
# for jobs that are scheduled to run on intervals of less than one minute.
#
# See https://docs.djangoproject.com/en/dev/ref/settings/#datetime-format for format string
# syntax details.
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"

# Maximum run time allowed for jobs that are triggered manually via the Django admin site, which
# prevents admin site HTTP requests from timing out.
#
# Longer running jobs should probably be handed over to a background task processing library
# that supports multiple background worker processes instead (e.g. Dramatiq, Celery, Django-RQ,
# etc. See: https://djangopackages.org/grids/g/workers-queues-tasks/ for popular options).
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds

# redis/channel layers setup
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        }
    },
}
# TODO check this https://docs.djangoproject.com/en/5.1/topics/cache/
TEMP_DIR = Path("/tmp/")

try:
    EMBA_MODULE_DICT = get_emba_modules(EMBA_ROOT)
except FileNotFoundError as file_error:
    EMBA_MODULE_DICT = {
        'D_Modules': [
            ('d10', 'D10_firmware_diffing'),
            ('d02', 'D02_firmware_diffing_bin_details'),
            ('d05', 'D05_firmware_diffing_extractor')
        ],
        'F_Modules': [
            ('f02', 'F02_toolchain'),
            ('f50', 'F50_base_aggregator'),
            ('f15', 'F15_cyclonedx_sbom'),
            ('f05', 'F05_qs_resolver'),
            ('f10', 'F10_license_summary'),
            ('f20', 'F20_vul_aggregator')
        ],
        'L_Modules': [
            ('l99', 'L99_cleanup'),
            ('l35', 'L35_metasploit_check'),
            ('l10', 'L10_system_emulation'),
            ('l23', 'L23_vnc_checks'),
            ('l25', 'L25_web_checks'),
            ('l20', 'L20_snmp_checks'),
            ('l22', 'L22_upnp_hnap_checks'),
            ('l15', 'L15_emulated_checks_nmap')
        ],
        'P_Modules': [
            ('p15', 'P15_ubi_extractor'),
            ('p60', 'P60_deep_extractor'),
            ('p02', 'P02_firmware_bin_file_check'),
            ('p35', 'P35_UEFI_extractor'),
            ('p14', 'P14_ext_mounter'),
            ('p07', 'P07_windows_exe_extract'),
            ('p25', 'P25_android_ota'),
            ('p18', 'P18_BMC_decryptor'),
            ('p99', 'P99_prepare_analyzer'),
            ('p50', 'P50_binwalk_extractor'),
            ('p20', 'P20_foscam_decryptor'),
            ('p40', 'P40_DJI_extractor'),
            ('p22', 'P22_Zyxel_zip_decrypt'),
            ('p17', 'P17_gpg_decompress'),
            ('p65', 'P65_package_extractor'),
            ('p21', 'P21_buffalo_decryptor'),
            ('p19', 'P19_bsd_ufs_mounter'),
            ('p23', 'P23_qemu_qcow_mounter'),
            ('p55', 'P55_unblob_extractor'),
            ('p10', 'P10_vmdk_extractor')
        ],
        'Q_Modules': [('q02', 'Q02_openai_question')],
        'S_Modules': [
            ('s100', 'S100_command_inj_check'),
            ('s99', 'S99_grepit'),
            ('s90', 'S90_mail_check'),
            ('s03', 'S03_firmware_bin_base_analyzer'),
            ('s20', 'S20_shell_check'),
            ('s02', 'S02_UEFI_FwHunt'),
            ('s45', 'S45_pass_file_check'),
            ('s12', 'S12_binary_protection'),
            ('s23', 'S23_lua_check'),
            ('s110', 'S110_yara_check'),
            ('s60', 'S60_cert_file_check'),
            ('s35', 'S35_http_file_check'),
            ('s24', 'S24_kernel_bin_identifier'),
            ('s16', 'S16_ghidra_decompile_checks'),
            ('s50', 'S50_authentication_check'),
            ('s108', 'S108_stacs_password_search'),
            ('s21', 'S21_python_check'),
            ('s109', 'S109_jtr_local_pw_cracking'),
            ('s17', 'S17_cwe_checker'),
            ('s25', 'S25_kernel_check'),
            ('s09', 'S09_firmware_base_version_check'),
            ('s65', 'S65_config_file_check'),
            ('s18', 'S18_capa_checker'),
            ('s36', 'S36_lighttpd'),
            ('s05', 'S05_firmware_details'),
            ('s115', 'S115_usermode_emulator'),
            ('s55', 'S55_history_file_check'),
            ('s27', 'S27_perl_check'),
            ('s80', 'S80_cronjob_check'),
            ('s19', 'S19_apk_check'),
            ('s95', 'S95_interesting_files_check'),
            ('s75', 'S75_network_check'),
            ('s106', 'S106_deep_key_search'),
            ('s107', 'S107_deep_password_search'),
            ('s15', 'S15_radare_decompile_checks'),
            ('s07', 'S07_bootloader_check'),
            ('s22', 'S22_php_check'),
            ('s26', 'S26_kernel_vuln_verifier'),
            ('s85', 'S85_ssh_check'),
            ('s10', 'S10_binaries_basic_check'),
            ('s13', 'S13_weak_func_check'),
            ('s08', 'S08_main_package_sbom'),
            ('s40', 'S40_weak_perm_check'),
            ('s118', 'S118_busybox_verifier'),
            ('s14', 'S14_weak_func_radare_check'),
            ('s116', 'S116_qemu_version_detection'),
            ('s04', 'S04_windows_basic_analysis'),
            ('s06', 'S06_distribution_identification')
        ]
    }
EMBA_S_MOD_CNT, EMBA_P_MOD_CNT, EMBA_Q_MOD_CNT, EMBA_L_MOD_CNT, EMBA_F_MOD_CNT, EMBA_D_MOD_CNT = count_emba_modules(EMBA_MODULE_DICT)

VERSION = get_version_strings()
