import os, shutil, tempfile, unittest
from click.testing import CliRunner

from lah.db import LahDb
from lah.models import Metric
from lah.cli import cli
from lah.metrics_cli import metrics_cli, metrics_ctglens_cmd

class MetricsCliTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "sample")
        self.temp_d = tempfile.TemporaryDirectory()
        self.dbfile = os.path.join(self.temp_d.name, "test.db")
        shutil.copy(os.path.join(self.data_dn, "test.db"), self.dbfile)

    def test0_metrics_cli(self):
        runner = CliRunner()

        result = runner.invoke(metrics_cli, [])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(metrics_cli, ["--help"])
        self.assertEqual(result.exit_code, 0)

    def test9_metrics_ctglens_cmd(self):
        runner = CliRunner()

        result = runner.invoke(metrics_ctglens_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(metrics_ctglens_cmd, [])
        self.assertEqual(result.exit_code, 1)

        db = LahDb(dbfile=self.dbfile)
        db.connect()
        session = db.session()
        for name in ["401_0_1_0", "401_0_2_0", "402_0_1_0", "402_0_2_0"]:
            session.add(Metric(grp=name, name="contig lengths", value=12))
        session.commit()

        result = runner.invoke(cli, ["-d", self.dbfile, "metrics", "ctg-lengths"])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print("\n"+result.output)
            raise

        expected_output = """      NAME |   RDS |   COUNT |   TOTAL |   MAX
-----------+-------+---------+---------+-------
 401_0_1_0 |     1 |      12 |      12 |    12
 401_0_2_0 |     1 |      12 |      12 |    12
 402_0_1_0 |     1 |      12 |      12 |    12
 402_0_2_0 |     1 |      12 |      12 |    12\n"""
        self.assertEqual(result.output, expected_output)

# -- MetricsCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
