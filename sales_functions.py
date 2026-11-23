# imports
import csv
from datetime import *
from reportlab.pdfgen import canvas
from time import *


def buy(args):
    # last_id = 0 (als bought.csv leeg is)
    last_id = "0"
    # aankoop datum is de datum die in datum.txt staat
    with open('datum.txt','r') as datum_file:
        aankoop_datum = datum_file.read()

    # check if expiration date is not older than buy date (product is already expired, why buy it)
    check_aankoop_datum = datetime.strptime(aankoop_datum,"%Y-%m-%d")
    if args.expiration_date == None:
        # if no expiration date is given, set it default 5 years ahead
        check_expiration_date = check_aankoop_datum + timedelta(days=(365*5))
        args.expiration_date = check_expiration_date.date()
    else:
        check_expiration_date = datetime.strptime(args.expiration_date,"%Y-%m-%d")
    check_interval = check_expiration_date - check_aankoop_datum
    if check_interval.days <= 0:
        # maak check_interval een string
        check_interval_string = str(abs(check_interval))
        print(f"The product {args.product_name} is already expired by {check_interval_string.split(",")[0]}, why would you buy it?")
        return

    # open bought.csv en stock.csv
    with open('bought.csv','r+', newline="") as buy_file, open('stock.csv','r+', newline="") as stock_file:
        buy_reader = csv.DictReader(buy_file)
        stock_reader = csv.DictReader(stock_file)
        
        rows_buy = list(buy_reader)
        rows_stock = list(stock_reader)
        # zoek in de bought.csv de laatste id
        for line in rows_buy:
            last_id = line['id']

        # je koopt altijd 1 product (default = 1)
        quantity_counter = 1
        while quantity_counter <= args.quantity:
            # de id van de aankoop is 1 hoger dan de laatste id in bought.csv
            last_id = str(int(last_id) + 1)

            # zet wat ik wil kopen eerst in een dictionary zo dat ik die aan bought.csv kan toevoegen
            buy_dict = {'id': last_id, 'product_name': args.product_name, 'buy_date': aankoop_datum, 'buy_price': args.price, 'expiration_date': args.expiration_date}
            stock_dict = {'id': last_id, 'product_name': args.product_name, 'buy_date': aankoop_datum, 'buy_price': args.price, 'expiration_date': args.expiration_date, 'bought_id': last_id}

            # ga naar begin van bought.csv en stock.csv
            buy_file.seek(0)
            stock_file.seek(0)
            # voeg de aankoop toe aan ingelezen regels(rows)
            rows_buy.append(buy_dict)
            rows_stock.append(stock_dict)
       
            # schrijf de regels weg incl de nieuwe aankoop in bought.csv
            buy_writer = csv.DictWriter(buy_file, fieldnames= buy_reader.fieldnames)      
            buy_writer.writeheader()
            buy_writer.writerows(rows_buy)

            # schrijf de regels weg incl de nieuwe aankoop in stock.csv
            stock_writer = csv.DictWriter(stock_file, fieldnames= stock_reader.fieldnames)
            stock_writer.writeheader()
            stock_writer.writerows(rows_stock)
            
            # quantity counter ophogen
            quantity_counter = quantity_counter + 1

        return


