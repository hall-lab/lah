import os, shutil, tempfile, unittest
from click.testing import CliRunner

from lah.db import LahDb
from lah.models import Metric, Seqfile
from lah.cli import cli
from lah.metrics_cli import metrics_cli, metrics_asm_cmd, metrics_haplotigs_cmd, metrics_seqfiles_cmd

class MetricsCliTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "sample")
        self.temp_d = tempfile.TemporaryDirectory()
        self.dbfile = os.path.join(self.temp_d.name, "test.db")
        shutil.copy(os.path.join(self.data_dn, "test.db"), self.dbfile)

    def tearDown(self):
        self.temp_d.cleanup()

    def test0_metrics_cli(self):
        runner = CliRunner()

        result = runner.invoke(metrics_cli, [])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(metrics_cli, ["--help"])
        self.assertEqual(result.exit_code, 0)

    def test1_metrics_asm_cmd(self):
        runner = CliRunner()

        result = runner.invoke(metrics_asm_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(metrics_asm_cmd, [])
        self.assertEqual(result.exit_code, 1)

        db = LahDb(dbfile=self.dbfile)
        db.connect()
        session = db.session()
        session.add(Metric(grp="asm", grp_id="1", name="bases", value="96"))
        session.add(Metric(grp="asm", grp_id="1", name="cnt", value="4"))
        session.commit()

        result = runner.invoke(cli, ["-d", self.dbfile, "metrics", "asm"])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print("\n"+result.output)
            raise

        expected_output = """NAME      VALUE
------  -------
bases        96
cnt           4\n"""
        self.assertEqual(result.output, expected_output)

    def test1_metrics_seqfiles_cmd(self):
        runner = CliRunner()

        result = runner.invoke(metrics_seqfiles_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(metrics_seqfiles_cmd, [])
        self.assertEqual(result.exit_code, 1)

        db = LahDb(dbfile=self.dbfile)
        db.connect()
        session = db.session()
        for seqfile in session.query(Seqfile):
            session.add(Metric(grp="seqfile", grp_id=seqfile.id, name="bases", value="36"))
            session.add(Metric(grp="seqfile", grp_id=seqfile.id, name="length median", value="7.2"))
        session.commit()

        result = runner.invoke(cli, ["-d", self.dbfile, "metrics", "seqfiles"])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print("\n"+result.output)
            raise

        expected_output = """ SEQFILE                                  | METRIC        |   VALUE
------------------------------------------+---------------+---------
 tests/data/sample/seqfiles/reads.1.fastq | bases         |    36
 tests/data/sample/seqfiles/reads.1.fastq | length median |     7.2
 tests/data/sample/seqfiles/reads.2.fastq | bases         |    36
 tests/data/sample/seqfiles/reads.2.fastq | length median |     7.2\n"""
        self.assertEqual(result.output, expected_output)

    def test1_metrics_haplotigs_cmd(self):
        runner = CliRunner()

        result = runner.invoke(metrics_haplotigs_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(metrics_haplotigs_cmd, [])
        self.assertEqual(result.exit_code, 1)

        db = LahDb(dbfile=self.dbfile)
        db.connect()
        session = db.session()
        for name in ["401_0_1_0", "401_0_2_0", "402_0_1_0", "402_0_2_0"]:
            session.add(Metric(grp="haplotig", grp_id=name, name="contig lengths", value=12))
        session.commit()

        result = runner.invoke(cli, ["-d", self.dbfile, "metrics", "haplotigs"])
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
