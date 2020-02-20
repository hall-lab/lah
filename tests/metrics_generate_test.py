import os, shutil, tempfile, unittest
from click.testing import CliRunner

from lah.cli import cli
from lah.metrics_cli import *
from lah.metrics_generate import metrics_generate_cmd
from lah.models import Metric

class MetricsTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "sample")
        self.temp_d = tempfile.TemporaryDirectory()
        self.dbfile = os.path.join(self.temp_d.name, "test.db")
        shutil.copy(os.path.join(self.data_dn, "test.db"), self.dbfile)

    def tearDown(self):
        self.temp_d.cleanup()

    def verify_haplotig_metrics(self, session):
         metrics = session.query(Metric).filter_by(grp="haplotig").all()
         self.assertEqual(len(metrics), 8)

    def verify_seqfile_metrics(self, session):
         metrics = session.query(Metric).filter_by(grp="seqfile").all()
         self.assertEqual(len(metrics), 14)

    def verify_asm_metrics(self, session):
         metrics = session.query(Metric).filter_by(grp="asm").all()
         self.assertEqual(len(metrics), 13)
         expected_metrtics = {
             "bases": "60",
             "cnt": "4",
             "mean": "15",
             "max": "24",
             "n50 ctg": "20",
             "n50 cnt": "2",
             "1000000": "0",
             "250000": "0",
             "100000": "0",
             "10000": "0",
             "5000": "0",
             "2000": "0",
             "0": "4",
         }
         self.assertDictEqual(dict(map(lambda m: (m.name, m.value), metrics)), expected_metrtics)

    def test_metrics_generate_cmd(self):
         runner = CliRunner()

         result = runner.invoke(metrics_generate_cmd, ["--help"])
         self.assertEqual(result.exit_code, 0)

         result = runner.invoke(cli, ["-d", self.dbfile, "metrics", "generate"])
         try:
             self.assertEqual(result.exit_code, 0)
         except:
             print(result.output)
             raise

         self.assertEqual(result.output, "Metrics generation complete! Use other metrics commands to view.\n")

         db = LahDb(dbfile=self.dbfile)
         db.connect()
         session = db.session()
         self.verify_haplotig_metrics(session)
         self.verify_seqfile_metrics(session)
         self.verify_asm_metrics(session)
         session.close()

# -- MetricsTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
