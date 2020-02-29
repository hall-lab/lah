import os, tempfile, unittest
from click.testing import CliRunner

from lah.cli import cli
from lah.init_cli import init_cmd
from lah.models import Haplotig
import lah.unbinned

class InitCliTest(unittest.TestCase):
    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_d.cleanup()

    def test_init_cmd(self):
        runner = CliRunner()

        result = runner.invoke(init_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["init"])
        self.assertEqual(result.exit_code, 1)

        dbfile = os.path.join(self.temp_d.name, "test.db")
        result = runner.invoke(cli, ["-d", dbfile, "init", "-o"])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise

        self.assertTrue(os.path.exists(dbfile))
        self.assertTrue(os.path.getsize(dbfile), 61440)
        self.assertFalse(os.path.exists(os.path.join(self.temp_d.name, Haplotig.asm_files_sdn())))
        self.assertFalse(os.path.exists(os.path.join(self.temp_d.name, Haplotig.asm_sdn())))
        self.assertFalse(os.path.exists(os.path.join(self.temp_d.name, Haplotig.seqfile_sdn())))
        self.assertFalse(os.path.exists(os.path.join(self.temp_d.name, lah.unbinned.subd())))

        os.remove(dbfile)
        result = runner.invoke(cli, ["-d", dbfile, "init"])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise

        self.assertTrue(os.path.exists(dbfile))
        self.assertTrue(os.path.getsize(dbfile), 61440)
        self.assertTrue(os.path.exists(os.path.join(self.temp_d.name, Haplotig.asm_files_sdn())))
        self.assertTrue(os.path.exists(os.path.join(self.temp_d.name, Haplotig.asm_sdn())))
        self.assertTrue(os.path.exists(os.path.join(self.temp_d.name, Haplotig.seqfile_sdn())))
        self.assertTrue(os.path.exists(os.path.join(self.temp_d.name, lah.unbinned.subd())))

# -- InitCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
