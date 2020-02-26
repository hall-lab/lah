import os, shutil, tempfile, unittest
from click.testing import CliRunner

from lah.db import LahDb
from lah.cli import cli
from lah.unbinned_cli import unbinned_cli, unbinned_list_cmd, unbinned_seqfile_cmd

class Dataset():
    def __init__(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "dataset")
        self.temp_d = tempfile.TemporaryDirectory()
        self.dn = self.temp_d.name
        self.dbfile = os.path.join(self.dn, "test.db")

        shutil.copy(os.path.join(self.data_dn, "haplotigs.tsv"), self.dn)

        runner = CliRunner()
        result = runner.invoke(cli, ["db", "create", self.dbfile])
        if result.exit_code != 0:
            print(result.output)
            raise Exception("Failed to create DB!")

        result = runner.invoke(cli, ["-d", self.dbfile, "db", "ingest", "-f", os.path.join(self.dn, "haplotigs.tsv"), "-g", "NA,rid,hid"])
        if result.exit_code != 0:
            print(result.output)
            raise Exception("Failed to ingest haplotigs!")

        self.seqfiles = []
        for i in range(1, 3):
            fn = os.path.join(self.data_dn, "seqfiles", ".".join(["reads", str(i), "fastq"]))
            self.seqfiles.append(fn)
            shutil.copy(fn, self.dn)
            fn += ".fai"
            shutil.copy(fn, self.dn)

        result = runner.invoke(cli, ["-d", self.dbfile, "seqfiles", "add"] + self.seqfiles)
        if result.exit_code != 0:
            print(result.output)
            raise Exception("Failed to add seqfiles!")

    #-- init

    def __del__(self):
        self.temp_d.cleanup()

    #-- del

#-- TestDataset
