import os, unittest
from click.testing import CliRunner

from lah.db import LahDb
from lah.cli_unbinned import unbinned_cli, unbinned_list_cmd
import lah.unbinned

class UnbinnedTest(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "sample")
        self.dbfile = os.path.join(self.data_d, "test.db")
        self.expected_names = set(["m54238_00000_0000000/000000001/dummy", "m54238_00000_0000000/000000002/dummy"])

    def test0_unbinned_cli(self):
         runner = CliRunner()

         result = runner.invoke(unbinned_cli, [])
         self.assertEqual(result.exit_code, 0)

         result = runner.invoke(unbinned_cli, ["--help"])
         self.assertEqual(result.exit_code, 0)

    def verify_unbinned_read_names(self, names):
        self.assertEqual(names, self.expected_names)

    def test1_unbinned_read_names(self):
        LahDb.connect(self.dbfile)
        read_names = lah.unbinned.read_names()
        self.verify_unbinned_read_names(read_names)

    def test1_unbinned_list_cmd(self):
        runner = CliRunner()

        result = runner.invoke(unbinned_list_cmd, [])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(unbinned_list_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(unbinned_list_cmd, ["-d", self.dbfile])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise

        names = set(result.output.split("\n"))
        names.remove("")
        self.verify_unbinned_read_names(names)

# -- UnbinnedTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
