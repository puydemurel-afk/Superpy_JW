# imports
import csv
from datetime import *

def verzet_tijd(args):
    # interval is het aantal dagen waarmee de datum aangepast moet worden
    interval = timedelta(days=args.advance_time)
    with open('datum.txt','r+', encoding="utf-8", newline="") as date_file:
        # lees de datum die we opgeslagen hebben
        datum_from_file = date_file.read()
        # maak van de string(datum) een datum type
        datum_type_date = date.strptime(datum_from_file,"%Y-%m-%d")
        # pas de opgeslagen datum aan met de meegegeven interval
        datum_save_to_file = datum_type_date + interval
        # schrijf de aangepaste datum als een string in datum.txt
        date_file.seek(0)
        date_file.write(datum_save_to_file.strftime("%Y-%m-%d"))
        return


def save_date():
    # sla de huidige datum op in datum.txt
    Current_date_time = str(datetime.now())
    datum = Current_date_time.split(" ")
    with open('datum.txt','r+', encoding="utf-8", newline="") as date_file:
        date_from_file = date_file.read()
        if date_from_file == "":
            date_file.write(datum[0])
        return


def specify_time(args):
    print(args.set_time)
    # sla de meegegeven datum op in datum.txt
    with open('datum.txt','w', encoding="utf-8", newline="") as date_file:
        #date_from_file = date_file.read()
        date_file.write(args.set_time)   
    return