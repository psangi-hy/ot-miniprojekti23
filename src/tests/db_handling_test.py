import unittest
import db_handling
from app import app

class Testdbhandling(unittest.TestCase):

    def setUp(self):
    
        self.app_context = app.app_context()
        self.app_context.push()
        db_handling.reset_tests()
    
    def test_rightbibtexkey(self):
        self.key = db_handling.bibtexgen("Mikko Mökö", "1980")
        self.assertEqual( self.key,"MM1980")

 
    def test_bibtexkey_no_pages(self):
        self.key = db_handling.bibtexgen("Mikko Mökö ja Reijo Kiva", "1980")
        self.assertEqual( self.key,"MM1980")

     
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
        result = db_handling.new_book("key1", "author1", "title1", 2022, "publisher1", "1", "10-15")
        self.assertTrue(result)

        books = db_handling.select_all_books()
        self.assertEqual(len(books), 1)

        book = books[0]
        self.assertEqual(book.key, "key1")
        self.assertEqual(book.author, "author1")
        self.assertEqual(book.title, "title1")
        self.assertEqual(book.year, 2022)
        self.assertEqual(book.publisher, "publisher1")
        self.assertEqual(book.volume, "1")
        self.assertEqual(book.pages, "10-15")

        self.app_context.pop()
    
    def test_new_inproceeding(self):
        result = db_handling.new_inproceeding("key1", "author1", "title1", 2022, "booktitle1", "10-15")
        self.assertTrue(result)

        inproceedings = db_handling.select_all_inproceedings()
        self.assertEqual(len(inproceedings), 1)

        inproceeding = inproceedings[0]
        self.assertEqual(inproceeding.key, "key1")
        self.assertEqual(inproceeding.author, "author1")
        self.assertEqual(inproceeding.title, "title1")
        self.assertEqual(inproceeding.year, 2022)
        self.assertEqual(inproceeding.booktitle, "booktitle1")
        self.assertEqual(inproceeding.pages, "10-15")

        self.app_context.pop()
    


