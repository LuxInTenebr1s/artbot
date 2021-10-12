#!/usr/bin/env python3
"""Main module."""

import logging

from dynaconf import (
    settings
)
from telegram.ext import (
    Updater
)

logger = logging.getLogger(__name__)

def _set_log_config():
    try:
        log_level = getattr(logging, settings.LOG_LEVEL.upper())
    except ValueError:
        log_level = logging.INFO
    finally:
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=log_level,
        )
    settings.LOG_LEVEL = "warning"

def artbot_app():
    """Artbot main entrypoint."""

    _set_log_config()
    logger.info(f'Starting \'{__name__}\' now.')

    updater = Updater(settings.TOKEN)

    # Start bot polling mode
    updater.start_polling()

    # Push updater to another thread
    updater.idle()

def test():
    """Testing function."""
    from artbot.signboard import DMXBoard # pylint: disable=C0415
    board = DMXBoard()
    board.set_text('test')

if __name__ == '__main__':
    artbot_app()
