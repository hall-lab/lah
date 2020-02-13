import os, tempfile, unittest
from click.testing import CliRunner

from lah.cli import cli
from lah.haplotig_cli import hap_cli, hap_list_cmd, hap_reads_cmd

class HaplotigCliTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "sample")
        self.dbfile = os.path.join(self.data_dn, "test.db")

    def test1_hap_cli(self):
        runner = CliRunner()
        result = runner.invoke(hap_cli, [])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(hap_cli, ["--help"])
        self.assertEqual(result.exit_code, 0)

    def test2_hap_list_cmd(self):
        runner = CliRunner()
        result = runner.invoke(hap_list_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["-d", self.dbfile, "haplotig", "list"])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = """  ID       NAME    READS
----  ---------  -------
   1  401_0_1_0        1
   2  401_0_2_0        2
   3  402_0_1_0        8
   4  402_0_2_0       14
"""
        self.assertEqual(result.output, expected_output)

    def test3_hap_reads_cmd(self):
        runner = CliRunner()
        result = runner.invoke(hap_reads_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["-d", self.dbfile, "haplotig", "reads", "402_0_1_0", "402_0_2_0"])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output ="""m54238_180909_174539/15467504/ccs
m54238_180909_174539/24445361/ccs
m54238_180910_180559/31916502/ccs
m54238_180914_183539/60817532/ccs
m54238_180916_191625/17694942/ccs
m54328_180924_001027/12976682/ccs
m54335_180925_223313/49349181/ccs
m54335_180926_225328/38011681/ccs
m54238_180902_013549/25756023/ccs
m54238_180910_180559/15270367/ccs
m54238_180913_181445/44892801/ccs
m54238_180916_191625/13369878/ccs
m54238_180916_191625/25822169/ccs
m54238_180916_191625/50135710/ccs
m54238_180919_165326/21496035/ccs
m54238_180919_165326/22217117/ccs
m54238_180921_173448/55574839/ccs
m54328_180929_232524/12321004/ccs
m54329_180924_222717/23069205/ccs
m54329_180925_224838/23068774/ccs
m54329_180927_232921/11534776/ccs
m54334_180927_231334/41812362/ccs
"""
        self.assertEqual(result.output, expected_output)

# -- HaplotigCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
