from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    count = 0
    folder = os.path.dirname(os.path.abspath(__file__))
    fin = os.path.join(folder, filename)
    f = open(fin)
    text = f.read()
    text = text.replace("\n", "")
    f.close()
    titles_and_authors = []
    soup = BeautifulSoup(text, "html.parser")
    rows = soup.find_all("tr")
    title = soup.find_all("a", class_ = "bookTitle")
    author = soup.find_all("a", class_ = "authorName")
    for row in rows:
        titles_and_authors.append((title[count].get_text().strip(), author[count].get_text().strip()))
        count += 1
    return titles_and_authors
        
    

def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    url_list = []
    response = requests.get("https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc")
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("a", class_ = "bookTitle")
    for i in range(10):
        url_list.append("https://www.goodreads.com" + books[i].get("href"))
    return url_list


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    info = []
    response = requests.get(book_url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("h1", id = "bookTitle")
    info.append(title)
    author = soup.find("a", class_ = "authorName")
    info.append(author)
    pages = soup.find("span", itemprop = "numberOfPages")
    info.append(pages)
    result = tuple(info)
    return result


def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    count = 0
    result = []
    folder = os.path.dirname(os.path.abspath(__file__))
    fin = os.path.join(folder, filepath)
    f = open(fin, encoding = "UTF-8")
    text = f.read()
    text = text.replace("\n", "")
    f.close()
    soup = BeautifulSoup(text, "html.parser")
    categories = soup.find_all("h4", class_ = "category__copy")
    titles = soup.find_all("img", class_ = "category__winnerImage")
    urls = soup.find_all("a", class_ = None)
    for cat in categories:
        category = categories[count].get_text()
        title = titles[count]["alt"]
        url = urls[count + 1].get("href")
        result.append((category, title, url))
        count += 1
    return result
        
    


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    folder = os.path.dirname(os.path.abspath(__file__))
    fin = os.path.join(folder, filename)
    with open(fin, "w", newline = "") as csvfile:
        csvwriter = csv.writer(csvfile)
        headers = ["Book title", "Author Name"]
        csvwriter.writerow(headers)
        for row in data:
            csvwriter.writerow(row)


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

search_urls = get_search_links()

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls


    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        results = get_titles_from_search_results("search_results.htm")
        # check that the number of titles extracted is correct (20 titles)
        self.assertTrue(len(results), 20)
        # check that the variable you saved after calling the function is a list
        self.assertTrue(type(results), list)
        # check that each item in the list is a tuple
        for result in results:
            self.assertTrue(type(result), tuple)
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(results[0][0], "Harry Potter and the Deathly Hallows (Harry Potter, #7)")
        self.assertEqual(results[0][1], "J.K. Rowling")
        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(results[19][0], "Harry Potter: The Prequel (Harry Potter, #0.5)")
        self.assertEqual(results[19][1], "Julian Harrison")
        

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertIsInstance(search_urls, list)

        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertTrue(len(search_urls), 10)

        # check that each URL in the TestCases.search_urls is a string
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        for i in search_urls:
            self.assertIsInstance(i, str)
        exp = r"https:\/\/www.goodreads.com\/books\/show\/.+"
        for i in search_urls:
            self.assertFalse(re.search(exp, i), None)
            


    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        summaries = []
        # for each URL in TestCases.search_urls (should be a list of tuples)
        for url in search_urls:
            summaries.append(get_book_summary(url))

        # check that the number of book summaries is correct (10)
        self.assertTrue(len(summaries), 10)

            # check that each item in the list is a tuple
        for summary in summaries:
            self.assertIsInstance(summary, tuple)
            # check that each tuple has 3 elements
            self.assertTrue(len(summary), 3)
            # check that the first two elements in the tuple are string
            self.assertTrue(type(summary[0]), str)
            self.assertTrue(type(summary[1]), str)
            # check that the third element in the tuple, i.e. pages is an int
            self.assertTrue(type(summary[2]), int)
            # check that the first book in the search has 337 pages
        self.assertTrue(summaries[0][2], 337)

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        summary = summarize_best_books("best_books_2020.htm")
        # check that we have the right number of best books (20)
        self.assertEqual(len(summary), 20)
            # assert each item in the list of best books is a tuple
        for book in summary:
            self.assertTrue(type(book), tuple)
            # check that each tuple has a length of 3
            self.assertEqual(len(book), 3)
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
            self.assertEqual(summary[0][0], "Fiction")
            self.assertEqual(summary[0][1], "The Midnight Library")
            self.assertEqual(summary[0][2], "https://www.goodreads.com/choiceawards/best-fiction-books-2020")
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
            self.assertEqual(summary[19][0], "Picture Books")
            self.assertEqual(summary[19][1], "Antiracist Baby")
            self.assertEqual(summary[19][2], "https://www.goodreads.com/choiceawards/best-picture-books-2020")


    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        results = get_titles_from_search_results("search_results.htm")
    
        # call write csv on the variable you saved and 'test.csv'
        write_csv(results, "test.csv")

        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        folder = os.path.dirname(os.path.abspath(__file__))
        f = os.path.join(folder, "test.csv")
        csv_lines = []
        with open(f, "r", newline = "") as csvfile:
            csvreader = csv.reader(csvfile)
            for line in csvreader:
                csv_lines.append(line)

        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)

        # check that the header row is correct

        self.assertEqual(csv_lines[0][0], "Book title")
        self.assertEqual(csv_lines[0][1], "Author Name")

        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(csv_lines[1][0], "Harry Potter and the Deathly Hallows (Harry Potter, #7)")
        self.assertEqual(csv_lines[1][1], "J.K. Rowling")

        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(csv_lines[20][0], "Harry Potter: The Prequel (Harry Potter, #0.5)")
        self.assertEqual(csv_lines[20][1], "Julian Harrison")



if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



