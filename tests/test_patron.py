import unittest;
from library.patron import Patron, InvalidNameException;

class TestPatron(unittest.TestCase):

    def setUp(self):
        fname = "marigold"
        lname = "p"
        age = 22
        id = 0

        self.instance = Patron(fname,lname,age,id)

    def test_constructor(self):
        
        self.assertEqual(self.instance.fname,"marigold")
        self.assertEqual(self.instance.lname,"p")
        self.assertEqual(self.instance.age,22)
        self.assertEqual(self.instance.memberID,0)
        self.assertEqual(self.instance.borrowed_books,[])
        
    def test_bad_constructor(self):
        fname = "marigold"
        badfname = "mar1gold"
        lname = "parson"
        badlname = "pars0n"
        age = 22
        id=0
        
        with self.assertRaises(InvalidNameException):
            binstance = Patron(badfname,lname,age,id)
        with self.assertRaises(InvalidNameException):
            binstance = Patron(fname,badlname,age,id)
        with self.assertRaises(InvalidNameException):
            binstance = Patron(badfname,badlname,age,id)

    def test_add_borrowed_book(self):
        book = "Testing and YOU!"
        self.instance.add_borrowed_book(book)
        self.assertEqual(self.instance.get_borrowed_books(),[book.lower()])
        #test not add twice
        self.instance.add_borrowed_book(book)
        self.assertEqual(self.instance.get_borrowed_books(),[book.lower()])

    def test_return_borrowed_book(self):
        book = "Testing and ME!"
        self.instance.add_borrowed_book(book)
        #add, test remove
        self.instance.return_borrowed_book(book)
        self.assertEqual(self.instance.get_borrowed_books(),[])
        #try to remove again, should be fine
        self.instance.return_borrowed_book(book)
        self.assertEqual(self.instance.get_borrowed_books(),[])
        
    def test_equal_patrons(self):
        fname = 'marigold'
        lname ='p'
        age=22
        id=0
        second = Patron(fname,lname,age,id)
        #should be equal
        self.assertTrue(self.instance.__eq__(second))
    
    def test_unequal_patrons(self):
        fname='john'
        lname='testing'
        age=4
        id=1000000000000000
        second = Patron(fname,lname,age,id)
        #should be unequal
        self.assertTrue(self.instance.__ne__(second))

    def test_getters(self):
        self.assertEqual(self.instance.get_fname(),"marigold")
        self.assertEqual(self.instance.get_lname(),"p")
        self.assertEqual(self.instance.get_age(),22)
        self.assertEqual(self.instance.get_memberID(),0)