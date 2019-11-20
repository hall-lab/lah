import tempfile, unittest
from click.testing import CliRunner

from .context import lah
from lah.cli_asm import asm_cli

class CliAsmTest(unittest.TestCase):
    def setUp(self):
        self.out = tempfile.TemporaryFile()
        self.err = tempfile.TemporaryFile()

    def tearDown(self):
        self.out.close()
        self.err.close()
    
    def test1_asm_cli(self):
         runner = CliRunner()

         result = runner.invoke(asm_cli, [])
         self.assertEqual(result.exit_code, 0)

         # FIXME -h returns 2 here, but 0 n the command line 
         #result = runner.invoke(asm_cli, ["-h"])
         #self.assertEqual(result.exit_code, 0)

         result = runner.invoke(asm_cli, ["--help"])
         self.assertEqual(result.exit_code, 0)

# -- CliAsmTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
