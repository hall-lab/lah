import filecmp, os, tempfile, unittest
from click.testing import CliRunner

from lah.db_cli import db_cli, db_create_cmd

class LahDbCliTest(unittest.TestCase):
    def setUp(self):
        self.data_d = data_d = os.path.join(os.path.dirname(__file__), "data", "db")
        self.temp_d = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_d.cleanup()

    def test1_lah_db(self):
        runner = CliRunner()
        result = runner.invoke(db_cli, [])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(db_cli, ["--help"])
        self.assertEqual(result.exit_code, 0)

    def test2_lah_db_create(self):
        runner = CliRunner()
        result = runner.invoke(db_create_cmd, [])
        self.assertEqual(result.exit_code, 2)
        result = runner.invoke(db_create_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        dbfile = os.path.join(self.temp_d.name, "test.db")
        result = runner.invoke(db_create_cmd, [dbfile])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        self.assertTrue(os.path.exists(dbfile))
        self.assertTrue(os.path.getsize(dbfile), 61440)

# -- LahDbCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
