"""
Kaitian - Keyboard Scan Code to English Mapper
Version 0.1.0 (Public Demo)

Demonstrates the keyboard scan-code-to-character mapping pipeline.
This public version maps PS/2 Set 1 scan codes to English letters only.
Chinese character mapping is a separate internal module.

How it works:
1. Physical key press generates a scan code (e.g., 0x1E for 'A')
2. This module maps the scan code to the corresponding English character
3. In the full system, this feeds into the Chinese semantic layer

PS/2 Set 1 scan codes referenced from:
https://wiki.osdev.org/PS/2_Keyboard
"""

from typing import Dict, Optional


# PS/2 Set 1 scan code → English character (make codes only)
SCAN_TO_ENGLISH: Dict[int, str] = {
    # ── Letters ──
    0x1E: 'a', 0x30: 'b', 0x2E: 'c', 0x20: 'd', 0x12: 'e',
    0x21: 'f', 0x22: 'g', 0x23: 'h', 0x17: 'i', 0x24: 'j',
    0x25: 'k', 0x26: 'l', 0x32: 'm', 0x31: 'n', 0x18: 'o',
    0x19: 'p', 0x10: 'q', 0x13: 'r', 0x1F: 's', 0x14: 't',
    0x16: 'u', 0x2F: 'v', 0x11: 'w', 0x2D: 'x', 0x15: 'y',
    0x2C: 'z',

    # ── Numbers ──
    0x02: '1', 0x03: '2', 0x04: '3', 0x05: '4', 0x06: '5',
    0x07: '6', 0x08: '7', 0x09: '8', 0x0A: '9', 0x0B: '0',

    # ── Modifiers ──
    0x1D: 'ctrl',  0x2A: 'lshift',  0x36: 'rshift',
    0x38: 'alt',   0x39: 'space',

    # ── Punctuation ──
    0x29: '`',  0x0C: '-',  0x0D: '=',  0x1A: '[',
    0x1B: ']',  0x27: ';',  0x28: '\'', 0x2B: '\\',
    0x33: ',',  0x34: '.',  0x35: '/',  0x37: '*',

    # ── Navigation ──
    0x01: 'esc',      0x0E: 'backspace', 0x0F: 'tab',
    0x1C: 'enter',    0x3A: 'capslock',  0x3B: 'f1',
    0x3C: 'f2',      0x3D: 'f3',        0x3E: 'f4',
    0x3F: 'f5',      0x40: 'f6',        0x41: 'f7',
    0x42: 'f8',      0x43: 'f9',        0x44: 'f10',
    0x57: 'f11',     0x58: 'f12',
}

# Shift-modified versions for letters
SHIFT_MAP: Dict[str, str] = {c: c.upper() for c in 'abcdefghijklmnopqrstuvwxyz'}


class ScanCodeMapper:
    """
    Maps PS/2 keyboard scan codes to English characters.
    
    In the full Kaitian system, this is the first stage of the pipeline:
    Scan Code → English Character → Pinyin Sequence → Chinese Character → Semantic Token
    """

    def __init__(self):
        self.shift_pressed = False

    def map_scan_code(self, scan_code: int) -> Optional[str]:
        """
        Convert a PS/2 Set 1 scan code to its character representation.
        
        Args:
            scan_code: The raw scan code byte (e.g., 0x1E).
        
        Returns:
            The corresponding character string, or None if not recognized.
        """
        char = SCAN_TO_ENGLISH.get(scan_code)

        if char is None:
            return None

        if char in SHIFT_MAP and self.shift_pressed:
            return SHIFT_MAP[char]

        return char

    def process_sequence(self, scan_codes: list[int]) -> str:
        """
        Process a sequence of scan codes into a string.
        Handles shift toggling automatically.
        
        Args:
            scan_codes: List of scan code integers.
        
        Returns:
            The assembled string.
        """
        result = []
        for code in scan_codes:
            if code in (0x2A, 0x36):  # Shift pressed
                self.shift_pressed = True
                continue
            if code in (0xAA, 0xB6):  # Shift released (break codes)
                self.shift_pressed = False
                continue

            char = self.map_scan_code(code)
            if char and len(char) == 1:  # Skip multi-char labels like 'ctrl'
                result.append(char)

        return ''.join(result)

    def list_all_mappings(self) -> None:
        """Print all scan code to character mappings."""
        print(f"{'Scan Code':<12} {'Character':<12} {'Description'}")
        print("-" * 50)
        for code, char in sorted(SCAN_TO_ENGLISH.items()):
            print(f"0x{code:02X} ({code:3d})   {char:<12}")


# ─── Demo ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mapper = ScanCodeMapper()

    print("=" * 60)
    print("Kaitian Scan Code Mapper (Public Demo)")
    print("=" * 60)

    # Demo 1: Show full mapping table
    print("\nFull scan code → English mapping:")
    print("-" * 50)
    mapper.list_all_mappings()

    # Demo 2: Simulate typing "hello world"
    print("\n" + "=" * 60)
    print("Demo: Simulating typing 'hello world'")
    print("=" * 60)

    hello_scan_codes = [
        0x23,  # h
        0x12,  # e
        0x26,  # l
        0x26,  # l
        0x18,  # o
        0x39,  # space
        0x11,  # w
        0x18,  # o
        0x13,  # r
        0x26,  # l
        0x20,  # d
    ]

    result = mapper.process_sequence(hello_scan_codes)
    print(f"Scan codes: {[f'0x{c:02X}' for c in hello_scan_codes]}")
    print(f"Result: '{result}'")

    # Demo 3: Simulate typing "Kaitian" with shift
    print("\n" + "=" * 60)
    print("Demo: Simulating typing 'Kaitian' (with Shift)")
    print("=" * 60)

    kaitian_scan_codes = [
        0x2A,  # lshift down
        0x25,  # k → K
        0xAA,  # lshift up
        0x1E,  # a
        0x17,  # i
        0x14,  # t
        0x17,  # i
        0x1E,  # a
        0x31,  # n
    ]

    result2 = mapper.process_sequence(kaitian_scan_codes)
    print(f"Scan codes: {[f'0x{c:02X}' for c in kaitian_scan_codes]}")
    print(f"Result: '{result2}'")
