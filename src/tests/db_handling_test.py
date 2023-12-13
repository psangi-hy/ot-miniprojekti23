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
   
    def test_bibtexkey_is_unique(self):
        result = db_handling.new_article("MM2022", "Mikko Mökö", "title1", "journal1", 2022, "1", "10-15", "tag")
        self.assertTrue(result)
     
        self.key = db_handling.bibtexgen("Mikko Mökö ja Reijo Kiva", 2022)
        self.assertEqual( self.key,"MM2022A")

        result = db_handling.new_article("MM2022A", "Mikko Mökö ja Reijo Kiva", "title1", "journal1", 2022, "1", "10-15", "tag")
        self.assertTrue(result)

        self.key = db_handling.bibtexgen("Mauri Musta", 2022)
        self.assertEqual( self.key,"MM2022B")

     
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
     
    def test_new_article(self):
        result = db_handling.new_article("key1", "author1", "title1", "journal1", 2022, "1", "10-15", "tag")
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
        self.assertEqual(article.tag, "tag")

        self.app_context.pop()
    
    def test_new_book(self):
        result = db_handling.new_book("key1", "author1", "title1", 2022, "publisher1", "1", "10-15", "tag")
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
        self.assertEqual(book.tag, "tag")

        self.app_context.pop()
    
    def test_new_inproceeding(self):
        result = db_handling.new_inproceeding("key1", "author1", "title1", 2022, "booktitle1", "10-15", "tag")
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
        self.assertEqual(inproceeding.tag, "tag")

        self.app_context.pop()
    
    def test_deleting(self):
        db_handling.new_book("key1", "author1", "title1", 2022, "publisher1", "1", "10-15", "tag")
        result = db_handling.delete_reference("book", 1)
        self.assertEqual(result, True)
        books = db_handling.select_all_books()
        self.assertEqual(len(books), 0)

        db_handling.new_article("key1", "author1", "title1", "journal1", 2022, "1", "10-15", "tag")
        result = db_handling.delete_reference("article", 1)
        self.assertEqual(result, True)
        articles = db_handling.select_all_articles()
        self.assertEqual(len(articles), 0)

        db_handling.new_inproceeding("key1", "author1", "title1", 2022, "booktitle1", "10-15", "tag")
        result = db_handling.delete_reference("inproceeding", 1)
        self.assertEqual(result, True)
        inproceedings = db_handling.select_all_inproceedings()
        self.assertEqual(len(inproceedings), 0)

        self.app_context.pop()

    def test_search_show_correct_references(self):
        result = db_handling.new_article("MM2022", "Mikko Mökö", "title1", "journal1", 2022, "1", "10-15", "tag1")
        self.assertTrue(result)

        result = db_handling.new_article("RK2022", "Reijo Kiva", "title2", "journal2", 2022, "1", "20", "tag2")
        self.assertTrue(result)

        result = db_handling.new_article("HK2022", "Heikki Kiva", "title3", "journal3", 2022, "1", "20", "tag3")
        self.assertTrue(result)
      
        search_results = db_handling.select_all_articles("tag2", "OR")
        search = search_results[0]
    
        self.assertEqual(search.key, "RK2022")
        self.assertEqual(search.author, "Reijo Kiva")
        self.assertEqual(search.title, "title2")
        self.assertEqual(search.journal, "journal2")
        self.assertEqual(search.year, 2022)
        self.assertEqual(search.volume, "1")
        self.assertEqual(search.pages, "20")
        self.assertEqual(search.tag, "tag2")

        search_results = db_handling.select_all_articles("tag3", "OR")
        search = search_results[0]
    
        self.assertEqual(search.key, "HK2022")
        self.assertEqual(search.author, "Heikki Kiva")
        self.assertEqual(search.title, "title3")
        self.assertEqual(search.journal, "journal3")
        self.assertEqual(search.year, 2022)
        self.assertEqual(search.volume, "1")
        self.assertEqual(search.pages, "20")
        self.assertEqual(search.tag, "tag3")

        search_results = db_handling.select_all_articles("tag1", "OR")
        search = search_results[0]
    
        self.assertEqual(search.key, "MM2022")
        self.assertEqual(search.author, "Mikko Mökö")
        self.assertEqual(search.title, "title1")
        self.assertEqual(search.journal, "journal1")
        self.assertEqual(search.year, 2022)
        self.assertEqual(search.volume, "1")
        self.assertEqual(search.pages, "10-15")
        self.assertEqual(search.tag, "tag1")

        self.app_context.pop()
    
    def test_OR_search_show_multiple_references(self):
        result = db_handling.new_article("MM2022", "Mikko Mökö", "title1", "journal1", 2022, "1", "10-15", "tag1")
        self.assertTrue(result)

        result = db_handling.new_article("RK2022", "Reijo Kiva", "title2", "journal2", 2022, "1", "20", "tag2")
        self.assertTrue(result)

        result = db_handling.new_article("HK2022", "Heikki Kiva", "title3", "journal3", 2022, "1", "20", "tag3")
        self.assertTrue(result)
        
        expected_results_found = False

        result_count = 0
        search_results = db_handling.select_all_articles("tag2 tag3", "OR")
        for search in search_results:
            if search.key == "RK2022":
                self.assertEqual(search.author, "Reijo Kiva")
                self.assertEqual(search.title, "title2")
                result_count += 1
            elif search.key == "HK2022":
                self.assertEqual(search.author, "Heikki Kiva")
                self.assertEqual(search.title, "title3")
                result_count += 1
        
        if result_count == 2:
            expected_results_found = True

        if not expected_results_found:
            self.fail("serach result not correct!")

        self.app_context.pop()
