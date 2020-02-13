import unittest
from click.testing import CliRunner

from lah.asm_cli import asm_cli

class AsmCliTest(unittest.TestCase):
    def test0_asm_cli(self):
         runner = CliRunner()

         result = runner.invoke(asm_cli, [])
         self.assertEqual(result.exit_code, 0)

         result = runner.invoke(asm_cli, ["--help"])
         self.assertEqual(result.exit_code, 0)

# -- AsmCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
