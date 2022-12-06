import unittest
from Session import Session
#Test cases to test Calulator methods
#You always create  a child class derived from unittest.TestCase
class TestSession(unittest.TestCase):
  #setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.session = Session(1,2)
  #Each test method starts with the keyword test_
    def test_admin_id(self):
        self.assertEqual(self.session.get_admin_id(), 1)
    def test_room_id(self):
        self.assertEqual(self.session.get_room_id(), 1)
# Executing the tests in the above test case class
if __name__ == "__main__":
  unittest.main()
