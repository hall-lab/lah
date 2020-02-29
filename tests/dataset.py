import os, shutil, tempfile, unittest
from click.testing import CliRunner

from lah.db import LahDb
from lah.cli import cli
from lah.models import *
from lah.unbinned_cli import unbinned_cli, unbinned_list_cmd, unbinned_seqfile_cmd

class Dataset():
    def __init__(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "dataset")
        self.temp_d = tempfile.TemporaryDirectory()
        self.dn = self.temp_d.name
        self.dbfile = os.path.join(self.dn, "test.db")

        shutil.copy(os.path.join(self.data_dn, "haplotigs.tsv"), self.dn)

        runner = CliRunner()
        result = runner.invoke(cli, ["-d", self.dbfile, "init"])
        if result.exit_code != 0:
            print(result.output)
            raise Exception("Failed to init LAH!")

        result = runner.invoke(cli, ["-d", self.dbfile, "haplotig", "ingest", "-f", os.path.join(self.dn, "haplotigs.tsv"), "-g", "NA,rid,hid"])
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

    def add_haplotig_assemblies(self):
        db = LahDb(dbfile=self.dbfile)
        db.connect()
        session = db.session()
        for haplotig in session.query(Haplotig):
            src = haplotig.asm_fn(self.data_dn)
            dest = haplotig.asm_fn(self.dn)
            shutil.copy(src, dest)
        db.disconnect()

    def add_merged_assemblies(self):
        src = Haplotig.merged_fn(self.data_dn)
        dest = Haplotig.merged_fn(self.dn)
        shutil.copy(src, dest)

#-- TestDataset
