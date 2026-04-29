#*********
# HackAssemblerTest.py – Unit tests for the Hack Assembler / Disassembler
# Autor: Emmanuel
#*********

import sys
import os
import tempfile
import unittest

# Make src/ importable regardless of cwd
_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC  = os.path.join(_HERE, '..', 'src')
sys.path.insert(0, _SRC)

from Code import Code
from SymbolTable import SymbolTable
from Parser import Parser
from HackDisassembler import _decode_instruction, disassemble


# ─────────────────────────────────────────────────────────────────────────────
# Helper: write a temp .asm file and assemble it, return list of binary strings
# ─────────────────────────────────────────────────────────────────────────────

def _assemble_source(asm_source: str) -> list[str]:
    """Write asm_source to a temp file, assemble it, return binary lines."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.asm',
                                    delete=False) as f:
        f.write(asm_source)
        asm_path = f.name
    try:
        from HackAssembler import assemble
        assemble(asm_path)
        hack_path = asm_path.replace('.asm', '.hack')
        with open(hack_path) as hf:
            lines = [l.strip() for l in hf if l.strip()]
        return lines
    finally:
        for p in (asm_path, asm_path.replace('.asm', '.hack')):
            try:
                os.remove(p)
            except FileNotFoundError:
                pass


# ─────────────────────────────────────────────────────────────────────────────
# Code module tests
# ─────────────────────────────────────────────────────────────────────────────

class TestCode(unittest.TestCase):

    def setUp(self):
        self.code = Code()

    def test_dest_empty(self):
        self.assertEqual(self.code.dest(''), '000')

    def test_dest_M(self):
        self.assertEqual(self.code.dest('M'), '001')

    def test_dest_D(self):
        self.assertEqual(self.code.dest('D'), '010')

    def test_dest_AMD(self):
        self.assertEqual(self.code.dest('AMD'), '111')

    def test_dest_A(self):
        self.assertEqual(self.code.dest('A'), '100')

    def test_jump_empty(self):
        self.assertEqual(self.code.jump(''), '000')

    def test_jump_JMP(self):
        self.assertEqual(self.code.jump('JMP'), '111')

    def test_jump_JEQ(self):
        self.assertEqual(self.code.jump('JEQ'), '010')

    def test_jump_JLT(self):
        self.assertEqual(self.code.jump('JLT'), '100')

    def test_comp_zero(self):
        self.assertEqual(self.code.comp('0'), '0101010')

    def test_comp_one(self):
        self.assertEqual(self.code.comp('1'), '0111111')

    def test_comp_D(self):
        self.assertEqual(self.code.comp('D'), '0001100')

    def test_comp_A(self):
        self.assertEqual(self.code.comp('A'), '0110000')

    def test_comp_M(self):
        self.assertEqual(self.code.comp('M'), '1110000')

    def test_comp_DplusA(self):
        self.assertEqual(self.code.comp('D+A'), '0000010')

    def test_comp_DplusM(self):
        self.assertEqual(self.code.comp('D+M'), '1000010')

    def test_comp_Dplus1(self):
        self.assertEqual(self.code.comp('D+1'), '0011111')

    # Shift extension
    def test_comp_shift_left_D(self):
        self.assertEqual(self.code.comp('D<<1'), '0000001')

    def test_comp_shift_left_M(self):
        self.assertEqual(self.code.comp('M<<1'), '1001001')

    def test_comp_shift_right_D(self):
        self.assertEqual(self.code.comp('D>>1'), '0000011')

    def test_comp_shift_right_M(self):
        self.assertEqual(self.code.comp('M>>1'), '1001011')

    def test_comp_shift_left_A(self):
        self.assertEqual(self.code.comp('A<<1'), '0001001')

    def test_comp_shift_right_A(self):
        self.assertEqual(self.code.comp('A>>1'), '0001011')


# ─────────────────────────────────────────────────────────────────────────────
# SymbolTable tests
# ─────────────────────────────────────────────────────────────────────────────

class TestSymbolTable(unittest.TestCase):

    def setUp(self):
        self.st = SymbolTable()

    def test_predefined_SP(self):
        self.assertEqual(self.st.getAddress('SP'), 0)

    def test_predefined_SCREEN(self):
        self.assertEqual(self.st.getAddress('SCREEN'), 16384)

    def test_add_and_retrieve(self):
        self.st.addEntry('LAB', 100)
        self.assertEqual(self.st.getAddress('LAB'), 100)


# ─────────────────────────────────────────────────────────────────────────────
# Full encoding tests
# ─────────────────────────────────────────────────────────────────────────────

class TestEncoding(unittest.TestCase):

    def setUp(self):
        self.code = Code()

    def _c(self, comp_str, dest_str='', jump_str=''):
        c = self.code.comp(comp_str)
        d = self.code.dest(dest_str)
        j = self.code.jump(jump_str)
        return '111' + c + d + j

    def test_a_instruction_21(self):
        self.assertEqual(format(21, '016b'), '0000000000010101')

    def test_c_D_equals_Dplus1(self):
        self.assertEqual(self._c('D+1', 'D'), '1110011111010000')

    def test_c_shift_left_D(self):
        self.assertEqual(self._c('D<<1', 'D'), '1110000001010000')

    def test_c_shift_left_A(self):
        self.assertEqual(self._c('A<<1', 'D'), '1110001001010000')

    def test_c_shift_left_M(self):
        self.assertEqual(self._c('M<<1', 'D'), '1111001001010000')

    def test_c_shift_right_D(self):
        self.assertEqual(self._c('D>>1', 'D'), '1110000011010000')

    def test_c_shift_right_A(self):
        self.assertEqual(self._c('A>>1', 'D'), '1110001011010000')

    def test_c_shift_right_M(self):
        self.assertEqual(self._c('M>>1', 'D'), '1111001011010000')


# ─────────────────────────────────────────────────────────────────────────────
# Parser tests
# ─────────────────────────────────────────────────────────────────────────────

class TestParser(unittest.TestCase):

    def _make_parser(self, source: str) -> Parser:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.asm',
                                        delete=False) as f:
            f.write(source)
            self._tmp = f.name
        return Parser(self._tmp)

    def tearDown(self):
        try:
            os.remove(self._tmp)
        except: pass

    def test_c_dest_comp_jump(self):
        p = self._make_parser('D=D+1;JGT\n')
        p.advance()
        self.assertEqual(p.dest(), 'D')
        self.assertEqual(p.comp(), 'D+1')
        self.assertEqual(p.jump(), 'JGT')

    def test_shift_left_parsed(self):
        p = self._make_parser('D=D<<1\n')
        p.advance()
        self.assertEqual(p.comp(), 'D<<1')


# ─────────────────────────────────────────────────────────────────────────────
# Assembler integration tests
# ─────────────────────────────────────────────────────────────────────────────

class TestAssemblerIntegration(unittest.TestCase):

    def test_a_instruction_literal(self):
        lines = _assemble_source('@21\n')
        self.assertEqual(lines[0], '0000000000010101')

    def test_c_shift_left_D(self):
        lines = _assemble_source('D=D<<1\n')
        self.assertEqual(lines[0], '1110000001010000')

    def test_c_shift_left_A(self):
        lines = _assemble_source('D=A<<1\n')
        self.assertEqual(lines[0], '1110001001010000')

    def test_c_shift_left_M(self):
        lines = _assemble_source('D=M<<1\n')
        self.assertEqual(lines[0], '1111001001010000')

    def test_add_asm(self):
        """Standard Add.asm: R0 = 2 + 3."""
        src = '@2\nD=A\n@3\nD=D+A\n@0\nM=D\n'
        expected = [
            '0000000000000010',
            '1110110000010000',
            '0000000000000011',
            '1110000010010000',
            '0000000000000000',
            '1110001100001000',
        ]
        self.assertEqual(_assemble_source(src), expected)

    def test_labels_and_jump(self):
        """Label forward reference + unconditional jump."""
        src = '(LOOP)\n@LOOP\n0;JMP\n'
        expected = [
            '0000000000000000',
            '1110101010000111',
        ]
        self.assertEqual(_assemble_source(src), expected)

    def test_variable_allocation(self):
        """User-defined variable gets RAM address starting at 16."""
        src = '@myVar\nM=D\n@myVar\nD=M\n'
        lines = _assemble_source(src)
        # @myVar → RAM[16] → 0000000000010000
        self.assertEqual(lines[0], '0000000000010000')
        # second reference to same variable → same address
        self.assertEqual(lines[2], '0000000000010000')

    def test_max_asm(self):
        """Max.asm: R2 = max(R0, R1). Tests labels, D-A arithmetic, branching."""
        src = (
            '@R0\nD=M\n@R1\nD=D-M\n@OUTPUT_FIRST\nD;JGT\n'
            '@R1\nD=M\n@OUTPUT_D\n0;JMP\n'
            '(OUTPUT_FIRST)\n@R0\nD=M\n'
            '(OUTPUT_D)\n@R2\nM=D\n'
            '(INFINITE_LOOP)\n@INFINITE_LOOP\n0;JMP\n'
        )
        expected = [
            '0000000000000000', '1111110000010000',
            '0000000000000001', '1111010011010000',
            '0000000000001010', '1110001100000001',
            '0000000000000001', '1111110000010000',
            '0000000000001100', '1110101010000111',
            '0000000000000000', '1111110000010000',
            '0000000000000010', '1110001100001000',
            '0000000000001110', '1110101010000111',
        ]
        self.assertEqual(_assemble_source(src), expected)


# ─────────────────────────────────────────────────────────────────────────────
# Disassembler tests
# ─────────────────────────────────────────────────────────────────────────────

class TestDisassembler(unittest.TestCase):

    def test_a_instruction_21(self):
        self.assertEqual(_decode_instruction('0000000000010101'), '@21')

    def test_c_shift_left_D(self):
        self.assertEqual(_decode_instruction('1110000001010000'), 'D=D<<1')

    def test_c_shift_left_A(self):
        self.assertEqual(_decode_instruction('1110001001010000'), 'D=A<<1')

    def test_c_shift_left_M(self):
        self.assertEqual(_decode_instruction('1111001001010000'), 'D=M<<1')

    def test_round_trip_shift_left_A(self):
        code = Code()
        bits = '111' + code.comp('A<<1') + code.dest('D') + code.jump('')
        self.assertEqual(_decode_instruction(bits), 'D=A<<1')

    def test_c_shift_right_D(self):
        self.assertEqual(_decode_instruction('1110000011010000'), 'D=D>>1')

    def test_c_shift_right_A(self):
        self.assertEqual(_decode_instruction('1110001011010000'), 'D=A>>1')

    def test_c_shift_right_M(self):
        self.assertEqual(_decode_instruction('1111001011010000'), 'D=M>>1')

    def test_round_trip_shift_right_D(self):
        code = Code()
        bits = '111' + code.comp('D>>1') + code.dest('D') + code.jump('')
        self.assertEqual(_decode_instruction(bits), 'D=D>>1')

    def test_round_trip_shift_right_M(self):
        code = Code()
        bits = '111' + code.comp('M>>1') + code.dest('D') + code.jump('')
        self.assertEqual(_decode_instruction(bits), 'D=M>>1')


if __name__ == '__main__':
    unittest.main(verbosity=2)
