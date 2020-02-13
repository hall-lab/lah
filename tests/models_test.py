import os, unittest

from lah.db import LahDb
from lah.models import *

class ModelsTest(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "sample")
        self.dbfile = os.path.join(self.data_d, "test.db")
        self.db = LahDb(self.dbfile)
        self.db.connect()

    def test_metadata(self):
        session = self.db.session()
        md = session.query(Metadata).all()
        self.assertEqual(len(md), 3)

    def test_metrics(self):
        session = self.db.session()
        metrics = session.query(Metric).all()
        self.assertEqual(len(metrics), 2)

# -- ModelsTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
