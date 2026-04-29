# Hack Assembler — Design Document

## Architecture

```
HackAssembler.py  (CLI entry point)
├── Parser.py         — tokenises .asm source
├── SymbolTable.py    — symbol → address mapping
├── Code.py           — mnemonic → binary
└── HackDisassembler.py — binary → mnemonic
```

## Two-Pass Algorithm

### Pass 1 — Label Collection

Walk every instruction without emitting output.

- `(LABEL)` → insert `LABEL → current_ROM_address` into SymbolTable.
- A/C instructions → increment ROM address counter.

### Pass 2 — Code Generation

Walk every instruction, emit binary:

1. **A-instruction** (`@xxx`):
   - If `xxx` is a decimal integer → encode as 16-bit.
   - If symbol already in table → use stored address.
   - Otherwise → allocate next free RAM address (starting at 16).
2. **C-instruction** → `111` + `comp(7)` + `dest(3)` + `jump(3)`.
3. **L-instruction** → no output.

## C-Instruction Binary Layout

```
Bit position:  15 14 13 12 11 10  9  8  7  6  5  4  3  2  1  0
Field:          1  1  1  a  c1 c2 c3 c4 c5 c6 d1 d2 d3 j1 j2 j3
```

- Bits 15–13: always `111` for C-instructions.
- Bits 12–6 (7 bits): comp field = `a` + `cccccc`.
- Bits 5–3 (3 bits): dest field `ddd`.
- Bits 2–0 (3 bits): jump field `jjj`.

## Shift Extension

The university project adds two new instructions outside the standard Nand2Tetris ISA:

| Assembly | Meaning | comp bits | a | zy |
|---|---|---|---|---|
| `D=D<<1` | D ← D × 2 | `0000001` | 0 | 0 |
| `D=A<<1` | D ← A × 2 | `0001001` | 0 | 1 |
| `D=M<<1` | D ← M × 2 | `1001001` | 1 | 1 |
| `D=D>>1` | D ← D / 2 | `0000011` | 0 | 0 |
| `D=A>>1` | D ← A / 2 | `0001011` | 0 | 1 |
| `D=M>>1` | D ← M / 2 | `1001011` | 1 | 1 |

- The `a` bit (bit 12) distinguishes register (`a=0`) from memory (`a=1`) source.
- The `zy` bit (c3, bit 9) selects the ALU y-input: 0 → D register, 1 → A/M.
- All six shift variants have unique 7-bit comp patterns → full round-trip disassembly is possible without register tracking.

## Disassembler Design

Reverse lookup of the same tables used by `Code.py`.  
All shift instructions have distinct bit patterns and round-trip correctly.

## Error Handling

- Unknown mnemonic → `ValueError` with descriptive message.
- Invalid 16-bit line in `.hack` file → warning to `stderr`, line skipped.
- Missing file → propagated `FileNotFoundError` from Python builtins.
