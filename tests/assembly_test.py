import os, tempfile, unittest

from .context import lah
from lah.assembly import Assembly
import lah.db

class LahAssemblyTests(unittest.TestCase):
    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()
        dbfile = os.path.join(self.temp_d.name, "test.db")
        lah.db.create(database_file=dbfile)
        self.session = lah.db.connect(database_file=dbfile)

    def tearDown(self):
        self.temp_d.cleanup()

    def test1_assembly_create_and_get(self):
        asm = Assembly(directory="/blah")
        self.assertIsNotNone(asm)
        self.assertEqual(asm.directory, "/blah")

        self.session.add(asm)
        self.session.commit()
        self.assertEqual(asm.id, 1)
        asm = self.session.query(Assembly).first()
        self.assertEqual(asm.id, 1)

# -- LahAssemblyTests

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
