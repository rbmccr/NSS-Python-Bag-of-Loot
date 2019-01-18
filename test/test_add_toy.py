import sqlite3
import unittest
import sys

sys.path.append("../")

from lootbag import Lootbag
from lootbag import add

class Testing(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    self.db = Lootbag('../bag_o_loot.db')

  def item_assigned_to_child(self, toy_name):
    with sqlite3.connect(self.db) as conn:
      cursor = conn.cursor()
      cursor.execute(f'''SELECT Toy
                        FROM Toy
                        WHERE Toy.Name = '{toy_name}'
                        ''')
      toy_id = cursor.fetchone()
      return (toy_id[0], toy_id[1])

  def test_add_toy(self):
    self.assertEqual(add("Hotwheels", 1), 1) # returns same ID passed in
    # self.assertEqual(item_assigned_to_child("Hotwheels"),("Hotwheels", 1))

if __name__ == '__main__':
  unittest.main()