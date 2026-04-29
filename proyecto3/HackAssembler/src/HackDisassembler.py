#*********
# HackDisassembler.py – Translates Hack binary back to assembly
# Autor: Emmanuel
#*********

import os
import sys


# ── Reverse-lookup tables ─────────────────────────────────────────────────────

_DEST_TABLE: dict[str, str] = {
    '000': '',
    '001': 'M',
    '010': 'D',
    '011': 'MD',
    '100': 'A',
    '101': 'AM',
    '110': 'AD',
    '111': 'AMD',
}

_JUMP_TABLE: dict[str, str] = {
    '000': '',
    '001': 'JGT',
    '010': 'JEQ',
    '011': 'JGE',
    '100': 'JLT',
    '101': 'JNE',
    '110': 'JLE',
    '111': 'JMP',
}

_COMP_TABLE: dict[str, str] = {
    # a=0
    '0101010': '0',
    '0111111': '1',
    '0111010': '-1',
    '0001100': 'D',
    '0110000': 'A',
    '0001101': '!D',
    '0110001': '!A',
    '0001111': '-D',
    '0110011': '-A',
    '0011111': 'D+1',
    '0110111': 'A+1',
    '0001110': 'D-1',
    '0110010': 'A-1',
    '0000010': 'D+A',
    '0010011': 'D-A',
    '0000111': 'A-D',
    '0000000': 'D&A',
    '0010101': 'D|A',
    # a=1
    '1110000': 'M',
    '1110001': '!M',
    '1110011': '-M',
    '1110111': 'M+1',
    '1110010': 'M-1',
    '1000010': 'D+M',
    '1010011': 'D-M',
    '1000111': 'M-D',
    '1000000': 'D&M',
    '1010101': 'D|M',
    # Shift extension
    '0000001': 'D<<1',
    '0001001': 'A<<1',
    '1001001': 'M<<1',
    '0000011': 'D>>1',
    '0001011': 'A>>1',
    '1001011': 'M>>1',
}


def _decode_instruction(bits: str) -> str:
    if len(bits) != 16:
        raise ValueError(f"Expected 16 bits, got {len(bits)}")
    if bits[0] == '0':
        value = int(bits, 2)
        return f'@{value}'
    comp_bits = bits[3:10]
    dest_bits = bits[10:13]
    jump_bits = bits[13:16]
    comp_mnem = _COMP_TABLE.get(comp_bits, f'???({comp_bits})')
    dest_mnem = _DEST_TABLE.get(dest_bits, '???')
    jump_mnem = _JUMP_TABLE.get(jump_bits, '???')
    result = ''
    if dest_mnem:
        result += dest_mnem + '='
    result += comp_mnem
    if jump_mnem:
        result += ';' + jump_mnem
    return result


def disassemble(input_path: str) -> None:
    base = os.path.splitext(input_path)[0]
    output_path = base + 'Dis.asm'
    asm_lines: list[str] = []
    with open(input_path, 'r') as f:
        for lineno, raw in enumerate(f, start=1):
            bits = raw.strip()
            if not bits:
                continue
            if len(bits) != 16 or not all(c in '01' for c in bits):
                continue
            asm_lines.append(_decode_instruction(bits))
    with open(output_path, 'w') as f:
        f.write('\n'.join(asm_lines) + '\n')
    print(f"Disassembled → {output_path}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)
    disassemble(sys.argv[1])
