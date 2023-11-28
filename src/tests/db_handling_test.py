import unittest
import db_handling

class Testdbhandling(unittest.TestCase):
    
    def test_rightbibtexkey(self):
        self.key = db_handling.bibtexgen("Mikko Mökö", "1980", "1", "55-52")
        self.assertEqual( self.key,"MM198015552")