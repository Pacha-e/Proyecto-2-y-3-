# Hack Assembler — User Guide

## Requirements

- Python 3.10 or later (uses `str | None` union syntax).
- No external dependencies.

## Directory Layout

```
HackAssembler/
├── src/
│   ├── HackAssembler.py      ← main entry point
│   ├── Parser.py
│   ├── SymbolTable.py
│   ├── Code.py
│   └── HackDisassembler.py
├── test/
│   └── HackAssemblerTest.py
├── docs/
│   ├── API.md
│   ├── DESIGN.md
│   └── USER_GUIDE.md
└── README.md
```

## Assembling a File

```bash
cd src
python HackAssembler.py ../path/to/Prog.asm
```

Output: `Prog.hack` in the same directory as `Prog.asm`.

## Disassembling a File

```bash
cd src
python HackAssembler.py -d ../path/to/Prog.hack
```

Output: `ProgDis.asm` in the same directory as `Prog.hack`.

## Running the Disassembler Directly

```bash
cd src
python HackDisassembler.py ../path/to/Prog.hack
```

## Running Tests

```bash
cd test
python -m unittest HackAssemblerTest -v
```

## Supported Assembly Syntax

### A-Instructions

```
@21          // integer literal
@LOOP        // symbolic label
@myVar       // variable (auto-allocated from RAM 16)
```

### C-Instructions

```
dest=comp
dest=comp;jump
comp;jump
```

**Shift extension** (university addition):

```
D=D<<1       // shift D left by 1
D=D>>1       // shift D right by 1
D=A<<1
D=M<<1
D=M>>1
```

### Label Declarations

```
(LOOP)       // defines ROM address for label LOOP
```

### Comments

```
@42 // this is a comment — everything after // is ignored
```

## Examples

### Add.asm

```asm
@2
D=A
@3
D=D+A
@0
M=D
```

### ShiftTest.asm

```asm
@R0
D=M
D=D<<1      // double R0
@R1
M=D
(END)
@END
0;JMP
```
