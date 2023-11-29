import unittest
import db_handling
from app import app

class Testdbhandling(unittest.TestCase):

    def setUp(self):
    
        self.app_context = app.app_context()
        self.app_context.push()
        db_handling.reset_tests()
    
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

     
    def test_new_article(self):
        result = db_handling.new_article("key1", "author1", "title1", "journal1", 2022, "1", "10-15")
        self.assertTrue(result)

        articles = db_handling.select_all_articles()
        self.assertEqual(len(articles), 1)

        article = articles[0]
        self.assertEqual(article.key, "key1")
        self.assertEqual(article.author, "author1")
        self.assertEqual(article.title, "title1")
        self.assertEqual(article.journal, "journal1")
        self.assertEqual(article.year, 2022)
        self.assertEqual(article.volume, "1")
        self.assertEqual(article.pages, "10-15")

        self.app_context.pop()
    
    def test_new_book(self):
        result = db_handling.new_article("key1", "author1", "title1", "journal1", 2022, "1", "10-15")
        self.assertTrue(result)

        articles = db_handling.select_all_articles()
        self.assertEqual(len(articles), 1)

        article = articles[0]
        self.assertEqual(article.key, "key1")
        self.assertEqual(article.author, "author1")
        self.assertEqual(article.title, "title1")
        self.assertEqual(article.journal, "journal1")
        self.assertEqual(article.year, 2022)
        self.assertEqual(article.volume, "1")
        self.assertEqual(article.pages, "10-15")

        self.app_context.pop()
    
    def test_new_inproceeding(self):
        result = db_handling.new_article("key1", "author1", "title1", "journal1", 2022, "1", "10-15")
        self.assertTrue(result)

        articles = db_handling.select_all_articles()
        self.assertEqual(len(articles), 1)

        article = articles[0]
        self.assertEqual(article.key, "key1")
        self.assertEqual(article.author, "author1")
        self.assertEqual(article.title, "title1")
        self.assertEqual(article.journal, "journal1")
        self.assertEqual(article.year, 2022)
        self.assertEqual(article.volume, "1")
        self.assertEqual(article.pages, "10-15")

        self.app_context.pop()
    


