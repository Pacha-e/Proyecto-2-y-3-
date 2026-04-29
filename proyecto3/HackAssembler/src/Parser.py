#*********
# Parser.py – Reads and parses a Hack .asm file
# Autor: Emmanuel
#*********

import re


class Parser:
    """
    Encapsulates access to the input .asm source code.
    """

    def __init__(self, path: str) -> None:
        with open(path, 'r') as f:
            raw = f.readlines()
        self._lines: list[str] = []
        for line in raw:
            stripped = re.sub(r'//.*', '', line).strip()
            if stripped:
                self._lines.append(stripped)
        self._index: int = -1
        self._current: str = ''

    def hasMoreLines(self) -> bool:
        return self._index < len(self._lines) - 1

    def advance(self) -> None:
        self._index += 1
        self._current = self._lines[self._index]

    def instructionType(self) -> str | None:
        line = self._current
        if line.startswith('@'):
            return 'A'
        if line.startswith('(') and line.endswith(')'):
            return 'L'
        if '=' in line or ';' in line or '<<' in line or '>>' in line:
            return 'C'
        return None

    def symbol(self) -> str:
        line = self._current
        if line.startswith('@'):
            return line[1:]
        return line[1:-1]

    def dest(self) -> str:
        line = self._current
        if '=' in line:
            return line.split('=')[0].strip()
        return ''

    def comp(self) -> str:
        line = self._current
        if '=' in line:
            line = line.split('=', 1)[1]
        if ';' in line:
            line = line.split(';', 1)[0]
        return line.strip()

    def jump(self) -> str:
        line = self._current
        if ';' in line:
            return line.split(';', 1)[1].strip()
        return ''
