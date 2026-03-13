from db_manager import DBManager
aniworld_db="instance/aniworld.db"
db = DBManager(aniworld_db)
tabel_name_anime="anime_namen"

def print_table(in_table):
    rows = db.get_all_in_table(table_name=in_table)
    for row in rows:
        print(row) 
    
def print_collum(in_table):
    rows = db.get_all_collum_in_table(table_name=in_table,coolum="such_url")
    for row in rows:
        print(row[0]) 
    
#print_table(tabel_name_anime)
print_collum(tabel_name_anime)