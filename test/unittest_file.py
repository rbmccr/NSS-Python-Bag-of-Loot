import sqlite3
import unittest
import sys

# Note: Use the tables.sql file to build the database tables BEFORE running this or any other tests!

sys.path.append("../")

from lootbag import Lootbag

class Testing(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    self.lootbag = Lootbag('../bag_o_loot.db')

# ==================================================================

# test if items can be added to bag, and assigned to a child.

  def test_add_toy(self):
    # function returns same ID that is passed in
    self.assertEqual(self.lootbag.add("Hotwheels", 1), 1)
    # database table will have toyID of 1
    self.assertEqual(self.lootbag.get_toyID("Hotwheels"), 1)
    # database table will return childID of 1 when toy name passed in
    self.assertEqual(self.lootbag.ls(1, True), "Hotwheels")

# ==================================================================

# Items can be removed from bag, per child.
# Removing a toy from the bag should not be allowed. A child's name must be specified.

  def test_remove_toy(self):
    # database has a toy with the name Hotwheels, and its ID is 1
    self.assertEqual(self.lootbag.get_toyID("Hotwheels"), 1)
    # database has a child "Brendan" with an ID of 1
    self.assertEqual(self.lootbag.get_childID("Brendan"), 1)
    # removing a toy without child name specified will throw error
    self.assertEqual(self.lootbag.remove(-1, 1), "No child specified")
    # removing the toy results in database response of toyID = None
    self.lootbag.remove(1)
    self.assertEqual(self.lootbag.get_toyID("Hotwheels"), None)

if __name__ == '__main__':
  unittest.main()