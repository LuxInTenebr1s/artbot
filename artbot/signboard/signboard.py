"""Module to describe Signboard functionality."""

from typing import List
import logging

from dmx import (
        Colour,
        DMXInterface,
        DMXLight3Slot,
        DMXUniverse
)

logger = logging.getLogger(__name__)

LETTERS_COUNT = 4
LIGHTS_NUBMER = 14 * LETTERS_COUNT

class DMXBoard():
    """Signboard over DMX driver class."""

    def __init__(self,
                 universe: int = 1,
                 base_address: int = 1):
        self._interface = DMXInterface("FT232R")
        self._universe = DMXUniverse(universe)
        self._lights = list()
        self._color = Colour(255, 0, 255)

        self._import_map_file(None)

        for idx in range(LIGHTS_NUBMER):
            address = base_address + (idx * 3)
            light = DMXLight3Slot(address=address)
            self._universe.add_light(light)
            self._lights.append(light)

    def set_text(self, text: str):
        """Set text DMX realization."""
        encoded = self._decode_text(text)

        for letter_idx, code in enumerate(encoded):
            for segment_idx, state in enumerate(self._decode_letter(code)):
                logger.debug(f'{letter_idx}:{segment_idx}: {state}')
                light_idx = letter_idx * 14 + segment_idx
                colour = self._color if state else Colour(0, 0, 0)

                self._lights[light_idx].set_colour(colour)


    def _import_map_file(self, path: str) -> dict:
        if not path:
            self._mapping = dict(map(lambda idx: (idx, idx), range(256)))
            logger.debug(f'Loaded mapping file:\n{self._mapping}')
        else:
            raise ValueError('Not yet implemented')

    def _decode_letter(self, letter: int) -> List[bool]:
        while letter:
            yield letter & 1
            letter >>= 1

    def _decode_text(self, text: str) -> List[int]:
        try:
            text = text.decode('ascii')
        except UnicodeDecodeError as exc:
            raise ValueError("Not an ASCII-decodable") from exc

        return map(lambda x: self._mapping[x], text)


class Signboard():
    """Signboard module main class."""

    def __init__(self):
        self._driver = None

    def set_text(self, text: str):
        """Set text to a signboard."""
        logger.info(f'Setting signboard text: f{text}')

        try:
            self._driver.set_text(text)
        except ValueError:
            logger.warning('set_text: no driver implementation')
        except Exception as exc:
            logger.error(f'Failed to set_text: {exc}')

    def flush(self):
        """Flush signboard."""
        logger.info('Flushing signboard')

        try:
            self._driver.flush()
        except ValueError:
            logger.warning('flush: no driver implementation')
        except Exception as exc:
            logger.error(f'Failed to flush: {exc}')
