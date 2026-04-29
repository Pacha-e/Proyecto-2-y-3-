# Changelog

Todos los cambios notables de este proyecto están documentados aquí.  
Formato: [Keep a Changelog](https://keepachangelog.com/es/1.0.0/)

---

## [1.2.0] — 2026-04-29

### Proyecto 3 — HackAssembler

#### Correcciones
- **`HackAssembler.py`**: reemplazado `sym.lstrip('-').isdigit()` por `sym.isdigit()` — el prefijo negativo no es válido en A-instructions de Hack y causaba `ValueError` en `format()`.
- **`README.md`**: corregida tabla de encodings shift — valores erróneos para `A<<1` (`0001001`), `M<<1` (`1001001`), `A>>1` (`0001011`), `M>>1` (`1001011`).
- **`docs/DESIGN.md`**: misma corrección de tabla + eliminada afirmación falsa de que `A<<1` y `D<<1` comparten el mismo patrón de bits (difieren en el bit `zy`/c3).

#### Tests
- Suite ampliada de 45 a 54 tests (todos pasando):
  - `test_add_asm`: ensamblado completo de Add.asm (R0 = 2 + 3)
  - `test_max_asm`: Max.asm con etiquetas y ramas condicionales
  - `test_labels_and_jump`: forward reference de etiqueta + salto incondicional
  - `test_variable_allocation`: variables de usuario asignadas desde RAM[16]
  - `test_c_shift_right_D/A/M`: desensambladoes de `>>1`
  - `test_round_trip_shift_right_D/M`: round-trip ensamblar → desensamblar para `>>1`

#### MD5 actualizados
- `HackAssembler.md5`, `HackAssemblerTest.md5`

---

## [1.1.0] — 2026-04-29

### Proyecto 2 — ALU y Shifter (HDL)

#### Correcciones
- **`ALU.hdl`**: revertido a versión con Shifter inlineado — el web IDE de Nand2Tetris no puede cargar chips externos definidos por el usuario. La lógica completa del Shifter se integra directamente en la ALU para compatibilidad total con el portal web.
- **`CPU.hdl`**: pin `result` de la ALU desconectado explícitamente (válido en HDL de Nand2Tetris).
- **`Shifter.hdl`**: limpieza de formato; lógica sin cambios. Verificable solo desde el simulador de escritorio.

#### MD5 actualizados
- `ALU.md5`, `CPU.md5`, `Shifter.md5`

---

## [1.0.0] — 2026-04-28

### Entrega inicial — Proyectos 2 y 3

#### Proyecto 2 — HDL (Nand2Tetris)

##### Añadido
- **`Shifter.hdl`**: chip de desplazamiento de 16 bits. `direction=0` → izquierda (`<<1`), `direction=1` → derecha (`>>1`). Output `result` = bit desplazado fuera. Verificado en simulador de escritorio.
- **`ALU.hdl`**: ALU estándar Hack extendida con modo shift inlineado. Trigger shift: `zx=0, nx=0, zy=0, ny=0, no=1`. Outputs: `out[16]`, `zr`, `ng`, `result`.
- **`Memory.hdl`**: memoria de datos (RAM16K + Screen + Keyboard).
- **`CPU.hdl`**: CPU Hack completa con soporte de instrucciones shift.
- **`Computer.hdl`**: computador Hack completo (CPU + Memory + ROM32K).
- **`design.txt`**: tabla de codificación C-instruction para instrucciones shift (`D<<1`, `A<<1`, `M<<1`, `D>>1`, `A>>1`, `M>>1`) con bits binarios completos.
- MD5 de todos los archivos HDL: `ALU.md5`, `CPU.md5`, `Computer.md5`, `Memory.md5`, `Shifter.md5`, `design.md5`.

#### Proyecto 3 — HackAssembler (Python)

##### Añadido
- **`HackAssembler.py`**: punto de entrada CLI. Ensambla `.asm → .hack` (dos pasadas) y desensambla `.hack → Dis.asm` con flag `-d`.
- **`Parser.py`**: tokenizador de líneas `.asm`. Soporta A-instructions, C-instructions, L-instructions (etiquetas) y extensión shift (`<<1`, `>>1`).
- **`SymbolTable.py`**: tabla de símbolos con símbolos predefinidos (SP, LCL, ARG, THIS, THAT, R0–R15, SCREEN, KBD).
- **`Code.py`**: traductor de mnemonics a binario. Incluye todas las instrucciones estándar Hack + extensiones de shift.
- **`HackDisassembler.py`**: desensamblador binario → assembly. Lookup inverso de las mismas tablas de `Code.py`.
- **`HackAssemblerTest.py`**: suite de 45 tests unitarios e integración (Code, SymbolTable, Parser, Encoding, Assembler, Disassembler).
- MD5 de todos los archivos fuente.
- Documentación: `README.md`, `docs/API.md`, `docs/DESIGN.md`, `docs/USER_GUIDE.md`.

#### Repositorio
- `README.md`: descripción general del proyecto.
- `CONTRIBUTORS.md`: integrantes.
- `LICENSE`: MIT.
- `.gitignore`: excluye `__pycache__/`, `*.pyc`, `.out`.
