import click, os, unittest
from click.testing import CliRunner

from lah.cli import cli as lah_cli

@click.command()
def the_test_cmd():
    print("Hello World!")
lah_cli.add_command(the_test_cmd, "test")

class CliTest(unittest.TestCase):
    def test_lah(self):
        runner = CliRunner()

        result = runner.invoke(lah_cli, [])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(lah_cli, ["-h"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(lah_cli, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(lah_cli, ["test"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, "Hello World!\n")

        dbfile = os.path.join(os.path.dirname(__file__), "data", "sample", "test.db")
        result = runner.invoke(lah_cli, ["test"])
        #result = runner.invoke(lah_cli, ["-d", dbfile, "test"])
        self.assertEqual(result.exit_code, 0)

# -- CliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
