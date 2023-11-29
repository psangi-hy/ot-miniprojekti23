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
    
    def test_validate_year_accepts_years_only(self):
        self.assertEqual(db_handling.validate_year("sata"), False)
        self.assertEqual(db_handling.validate_year("10-20"), False)
        self.assertEqual(db_handling.validate_year("10 20"), False)
        self.assertEqual(db_handling.validate_year("1001"), True)
    
    def test_validate_pages_accepts_pages_only(self):
        self.assertEqual(db_handling.validate_pages("sata"), False)
        self.assertEqual(db_handling.validate_pages("10 - 20"), True)
        self.assertEqual(db_handling.validate_pages("10-20"), True)
        self.assertEqual(db_handling.validate_pages(""), True)
        self.assertEqual(db_handling.validate_pages("1001"), True)
    
    def test_validate_volume_accepts_volumes_only(self):
        self.assertEqual(db_handling.validate_volume("sata"), False)
        self.assertEqual(db_handling.validate_volume("10-20"), False)
        self.assertEqual(db_handling.validate_volume("10 20"), False)
        self.assertEqual(db_handling.validate_volume(""), True)
        self.assertEqual(db_handling.validate_volume("1001"), True)

