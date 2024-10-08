import logging, inspect

from celery import shared_task


def logger(message: str, message_type: str = 'debug') -> None:
    """
        Логирование сообщений

        :param message: str - Сообщение
        :param message_type: str - Тип сообщения ('debug', 'info', 'warning', 'error', 'critical')
    """
    message = f"{inspect.stack()[1].function} {message}"

    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)

    match message_type:
        case 'info':
            log.info(message)
        case 'warning':
            log.warning(message)
        case 'error':
            log.error(message)
        case 'critical':
            log.critical(message)
        case _:
            log.debug(message)
