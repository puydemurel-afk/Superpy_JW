Please include a short, 300-word report that highlights three technical elements of your implementation that you find notable.
Explain what problem they solve and why you chose to implement them in this way.


1.  bepaal wat de laatste dag van de maand is.
    probleem :  elke laatste dag van de maand is anders, waardes 31, 30, 29 en 28 (feb en schrikkeljaar)
    oplossing : je neemt van de maand de 28e dag, daar tel je 4 dagen bij op, dan zit je altijd in de volgende maand.
                vervolgens trek je van de huidige maand het aantal dagen van de volgende maand af en kom je op de laatste dag van de maand uit.
                bv 23 nov 2026, 28 nov + 4 dagen = 2 dec, 2 dec - 2 dagen is 30 nov

                begin_reken_datum = date.strptime(args.date,"%Y-%m")
                volgende_maand = begin_reken_datum.replace(day=28) + timedelta(days=4)
                eind_reken_datum = volgende_maand - timedelta(days=volgende_maand.day)
                print(f"reken datum : van {begin_reken_datum} tot {eind_reken_datum}")

2.  maak een simpele kassabon voor een verkocht product.
    probleem :  naar een pdf bestand schrijven en dit een unieke naam geven.
    oplossing : een time-stamp toevoegen aan de filenaam
                gebruik datetime.strftime om een string te maken van een datum en tijd.
                Module ReportLab gebruikt om regels in een pdf te schrijven.

                # kassabon in pdf schrijven
                datum_tijd = verkoop_datum + "_" + datetime.strftime(datetime.now(),"%H%M%S")
                kassabon_filename = "kassabon_" + datum_tijd + ".pdf"
                kassabon = canvas.Canvas(kassabon_filename)
                kassabon.drawString(10,800, "JW's Shop")
                kassabon.drawString(10,785,"tinytown NL +31612345678")
                kassabon.drawString(10,770,"KASSABON")
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

3.  verlopen producten uit de voorraad halen.
    probleem :  product vinden in de voorraad, product toevoegen aan bestand verlopen producten, product verwijderen uit voorraad
                en voorraad opnieuw opslaan
    oplossing : eerst de voorraad lezen en langs gaan om de index te zoeken van het te verwijderen product.
                daarna product toevoegen aan bestand door 'a' te gebruiken bij openen.
                nieuwe voorraad lijst maken en deze wegschrijven als nieuw bestand door 'w' te gebruiken bij openen bestand.

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
