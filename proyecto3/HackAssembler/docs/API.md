# Hack Assembler — API Reference

## Module: `Parser`

| Method | Signature | Description |
|---|---|---|
| `__init__` | `(path: str)` | Open and pre-process the .asm file (strip comments/blanks). |
| `hasMoreLines` | `() → bool` | True if there are more instructions to process. |
| `advance` | `() → None` | Move to the next instruction. Call only when `hasMoreLines()`. |
| `instructionType` | `() → 'A' \| 'C' \| 'L' \| None` | Classify the current instruction. |
| `symbol` | `() → str` | A-instruction: value after `@`. L-instruction: label inside `()`. |
| `dest` | `() → str` | C-instruction: destination mnemonic (before `=`), or `''`. |
| `comp` | `() → str` | C-instruction: computation mnemonic (may include `<<1`/`>>1`). |
| `jump` | `() → str` | C-instruction: jump mnemonic (after `;`), or `''`. |

---

## Module: `SymbolTable`

| Method | Signature | Description |
|---|---|---|
| `__init__` | `()` | Pre-load all Hack predefined symbols. |
| `addEntry` | `(symbol: str, address: int) → None` | Insert or overwrite a symbol. |
| `contains` | `(symbol: str) → bool` | Check existence. |
| `getAddress` | `(symbol: str) → int` | Return the numeric address. |

### Pre-defined Symbols

| Symbol | Address |
|---|---|
| SP | 0 |
| LCL | 1 |
| ARG | 2 |
| THIS | 3 |
| THAT | 4 |
| R0–R15 | 0–15 |
| SCREEN | 16384 |
| KBD | 24576 |

---

## Module: `Code`

| Method | Signature | Description |
|---|---|---|
| `dest` | `(mnemonic: str) → str` | 3-bit destination field. |
| `jump` | `(mnemonic: str) → str` | 3-bit jump field. |
| `comp` | `(mnemonic: str) → str` | 7-bit computation field (`a` + `cccccc`). |

### Shift Encoding (extension)

| Mnemonic | 7-bit field | Notes |
|---|---|---|
| `D<<1` or `A<<1` | `0000001` | a=0, shift-left |
| `M<<1` | `1000001` | a=1, shift-left |
| `D>>1` or `A>>1` | `0000011` | a=0, shift-right |
| `M>>1` | `1000011` | a=1, shift-right |

---

## Module: `HackDisassembler`

| Function | Signature | Description |
|---|---|---|
| `disassemble` | `(input_path: str) → None` | Read `.hack`, write `<base>Dis.asm`. |
| `_decode_instruction` | `(bits: str) → str` | Decode one 16-bit string to assembly. |

---

## Module: `HackAssembler` (entry point)

| Function | Signature | Description |
|---|---|---|
| `assemble` | `(input_path: str) → None` | Two-pass assembly: `.asm` → `.hack`. |
| `disassemble` | `(input_path: str) → None` | Delegate to `HackDisassembler.disassemble`. |
| `main` | `() → None` | CLI entry point. |