def sell(args):
    # last_id = 0 (als sold.csv leeg is)
    last_id_sold = "0"
    # verkoop datum is de datum die in datum.txt staat
    with open('datum.txt','r') as datum_file:
        verkoop_datum = datum_file.read()

    # open sold.csv en stock.csv
    with open('sold.csv','r+', newline="") as sold_file, open('stock.csv','r', newline="") as stock_file:
        sold_reader = csv.DictReader(sold_file)
        stock_reader = csv.DictReader(stock_file)
        rows_sold = list(sold_reader)
        rows_stock = list(stock_reader)

        # zoek in de sold.csv de laatste id
        for line in rows_sold:
            last_id_sold = line["id"]

        # nu checken of product (args.product_name) wel in de voorraad (stock) voorkomt
        index_stock = 0
        stock_found = False
        for row in rows_stock:
            #last_id = row['id']
            if row["product_name"] == args.product_name:
                # ja, dan product_name opslaan in sold en regel uit voorraad (stock) halen
                # de id van de aankoop is 1 hoger dan de laatste id in sold.csv
                stock_found = True
                last_id_sold = str(int(last_id_sold) + 1)
                # zet wat ik wil kopen eerst in een dictionary zo dat ik die aan bought.csv kan toevoegen
                sold_dict = {'id': last_id_sold, 'bought_id': row["bought_id"], 'sell_date': verkoop_datum, 'sell_price': args.price}           
                # ga naar begin van sold.csv
                sold_file.seek(0)
                # voeg de aankoop toe aan ingelezen regels(rows)
                rows_sold.append(sold_dict)
                # schrijf de regels weg incl de nieuwe aankoop in bought.csv
                sold_writer = csv.DictWriter(sold_file, fieldnames= sold_reader.fieldnames)      
                sold_writer.writeheader()
                sold_writer.writerows(rows_sold)      
                break
            index_stock = index_stock + 1

    if stock_found == False:
        # nee, dan error geven en stoppen (return)
        print(f"ERROR : Product {args.product_name} is not in stock")
    else:
        # haal regel uit voorraad (stock)
        removed_stock_item = rows_stock.pop(index_stock)
        with open('stock.csv','w', newline="") as stock_file:
            # schrijf de regels weg excl de nieuwe verkoop in stock.csv
            stock_writer = csv.DictWriter(stock_file, fieldnames= stock_reader.fieldnames)
            stock_writer.writeheader()
            stock_writer.writerows(rows_stock)   

        # kassabon in pdf schrijven
        datum_tijd = verkoop_datum + "_" + datetime.strftime(datetime.now(),"%H%M%S")
        kassabon_filename = "kassabon_" + datum_tijd + ".pdf"
        kassabon = canvas.Canvas(kassabon_filename)
        kassabon.drawString(10,800, "JW's Shop")
        kassabon.drawString(10,785,"tinytown NL +31612345678")
        kassabon.drawString(10,770,"KASSABON")
        #kassabon.drawString(10,755," ")
        kassabon.drawString(10,740,datum_tijd)
        kassabon.drawString(10,725,args.product_name)
        totaalprijs = "Totaal (incl btw) " + str(args.price)
        kassabon.drawString(10,710, totaalprijs)
        ex_btw = args.price * 0.79
        btw = args.price * 0.21
        btw_regel = "Incl BTW: 21%      " + str(args.price) + "            " + str(btw)
        btw_regel_info = "                BTW      bedrag      btw"
        kassabon.drawString(10,695,btw_regel_info)
        kassabon.drawString(10,680,btw_regel)
        kassabon.drawString(10,645,"Bedankt voor uw bezoek")
        kassabon.save()
    return


def expired():
    with open('stock.csv','r', newline="") as stock_file, open('datum.txt','r') as datum_file:
        stock_reader = csv.DictReader(stock_file)
        rows_stock = list(stock_reader)
        expired_stock = []
        datum_from_file = datum_file.read()
        datum_type_date = date.strptime(datum_from_file,"%Y-%m-%d")
        indexes_to_remove = []
        index_stock = 1
        for row in rows_stock:
            if date.strptime(row["expiration_date"],"%Y-%m-%d") < datum_type_date:
                # product has expired
                # store indexes remove product from stock
                indexes_to_remove.append(index_stock)
                expired_stock.append(row)
            index_stock = index_stock + 1

    with open('expired_products.csv','a',newline="") as expired_file:
        # write to file expited products
        expired_writer = csv.DictWriter(expired_file, fieldnames= stock_reader.fieldnames)
        expired_writer.writerows(expired_stock)
        
    #remove product from stock
    # first reverse indexes to remove so we remove from end to beginning
    new_stock = []
    index_stock = 0
    for row in rows_stock:
        index_stock = index_stock + 1
        if index_stock in indexes_to_remove:
            pass
        else:
            new_stock.append(row)

    with open('stock.csv','w', newline="") as stock_file:
        stock_writer = csv.DictWriter(stock_file, fieldnames= stock_reader.fieldnames)
        stock_writer.writeheader()
        stock_writer.writerows(new_stock)
    print("Voorraad gecheckt op expired producten")
    return
