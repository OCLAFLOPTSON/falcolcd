"""
A MicroPython library of drivers and utilities for character LCD displays

Version: 0.1

Current Modules:
    HD44780 I2C Driver:
        A driver for HD44780-compatible character LCDs using an I2C
        backpack.

        Features:
            - 4-bit HD44780 protocol over I2C
            - Single character output
            - Multi-character string output
            - Cursor control
            - Custom character support
            - Backlight control

Planned Modules:
    This library is designed to expand to include:
        - SPI-based LCD controllers
        - Parallel GPIO HD44780 drivers
        - OLED character-mode abstractions (if applicable)
        - Unified display interface layer across controllers

License: MIT
Copyright 2026 Timothy S Falco

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the “Software”),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

__version__ = 0.1

from hd44780 import HD44780
from special_char import SpecialCharacters
