#*********
# HackAssembler.py – Main assembler/disassembler entry point
# Autor: Emmanuel
#*********

import sys
import os

def assemble(input_path: str) -> None:
    from Parser import Parser
    from SymbolTable import SymbolTable
    from Code import Code

    symbol_table = SymbolTable()
    code = Code()

    parser = Parser(input_path)
    rom_address = 0
    while parser.hasMoreLines():
        parser.advance()
        itype = parser.instructionType()
        if itype == 'L':
            symbol_table.addEntry(parser.symbol(), rom_address)
        elif itype in ('A', 'C'):
            rom_address += 1

    parser = Parser(input_path)
    var_address = 16
    output_lines = []

    while parser.hasMoreLines():
        parser.advance()
        itype = parser.instructionType()
        if itype == 'A':
            sym = parser.symbol()
            if sym.lstrip('-').isdigit():
                value = int(sym)
            elif symbol_table.contains(sym):
                value = symbol_table.getAddress(sym)
            else:
                symbol_table.addEntry(sym, var_address)
                value = var_address
                var_address += 1
            output_lines.append(format(value, '016b'))
        elif itype == 'C':
            d = code.dest(parser.dest())
            c = code.comp(parser.comp())
            j = code.jump(parser.jump())
            output_lines.append('111' + c + d + j)

    base = os.path.splitext(input_path)[0]
    output_path = base + '.hack'
    with open(output_path, 'w') as f:
        f.write('\n'.join(output_lines) + '\n')
    print(f"Assembled → {output_path}")

def disassemble(input_path: str) -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, here)
    from HackDisassembler import disassemble as _dis
    _dis(input_path)

def main() -> None:
    args = sys.argv[1:]
    if not args:
        print("Usage:")
        print("  python HackAssembler.py Prog.asm")
        print("  python HackAssembler.py -d Prog.hack")
        sys.exit(1)
    if args[0] == '-d':
        if len(args) < 2:
            sys.exit(1)
        disassemble(args[1])
    else:
        assemble(args[0])

if __name__ == '__main__':
    main()
