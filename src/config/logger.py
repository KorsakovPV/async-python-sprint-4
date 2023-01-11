import logging
from logging.config import dictConfig


def get_logger(logger_name: str, log_level: str = 'INFO') -> logging.Logger:
    logger_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '[%(filename)s:%(lineno)s - %(funcName)20s()] %(asctime)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': log_level,
                'formatter': 'default',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stderr',
            },
            'file': {
                'level': log_level,
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'default',
                'filename': 'log_file.log',
                'maxBytes': 500000,
                'backupCount': 10
            }
        },
        'loggers': {
            '': {
                'handlers': ['file', 'console'],
                'level': log_level,
                'propagate': False
            },
        }
    }

    dictConfig(logger_config)

    return logging.getLogger(logger_name)


LOG_LEVEL = 'DEBUG'

logger = get_logger('root', LOG_LEVEL)

###################################################################################################
# Логер рекомендованный практикумом
# LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# LOG_DEFAULT_HANDLERS = ['console', ]
#
# # Настраивается логирование uvicorn-сервера
# # Про логирование в Python можно прочитать в документации
# # https://docs.python.org/3/howto/logging.html
# # https://docs.python.org/3/howto/logging-cookbook.html
#
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': LOG_FORMAT
#         },
#         'default': {
#             '()': 'uvicorn.logging.DefaultFormatter',
#             'fmt': '%(levelprefix)s %(message)s',
#             'use_colors': None,
#         },
#         'access': {
#             '()': 'uvicorn.logging.AccessFormatter',
#             'fmt': "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s",
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose',
#         },
#         'default': {
#             'formatter': 'default',
#             'class': 'logging.StreamHandler',
#             'stream': 'ext://sys.stdout',
#         },
#         'access': {
#             'formatter': 'access',
#             'class': 'logging.StreamHandler',
#             'stream': 'ext://sys.stdout',
#         },
#     },
#     'loggers': {
#         '': {
#             'handlers': LOG_DEFAULT_HANDLERS,
#             'level': 'INFO',
#         },
#         'uvicorn.error': {
#             'level': 'INFO',
#         },
#         'uvicorn.access': {
#             'handlers': ['access'],
#             'level': 'INFO',
#             'propagate': False,
#         },
#     },
#     'root': {
#         'level': 'INFO',
#         'formatter': 'verbose',
#         'handlers': LOG_DEFAULT_HANDLERS,
#     },
# }

# Мой логер
# log_level: str = 'INFO'
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'default': {
#             'format': '[%(filename)s:%(lineno)s - %(funcName)20s()] %(asctime)s %(message)s'
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': log_level,
#             'formatter': 'default',
#             'class': 'logging.StreamHandler',
#             'stream': 'ext://sys.stderr',
#         },
#         'file': {
#             'level': log_level,
#             'class': 'logging.handlers.RotatingFileHandler',
#             'formatter': 'default',
#             'filename': 'log_file.log',
#             'maxBytes': 500000,
#             'backupCount': 10
#         }
#     },
#     'loggers': {
#         '': {
#             'handlers': ['file', 'console'],
#             'level': log_level,
#             'propagate': False
#         },
#     }
# }

# logging_config.dictConfig(LOGGING)