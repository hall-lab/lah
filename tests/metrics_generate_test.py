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

         db = LahDb(dbfile=self.dbfile)
         db.connect()
         session = db.session()
         metrics = session.query(Metric).filter_by(name="contig lengths").all()
         self.assertEqual(len(metrics), 4)

# -- MetricsTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__