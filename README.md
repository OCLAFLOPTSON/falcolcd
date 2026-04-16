# A MicroPython library of drivers and utilities for character LCD displays

Version: 0.1

---
## Current Modules:

- ### HD44780 I2C Driver:

    A driver for HD44780-compatible character LCDs using an I2C
    backpack.

    ### Features:
    - 4-bit HD44780 protocol over I2C
    - Single character output
    - Multi-character string output
    - Cursor control
    - Custom character support
    - Backlight control

## Planned Modules:

This library is designed to expand to include:
- SPI-based LCD controllers
- Parallel GPIO HD44780 drivers
- OLED character-mode abstractions (if applicable)
- Unified display interface layer across controllers
---

## Installation

```bash
git clone <address>
```
---

## Example Usage (HD44780 I2C)

```python
from time import sleep
from machine import I2C, Pin
from onewire import OneWire
from ds18x20 import DS18X20
from Screens import HD44780, SpecialCharacters

# Define LCD screen controller
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
lcd = HD44780(i2c=i2c, rows=2, cols=16)
lcd.create_char(0, SpecialCharacters.Door.open)
lcd.create_char(1, SpecialCharacters.Door.closed)

# Initialize Screen
lcd.clear()
lcd.control_backlight(True)
lcd.write_str("Hello World", (0,3))

# Display Sensor Data In Realtime
reed_switch = Pin(0, Pin.IN, Pin.PULL_UP) # door contact sensor
onewire_probe = Pin(1)                    # OneWire temperature sensor
onewire = DS18X20(OneWire(onewire_probe))
onewire_rom = onewire.scan()[0]

while True:
    onewire.convert_temp()
    sleep(0.75)
    TEMP = str(int((onewire.read_temp(onewire_rom) * 9/5) + 32))
    lcd.clear()
    lcd.write_str(TEMP, (0,0))
    if reed_switch.value():
        lcd.write_str(lcd.special_char(1), (1,0))
    else:
        lcd.write_str(lcd.special_char(0), (1,0))
```
---

## Custom Characters

The library supports CGRAM-based custom characters (max 8 per display).

```python
rombus = [
    0b00000, # _____
    0b00100, # __#__
    0b01010, # _#_#_
    0b10001, # #___#
    0b10001, # #___#
    0b01010, # _#_#_
    0b00100, # __#__
    0b00000  # _____
]
lcd.create_char(0, SpecialCharacters.smiley_face)
lcd.create_char(1, rombus)
```

---

## License: MIT

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
