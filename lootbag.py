import sqlite3
import sys

database = 'bag_o_loot.db' # TODO: CHANGE PATH WHEN RUNNING TESTS

# IMPORTANT:
  # 1. Children must have unique names
  # 2. Children can only receive one present (removing a present revokes a child's toy dilvery status in command line)

# ============================================================================

# 0. Class created for establishing child props and method to add to database
class Child:
  def __init__(self, name, delivered=0):
    self.name = name
    self.delivered = delivered

  def add_child(self):

    child = {
      "name": self.name,
      "delivered": self.delivered
    }

    with sqlite3.connect(database) as conn:
      cursor = conn.cursor()

      try:
        cursor.execute(
          '''
          INSERT INTO Child
          Values(?,?,?)
          ''', (None, child["name"], child["delivered"])
        )
      except sqlite3.OperationalError as err:
        print("Error when attempting to post child to database...", err)

# ============================================================================

class Lootbag:
  def __init__(self, db = 'bag_o_loot.db'): # TODO: CHANGE PATH WHEN RUNNING TESTS
    self.db = db

# 1. Add a toy to the bag o' loot, and label it with the child's name who will receive it. The first argument must be the word add. The second argument is the gift to be delivered. The third argument is the name of the child.

  def add(self, name, child_id):

    toy = {
      "name": name,
      # get child's ID from db using name in command line
      "childID": child_id
    }

    with sqlite3.connect(self.db) as conn:
      cursor = conn.cursor()
      try:
        cursor.execute(
          '''
          INSERT INTO Toy
          Values(?,?,?)
          ''', (None, toy["name"], toy["childID"])
        )

        # return data used to set child's toy delivery status to 1
        return toy["childID"]

      except sqlite3.OperationalError as err:
        print("Error when attempting to post toy to database...", err)

  def get_childID(self, name):
    with sqlite3.connect(self.db) as conn:
      cursor = conn.cursor()
      try:
        cursor.execute(f'''SELECT Child.childID
                          FROM Child
                          WHERE Child.Name = '{name}'
                          ''')

        child_id = cursor.fetchone()
        return child_id[0]

      except sqlite3.OperationalError as err:
        print("Error when getting child ID...", err)

  # ============================================================================

  # 2. Remove a toy from the bag o' loot in case a child's status changes before  delivery starts.
  def remove(self, child_id=None, toy_id=1):

    if type(child_id) == int and child_id > 0:
      with sqlite3.connect(self.db) as conn:
        cursor = conn.cursor()
        try:
          cursor.execute(f'''DELETE FROM Toy
                            WHERE toyID = '{toy_id}'
                            ''')

        except sqlite3.OperationalError as err:
          print("Error when attempting to remove toy from database...", err)
    else:
      return "No child specified"

  def get_toyID(self, toy_name):
    with sqlite3.connect(self.db) as conn:
      cursor = conn.cursor()
      try:
        cursor.execute(f'''SELECT Toy.toyID
                          FROM Toy
                          WHERE Toy.Name = '{toy_name}'
                          ''')
        toy_id = cursor.fetchone()
        if toy_id != None:
          return toy_id[0]

      except sqlite3.OperationalError as err:
        print("Error when getting toy ID...", err)

  # ============================================================================

  # 3. Produce a list of children currently receiving presents.
  def ls(self, child_id=None, setting_delivered_status=False):
    if child_id == None:
      return "No child ID specified"

    if child_id == False:
      with sqlite3.connect(self.db) as conn:
        cursor = conn.cursor()
        try:
          list_of_names = list()
          for row in cursor.execute('''SELECT *
                            FROM Child
                            WHERE Child.Delivered = 1
                            '''):
            list_of_names.append(row[1])
            print(row[1])
          return list_of_names

        except sqlite3.OperationalError as err:
          print("Error when getting list of children...", err)
    else:
      # 4. List toys in the bag o' loot for a specific child.
      with sqlite3.connect(self.db) as conn:
        cursor = conn.cursor()
        try:
          cursor.execute(f'''SELECT Toy.Name
                            FROM Toy
                            WHERE Toy.childID = '{child_id}'
                            ''')
          toy_name = cursor.fetchone()
          try:
            if setting_delivered_status == True: # IF statement used with #5 to   handle delivery status
              return toy_name[0]
            else:
              print("Toy: ", toy_name[0])
              return toy_name[0]
          except TypeError:
            print("This child has no toy listed in the database.")
            return False

        except sqlite3.OperationalError as err:
          print("Error when getting list of children...", err)

  # ============================================================================

  # 5. Specify when a child's toys have been delivered (sets false to true).
  def delivered(self, child_id):
    self.update_child_delivery_status(True, child_id)

  #============================================================================

  # Update delivered status if a child has received his/her one gift
  # revoke delivered status if child has no gift in the database
  def update_child_delivery_status(self, adding_item, child_id):
    if adding_item == True:
      with sqlite3.connect(self.db) as conn:
        cursor = conn.cursor()
        try:
          cursor.execute(f'''UPDATE Child
                            SET Delivered = 1
                            WHERE Child.childID = '{child_id}'
                          ''')
        except sqlite3.OperationalError as err:
          print("Error when updating delivered status after add...", err)
    else:
      with sqlite3.connect(self.db) as conn:
        cursor = conn.cursor()
        try:
          cursor.execute(f'''UPDATE Child
                            SET Delivered = 0
                            WHERE Child.childID = '{child_id}'
                          ''')
        except sqlite3.OperationalError as err:
          print("Error when updating delivered status after remove...", err)

# ============================================================================

lootbag = Lootbag()

if __name__ == '__main__':

  # trigger function call based on command line input
  if sys.argv[1] == 'add':
    print("adding toy to database...")
    child_id_from_add = lootbag.add(sys.argv[2],  lootbag.get_childID(sys.argv[3]))
    lootbag.update_child_delivery_status(True, child_id_from_add)

  if sys.argv[1] == 'remove':
    print("removing toy from database...")
    toy_id = lootbag.get_toyID(sys.argv[2])
    child_id = lootbag.get_childID(sys.argv[3])
    lootbag.remove(toy_id)
    lootbag.update_child_delivery_status(False, child_id)

  if sys.argv[1] == 'ls':
    try:
      if sys.argv[2] != None:
        print(f"listing {sys.argv[2]}'s stored present...")
        child_id = lootbag.get_childID(sys.argv[2])
        lootbag.ls(child_id)
    except IndexError:
      print("listing names of children who have received a present (none if no names listed)...")
      lootbag.ls(False) # don't pass a specific name in

  if sys.argv[1] == 'delivered':
    child_id = lootbag.get_childID(sys.argv[2])
    toy_name = lootbag.ls(child_id, True)
    toy_id = lootbag.get_toyID(toy_name) # if this method returns False, then there's not a toy in the database for this child
    if toy_id != None:
      print("updating delivered status...")
      lootbag.delivered(child_id)