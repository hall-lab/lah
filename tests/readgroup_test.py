import os, tempfile, unittest

from .context import lah
from lah.read_group import ReadGroup
import lah.db

class LahReadGroupTest(unittest.TestCase):
    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()
        self.dbfile = os.path.join(self.temp_d.name, "test.db")

    def tearDown(self):
        self.temp_d.cleanup()

    def test1_read_group_create_and_get(self):
        dbfile = self.dbfile
        db = lah.db.LahDb(dbfile=dbfile)
        db.create()
        sessionmaker = db.connect()
        session = sessionmaker()

        read_group = ReadGroup(name="402_0_2_0", reads_cnt=14, assembly_id=1)
        self.assertIsNotNone(read_group)
        self.assertEqual(read_group.name, "402_0_2_0")
        self.assertEqual(read_group.reads_cnt, 14)

        session.add(read_group)
        session.commit()

        self.assertEqual(read_group.id, 1)
        read_group = session.query(ReadGroup).first()
        self.assertEqual(read_group.id, 1)

# -- LahReadGroupTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
