from machine import I2C
from asyncio import sleep_ms, sleep_us

class HD44780:
    '''
    A character LCD controller using the HD44780-compatible instruction
    set.
    '''
    class Commands:
        CLR = 0x01
        HOME = 0x02
        ENTRY_MODE = 0x06
        DISPLAY_ON = 0x0C
        DISPLAY_OFF = 0x08
        FUNCTION_SET = 0x28
        SET_DDRAM = 0x80
        SET_CGRAM = 0x40

    def __init__(self, i2c: I2C, rows: int, cols: int, addr: int=0x027):
        self.I2C = i2c
        self.addr = addr
        self.rows = rows
        self.cols = cols
        self._init()
    
    def _init(self):
        sleep_ms(50)
        for _ in range(3):
            self._write4(0x30)
            sleep_ms(5)
        self._write4(0x20)
        sleep_ms(5)

        self.command(self.Commands.LCD_FUNCTION_SET)
        self.command(self.Commands.LCD_DISPLAY_OFF)
        self.clear()
        self.command(self.Commands.LCD_ENTRY_MODE)
        self.command(self.Commands.LCD_DISPLAY_ON)

    def _write_byte(self, data):
        self.i2c.writeto(self.addr, bytes([data]))

    def _strobe(self, data):
        self._write_byte(data | 0x04)
        sleep_us(1)
        self._write_byte(data & ~0x04)
        sleep_us(50)

    def _write4(self, data):
        self._write_byte(data | self.backlight)
        self._strobe(data | self.backlight)

    def _send(self, value, mode):
        high = value & 0xF0
        low = (value << 4) & 0xF0
        self._write4(high | mode)
        self._write4(low | mode)

    def command(self, cmd):
        '''Send a command to the screen module.'''
        self._send(cmd, 0x00)

    def write_char(self, char_val):
        '''Write a single character at the current cursor position.'''
        self._send(char_val, 0x01)

    def clear(self):
        '''Clear the screen.'''
        self.command(self.Commands.LCD_CLR)
        sleep_ms(2)

    def home(self):
        '''Send a cursor home command to the screen module.'''
        self.command(self.Commands.LCD_HOME)
        sleep_ms(2)

    def set_cursor(self, row: int, col: int,
                   row_offsets=[0x00, 0x40, 0x14, 0x54]):
        '''Manually set cursor position.'''
        if row > self.rows:
            row = self.rows - 1
        addr = col + row_offsets[row]
        self.command(self.Commands.LCD_SET_DDRAM | addr)

    def write_str(self, str, cursor: tuple[int, int]|bool=False):
        '''Write a string to the screen module.'''
        if (cursor and
            type(cursor) == tuple and
            type(cursor[0]) == int and
            type(cursor[1]) == int):
            self.set_cursor(cursor[0], cursor[1])
        for char in str:
            self.write_char(ord(char))
    
    def control_backlight(self, on: bool):
        '''Turn the backlight on or off.'''
        if on:
            self.backlight = 0x01
            self._write_byte(self.backlight)
        else:
            self.backlight = 0x00
            self._write_byte(self.backlight)
        
    def create_char(self, slot: int, bitmap: list[int]):
        """
        ### Create a custom character in CGRAM.
        - Slots: 0-7
        - bitmap: list of 8 bytes (5-bit rows)
        """
        slot &= 0x07
        self.command(0x40 | (slot << 3))
        for row in bitmap:
            self.write_char(row)
    
    def special_char(self, slot: int):
        """
        ### Refer to a special character stored at slot in CGRAM.
        - Slots: 0-7
        """
        return chr(slot)