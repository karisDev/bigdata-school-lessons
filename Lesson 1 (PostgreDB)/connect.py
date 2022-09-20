# database credentials
credentials = {
  'host': 'localhost',
  'database': 'database',
  'port': 5433,
  'user': 'root',
  'password': 'root'
}

# terminal color escape-codes
class cl:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

# phrases
locale = {
  'cancel': f"{cl.OKGREEN}Canceled!{cl.ENDC}",
  'init': {
    'connecting': f"{cl.HEADER}Connecting to database...{cl.ENDC}",
    'connected': f"{cl.OKGREEN}Connected!{cl.ENDC}",
    'failed': f"{cl.FAIL}Failed to connect to database! Check your credentials.{cl.ENDC}"
  },
  'disconnected': f"{cl.OKGREEN}Disconnected from database!{cl.ENDC}",
  'create': {
    'intro':f"{cl.HEADER}{cl.BOLD}Creating new entry...{cl.ENDC}",
    'success': f"{cl.OKGREEN}Entry created successfully!{cl.ENDC}",
    'fail': f"{cl.FAIL}Failed to create entry!{cl.ENDC}",
    'enter': {
      'name': f"{cl.OKCYAN}Enter name: {cl.ENDC}",
      'surname': f"{cl.OKCYAN}Enter surname: {cl.ENDC}",
      'age': f"{cl.OKCYAN}Enter age: {cl.ENDC}",
    }
  },
  'show': {
    'intro': f"{cl.HEADER}{cl.BOLD}Entries:{cl.ENDC}",
    'empty': f"{cl.WARNING}Table is empty!{cl.ENDC}",
    'fail': f"{cl.FAIL}Failed to show entries!{cl.ENDC}"
  },
  'delete': {
    'no_entries': f"{cl.WARNING}There are no entries to delete!{cl.ENDC}",
    'enter_id': f"{cl.OKCYAN}Enter id: {cl.ENDC}",
    'success': f"{cl.OKGREEN}Entry deleted successfully! (if it existed){cl.ENDC}",
    'fail': f"{cl.FAIL}Failed to delete entry!{cl.ENDC}"
  },
  'update': {
    'no_entries': f"{cl.WARNING}There are no entries to update!{cl.ENDC}",
    'enter': {
      'id': f"{cl.OKCYAN}Enter id: {cl.ENDC}",
      'name': f"{cl.OKCYAN}Enter name: {cl.ENDC}",
      'surname': f"{cl.OKCYAN}Enter surname: {cl.ENDC}",
      'age': f"{cl.OKCYAN}Enter age: {cl.ENDC}",
    },
    'success': f"{cl.OKGREEN}Entry updated successfully! (if it existed){cl.ENDC}",
    'fail': f"{cl.FAIL}Failed to update entry!{cl.ENDC}"
  }
}

# all database related functions
class db_worker:
  def __init__(self, credentials):
    import psycopg2
    try:
      print(locale["init"]["connecting"])
      self.db = psycopg2.connect(**credentials)
      self.c = self.db.cursor()
      self.init_table()
      print(locale["init"]["connected"])
    except:
      self.db = None
      exit(locale["init"]["failed"])

  def __del__(self):
    if self.db:
      self.db.close()
      print(locale["disconnected"])

  def show_entries(self): # returns True if there are entries
    import pandas
    print(locale["show"]["intro"])
    try:
      self.db.rollback() # rollback if last comand had an error
      self.c.execute("SELECT * FROM users")
      data = self.c.fetchall()
      df = pandas.DataFrame(data, columns=["id", "name", "surname", "age"])
      print(locale["show"]["empty"] if df.empty else f"{cl.OKBLUE}{df.to_string(index=False)}{cl.ENDC}", '\n')
      return not df.empty
    except:
      print(locale["show"]["fail"])
      return False

  def create_entry(self):
    print(locale["create"]["intro"] + '\n')
    try:
      name = input(locale["create"]["enter"]["name"])
      surname = input(locale["create"]["enter"]["surname"])
      age = input(locale["create"]["enter"]["age"])
      
      self.c.execute(f"INSERT INTO users (name, surname, age) VALUES ('{name}', '{surname}', '{age}')")
      self.db.commit()
      return locale["create"]["success"]
    except KeyboardInterrupt:
      return locale["cancel"]
    except:
      return locale["create"]["fail"]

  def delete_entry(self):
    if not self.show_entries():
      return locale["delete"]["no_entries"]
    
    try:
      id = input(locale["delete"]["enter_id"])
      self.c.execute(f"DELETE FROM users WHERE id = {id}")
      self.db.commit()
      return locale["delete"]["success"]
    except KeyboardInterrupt:
      return locale["cancel"]
    except:
      return locale["delete"]["fail"]

  def update_entry(self):
    if not self.show_entries():
      return locale["update"]["no_entries"]
    
    try:
      id = input(locale["update"]["enter"]["id"])
      name = input(locale["update"]["enter"]["name"])
      surname = input(locale["update"]["enter"]["surname"])
      age = input(locale["update"]["enter"]["age"])
      self.c.execute(f"UPDATE users SET name = '{name}', surname = '{surname}', age = '{age}' WHERE id = {id}")
      self.db.commit()
      return locale["update"]["success"]
    except KeyboardInterrupt:
      return locale["cancel"]
    except:
      return locale["update"]["fail"]

  def init_table(self):
    self.c.execute("CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY, name varchar(255), surname varchar(255), age int)")
    self.db.commit()

def choose_command(commands, header='Choose command:'):
  print(f"{cl.HEADER}{cl.BOLD}{header}{cl.ENDC}")
  for i in range(len(commands)):
    print(f"{cl.OKBLUE}{i+1}. {commands[i]}{cl.ENDC}")
  
  while (command := input(f"\n{cl.OKCYAN}Choose command: {cl.ENDC}")) not in [str(i) for i in range(1, len(commands)+1)]:
    print(f"{cl.WARNING}Invalid command!{cl.ENDC}")
  else:
    return command

def check_requirements():
  try:
    import psycopg2
  except:
    exit(f"{cl.FAIL}psycopg2 is not installed!{cl.ENDC}\n{cl.OKCYAN}Run {cl.BOLD}'pip3 install psycopg2'{cl.ENDC}{cl.OKCYAN} to install it.{cl.ENDC}")
  
  try:
    import pandas
  except:
    exit(f"{cl.FAIL}pandas is not installed!{cl.ENDC}\n{cl.OKCYAN}Run {cl.BOLD}'pip3 install pandas'{cl.ENDC}{cl.OKCYAN} to install it.{cl.ENDC}")

def main():
  print("\033c")
  check_requirements()

  db = db_worker(credentials)
  try:
    callback_message = None
    while True:
      print("\033c")
      db.show_entries()

      if callback_message:
        print(f"{cl.HEADER}{cl.BOLD}Message:{cl.ENDC}\n{callback_message}\n")
        callback_message = None
      
      command = choose_command(['Create entry', 'Delete entry', 'Update entry', 'Exit'], "Supported operations:")
      print("\033c")
      if command == '1':
        callback_message = db.create_entry()
      elif command == '2':
        callback_message = db.delete_entry()
      elif command == '3':
        callback_message = db.update_entry()
      elif command == '4':
        exit(f"{cl.OKGREEN}\nExiting...{cl.ENDC}")
  except KeyboardInterrupt:
    exit(f"{cl.OKGREEN}\n\nExiting...{cl.ENDC}")

if __name__ == '__main__':
  main()
