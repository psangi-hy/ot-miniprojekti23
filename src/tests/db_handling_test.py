import unittest
import db_handling

class Testdbhandling(unittest.TestCase):
    
    def test_rightbibtexkey(self):
        self.key = db_handling.bibtexgen("Mikko Mökö", "1980", "1", "55-52")
        self.assertEqual( self.key,"MM198015552")
    
    def test_bibtexkey_no_pages(self):
        self.key = db_handling.bibtexgen("Mikko Mökö", "1980", "1", None)
        self.assertEqual( self.key,"MM198010")
        

    def test_bibtetxgen_no_volume(self):
        self.key = db_handling.bibtexgen("Mikko Mökö", "1980", None, "55-52")
        self.assertEqual( self.key,"MM198005552")
    
    def test_bibtexgen_no_pages_and_volume(self):
        self.key = db_handling.bibtexgen("Mikko Mökö", "1980", None, None)
        self.assertEqual( self.key,"MM198000")
