import sqlite3
import sys

database = 'bag_o_loot.db'

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

# 1. Add a toy to the bag o' loot, and label it with the child's name who will receive it. The first argument must be the word add. The second argument is the gift to be delivered. The third argument is the name of the child.

def add():

  toy = {
    "name": sys.argv[2],
    # get child's ID from db using name in command line
    "childID": get_childID(sys.argv[3])
  }

  with sqlite3.connect(database) as conn:
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

def get_childID(name):
  with sqlite3.connect(database) as conn:
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

# 2. Remove a toy from the bag o' loot in case a child's status changes before delivery starts.
def remove(toy_id):

  with sqlite3.connect(database) as conn:
    cursor = conn.cursor()
    try:
      cursor.execute(f'''DELETE FROM Toy
                        WHERE toyID = '{toy_id}'
                        ''')

    except sqlite3.OperationalError as err:
      print("Error when attempting to remove toy from database...", err)

def get_toyID(toy_name):
  with sqlite3.connect(database) as conn:
    cursor = conn.cursor()
    try:
      cursor.execute(f'''SELECT Toy.toyID
                        FROM Toy
                        WHERE Toy.Name = '{toy_name}'
                        ''')

      toy_id = cursor.fetchone()
      return toy_id[0]

    except sqlite3.OperationalError as err:
      print("Error when getting toy ID...", err)

# 3. Produce a list of children currently receiving presents.

# 4. List toys in the bag o' loot for a specific child.

# 5. Specify when a child's toys have been delivered.

# ============================================================================

# Update delivered status if a child has received his/her one gift
# revoke delivered status if child has no gift in the database
def update_child_delivery_status(adding_item, child_id):

  print("updating delivered status...")

  if adding_item == True:
    with sqlite3.connect(database) as conn:
      cursor = conn.cursor()
      try:
        cursor.execute(f'''UPDATE Child
                          SET Delivered = 1
                          WHERE Child.childID = '{child_id}'
                        ''')
      except sqlite3.OperationalError as err:
        print("Error when updating delivered status after add...", err)
  else:
    with sqlite3.connect(database) as conn:
      cursor = conn.cursor()
      try:
        cursor.execute(f'''UPDATE Child
                          SET Delivered = 0
                          WHERE Child.childID = '{child_id}'
                        ''')
      except sqlite3.OperationalError as err:
        print("Error when updating delivered status after remove...", err)

# trigger function call based on command line input
if sys.argv[1] == 'add':
  print("adding toy to database...")
  child_id_from_add = add()
  update_child_delivery_status(True, child_id_from_add)

if sys.argv[1] == 'remove':
  print("removing toy from database...")
  toy_id = get_toyID(sys.argv[2])
  child_id = get_childID(sys.argv[3])
  remove(toy_id)
  update_child_delivery_status(False, child_id)

# if __name__ == '__main__':
#   child = Child("Jack")
#   child.add_child()