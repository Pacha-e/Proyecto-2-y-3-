#*********
# Code.py – Translates Hack assembly mnemonics to binary
# Autor: Emmanuel
#*********


class Code:
    """
    Translates Hack assembly language mnemonics into binary codes.

    Encoding reference (C-instruction layout):
        1 1 1  a c1 c2 c3 c4 c5 c6  d1 d2 d3  j1 j2 j3
        [15]   [13]                  [5]        [2]

    SHIFT EXTENSION (ALU Logic):
        Trigger: zx=0, nx=0, ny=0, no=1  (c1=0, c2=0, c4=0, c6=1)
        Source Select (zy / c3): 0=x (D), 1=y (A/M)
        Direction (f / c5): 0=Left, 1=Right

        Mappings (a + cccccc):
            D<<1 : 0 + 000001 -> '0000001'
            A<<1 : 0 + 001001 -> '0001001'
            M<<1 : 1 + 001001 -> '1001001'
            D>>1 : 0 + 000011 -> '0000011'
            A>>1 : 0 + 001011 -> '0001011'
            M>>1 : 1 + 001011 -> '1001011'
    """

    _DEST: dict[str, str] = {
        '':    '000',
        'M':   '001',
        'D':   '010',
        'MD':  '011',
        'DM':  '011',
        'A':   '100',
        'AM':  '101',
        'MA':  '101',
        'AD':  '110',
        'DA':  '110',
        'AMD': '111',
        'ADM': '111',
        'MAD': '111',
        'MDA': '111',
        'DAM': '111',
        'DMA': '111',
    }

    _JUMP: dict[str, str] = {
        '':    '000',
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111',
    }

    _COMP: dict[str, str] = {
        # a=0
        '0':   '0101010',
        '1':   '0111111',
        '-1':  '0111010',
        'D':   '0001100',
        'A':   '0110000',
        '!D':  '0001101',
        '!A':  '0110001',
        '-D':  '0001111',
        '-A':  '0110011',
        'D+1': '0011111',
        'A+1': '0110111',
        'D-1': '0001110',
        'A-1': '0110010',
        'D+A': '0000010',
        'D-A': '0010011',
        'A-D': '0000111',
        'D&A': '0000000',
        'D|A': '0010101',
        # a=1
        'M':   '1110000',
        '!M':  '1110001',
        '-M':  '1110011',
        'M+1': '1110111',
        'M-1': '1110010',
        'D+M': '1000010',
        'D-M': '1010011',
        'M-D': '1000111',
        'D&M': '1000000',
        'D|M': '1010101',
        # Shift Extension
        'D<<1': '0000001',
        'A<<1': '0001001',
        'M<<1': '1001001',
        'D>>1': '0000011',
        'A>>1': '0001011',
        'M>>1': '1001011',
    }

    def dest(self, mnemonic: str) -> str:
        key = mnemonic.strip()
        if key not in self._DEST:
            raise ValueError(f"Unknown dest mnemonic: '{mnemonic}'")
        return self._DEST[key]

    def jump(self, mnemonic: str) -> str:
        key = mnemonic.strip().upper()
        if key not in self._JUMP:
            raise ValueError(f"Unknown jump mnemonic: '{mnemonic}'")
        return self._JUMP[key]

    def comp(self, mnemonic: str) -> str:
        key = mnemonic.strip().replace(' ', '')
        if key not in self._COMP:
            raise ValueError(f"Unknown comp mnemonic: '{mnemonic}'")
        return self._COMP[key]
