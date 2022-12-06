import unittest
from Session import Session
#Test cases to test Calulator methods
#You always create  a child class derived from unittest.TestCase
class TestSession(unittest.TestCase):
    def setUp(self):
        self.session = Session(1,1)
        
    def test_admin_id(self):
        self.assertEqual(self.session.get_admin_id(), 1)
        
    def test_room_id(self):
        self.assertEqual(self.session.get_room_id(), 1)
        
    def test_get_number_of_players(self):
        self.session.set_new_player(1)
        self.session.set_new_player(2)
        self.assertEqual(len(self.session.get_players()), 2)
        
# Executing the tests in the above test case class
if __name__ == "__main__":
  unittest.main()
