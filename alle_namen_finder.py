import itertools
from db_manager import DBManager
from tqdm import tqdm
import cProfile
import pstats

table_from_this_file = "alle_namen"

db = DBManager("alle_namen_und_gefundene_namens.db")

# Tabelle erstellen (einmal am Anfang)
db.create_table_alle_namen()

def generate_combinations(max_len):
    """
    Gibt alle Kombinationen des Alphabets (klein), '-' und Zahlen zurück
    bis zur Länge max_len als Generator (spart Speicher).
    """
    list_aller_zeichen = list("abcdefghijklmnopqrstuvwxyz-0123456789!?:") 
    alphabet = len(list_aller_zeichen) 
    total = sum(alphabet**i for i in range(1, max_len+1))

    with tqdm(total=total, unit="tries") as pbar:
        for length in range(1, max_len + 1):
            for combo in itertools.product(list_aller_zeichen, repeat=length):
                url= "".join(combo)
                #print(url, end="\r")
                # Schauen ob der name schon da ist
                finde_url_in_data_base = db.find_by_title(in_table=table_from_this_file,such_url=url)
                if not finde_url_in_data_base:
                    db.add_name_in_alle_namen(such_url=url)
                pbar.update(1)

with cProfile.Profile() as pr:
    generate_combinations(4)
    db.close()
stats = pstats.Stats(pr)
stats.sort_stats(pstats.SortKey.TIME)
stats.dump_stats(filename="profile_n4_v1.prof")