# Hack Assembler & Disassembler

Two-pass Hack assembler and disassembler for the Nand2Tetris course, extended with shift instructions (`<<1`, `>>1`).

## Requirements

Python 3.10+. No external packages.

## Usage

```bash
# Assemble  (.asm → .hack)
python src/HackAssembler.py path/to/Prog.asm

# Disassemble  (.hack → Dis.asm)
python src/HackAssembler.py -d path/to/Prog.hack
```

## Run Tests

```bash
python -m unittest test/HackAssemblerTest.py -v
```

## File Structure

```
src/HackAssembler.py     — entry point (assemble / disassemble)
src/Parser.py            — tokenises .asm lines
src/SymbolTable.py       — symbol → address table with predefined symbols
src/Code.py              — mnemonic → binary translation
src/HackDisassembler.py  — binary → assembly translation
test/HackAssemblerTest.py
docs/API.md  DESIGN.md  USER_GUIDE.md
```

## Shift Instruction Encoding

| Assembly | Binary comp field (7 bits) |
|---|---|
| `D<<1` / `A<<1` | `0000001` |
| `M<<1`          | `1000001` |
| `D>>1` / `A>>1` | `0000011` |
| `M>>1`          | `1000011` |

See `docs/DESIGN.md` for the full C-instruction bit layout.
