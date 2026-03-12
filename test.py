from db_manager import DBManager
db = DBManager("aniworld.db")

def print_table(in_table):
    rows = db.get_all("alle_namen")
    for row in rows:
        print(row) 
    
db.delete_all_in_table("alle_namen")
print_table("alle_namen")
