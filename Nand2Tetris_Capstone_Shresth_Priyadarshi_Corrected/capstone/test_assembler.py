import unittest
from assembler import assemble

class AssemblerTests(unittest.TestCase):
    def test_a_and_c_instructions(self):
        out, errors, warnings = assemble(["@2", "D=A", "@3", "D=D+A"])
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual(len(out), 4)
        self.assertTrue(all(len(line) == 16 and set(line) <= {"0", "1"} for line in out))

    def test_variables_start_at_16(self):
        out, errors, _ = assemble(["@counter", "M=1", "@counter", "D=M"])
        self.assertEqual(errors, [])
        self.assertEqual(out[0], format(16, "016b"))
        self.assertEqual(out[2], format(16, "016b"))

    def test_duplicate_label_warning(self):
        _, errors, warnings = assemble(["(LOOP)", "@LOOP", "(LOOP)", "0;JMP"])
        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), 1)
        self.assertIn("duplicate label", warnings[0][1])

    def test_invalid_instruction_reports_line(self):
        _, errors, _ = assemble(["@0", "D=X+1"])
        self.assertEqual(errors[0][0], 2)

if __name__ == "__main__":
    unittest.main()
