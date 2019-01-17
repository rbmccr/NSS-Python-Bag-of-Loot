import sqlite3
import sys

database = 'bag_o_loot.db'

# ============================================================================

# 0. Class created for establishing child props and method to add to database
class Child:
  def __init__(self, name, delivered = 0):
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

  print(toy["childID"])

  with sqlite3.connect(database) as conn:
    cursor = conn.cursor()
    try:
      cursor.execute(
        '''
        INSERT INTO Toy
        Values(?,?,?)
        ''', (None, toy["name"], toy["childID"])
      )

      # set child's delivered status to 1
      update_child_delivery_status(True, toy["childID"])

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

# 3. Produce a list of children currently receiving presents.

# 4. List toys in the bag o' loot for a specific child.

# 5. Specify when a child's toys have been delivered.

# ============================================================================

# Update delivered status if a child has received his/her one gift
# revoke delivered status if child has no gift in the database
def update_child_delivery_status(adding_item, child_id):
  print("updating delivered status")
  if adding_item == True:
    with sqlite3.connect(database) as conn:
      cursor = conn.cursor()
      try:
        cursor.execute(f'''UPDATE Child
                          SET Delivered = 1
                          WHERE Child.childID = '{child_id}'
                        ''')
      except sqlite3.OperationalError as err:
        print("Error when updating delivered status...", err)
  else:
    # ....
    print('something')

# trigger function call based on command line input
if sys.argv[1] == 'add':
  print("adding toy to database...")
  add()

if sys.argv[1] == 'remove':
  print("removing toy from database...")
  # remove()

# if __name__ == '__main__':
#   child3 = Child("Zac")
#   child3.add_child()