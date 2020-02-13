import unittest
from click.testing import CliRunner

from lah.asm_metrics import asm_metrics_cmd

class AsmMetricsTest(unittest.TestCase):
    #FIXME ACTUALLY TEST!
    def test0_asm_metrics_cmd(self):
         runner = CliRunner()

         result = runner.invoke(asm_metrics_cmd, [])
         self.assertEqual(result.exit_code, 1)

         result = runner.invoke(asm_metrics_cmd, ["--help"])
         self.assertEqual(result.exit_code, 0)

# -- AsmMetricsTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
