# imports
import csv
from datetime import *
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Spacer, Paragraph, Table, SimpleDocTemplate
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing
from rich import print
from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.table import Table as tb


def report(args):
    # Inventory - voorraad
    if args.report_type == "inventory":
        # print de titel en de header van de tabel
        print("[bold green]INVENTORY[/bold green]")
        print("Product                         Aantal  Prijs   Expiration date")
        # voorraad zit in de file stock.csv
        with open('stock.csv', 'r') as stock_file:
            stock_reader = csv.DictReader(stock_file)
            rows_stock = list(stock_reader)
            # lijst per product
            # lijst voor de voorraad
            inventory = []
            count = 1
            for row in rows_stock:
                count = 1
                add_inventory = {'product_name': row["product_name"],'count': count,'buy_price': row["buy_price"],'expiration_date': row["expiration_date"]}
                if inventory == []:
                    inventory.append(add_inventory)
                else:
                    seek_row = 0
                    for i in inventory:
                        # zit product van de voorraad in de inventory lijst?
                        if (row['product_name'] == i["product_name"]) and (row["buy_price"] == i["buy_price"]) and (row["expiration_date"] == i["expiration_date"]):
                            count = int(inventory[seek_row]["count"]) + 1
                            product_found = True
                            break
                        else:
                            product_found = False
                            seek_row = seek_row + 1
                    if product_found:
                        # vind in inventory met index en wijzig count met 1 om hoog
                        inventory[seek_row]["count"] = str(count)
                    else:
                        inventory.append(add_inventory)
            # print de waardes van de tabel
            for i in inventory:
                print(f"[italic]{i["product_name"]}[/italic]\t\t\t\t{i["count"]}\t{i["buy_price"]}\t{i["expiration_date"]}")

            # data voor tabel voorbereiden
            table_data = [
                ['Product', 'Aantal', 'Prijs', 'Expiration date']
            ]
            new_dict = {}
            bar_new_dict = {}
            # data voor tabel en bar chart maken
            for i in inventory:
                temp_table_data = []
                temp_dict_data = {}
                bar_temp_table_data = []
                bar_temp_dict_data = {}

                temp_table_data.append(i["count"])
                temp_table_data.append(i["buy_price"])
                temp_table_data.append(i["expiration_date"])
                bar_temp_table_data.append(int(i["count"]))
                bar_temp_table_data.append(float(i["buy_price"]))

                temp_dict_data = new_dict | ({i["product_name"]: temp_table_data})
                bar_temp_dict_data = bar_new_dict | ({i["product_name"]: bar_temp_table_data})
                new_dict = temp_dict_data
                bar_new_dict = bar_temp_dict_data

            bar_data = []
            # data toevoegen voor alle producten in de voorraad
            for i in inventory:
                temp_list = [i["product_name"]] + temp_dict_data[i["product_name"]]
                bar_data.append(bar_temp_dict_data[i["product_name"]])
                table_data.append(temp_list)

            if args.export == True:
                # maak van de inventory een pdf file
                datum_tijd = datetime.strftime(datetime.now(),"%Y-%m-%d_%H%M%S")
                # unike naam door datum en tijd toe te voegen
                doc_filename = "Report-inventory_" + datum_tijd + ".pdf"
                # pagina setup
                doc = SimpleDocTemplate(doc_filename, pagesize=A4)
                styles = getSampleStyleSheet()
                title = Paragraph("Report inventory JW's Shop", styles['Title'])

                # stijl en font's bepalen van de tabel
                table = Table(table_data, style=[
                    ('GRID', (0,0),(-1,-1), 0.5, colors.grey),
                    ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold')
                ])

                # de chart voorbereiden, stijl en settings voor de assen
                chart = Drawing(400,200)

                bar_chart = VerticalBarChart()
                bar_chart.data = bar_data
                bar_chart.categoryAxis.categoryNames = ['Aantal', 'Prijs']
                bar_chart.valueAxis.valueMin = 0
                bar_chart.valueAxis.valueMax = max(max(x) * 1.1 for x in bar_chart.data)
                bar_chart.valueAxis.valueStep = max(max(x) / 5 for x in bar_chart.data)

                chart.add(bar_chart)
                # maak het document en schrijf het naar een pdf file
                doc.build([title, Spacer(0,12), table, chart])

                print("Voorraad in PDF file opgeslagen")
            # print de tabel in ene format gemaakt met Rich
            console = Console()
            table = tb(show_footer=False)
            table_centered = Align.center(table)

            console.clear()

            with Live(table_centered, console=console, screen=False):
                table.add_column("Product", no_wrap=True)
                table.add_column("Aantal", no_wrap=True)
                table.add_column("Prijs", no_wrap=True)
                table.add_column("Expiration date", no_wrap=True)
                for row in table_data:
                    table.add_row(*row)

                table.width = console.measure(table).maximum
                table.width = None

    # Revenue - omzet
    if args.report_type == "revenue":
        # eerst de dag uit datum.txt halen
        with open('datum.txt','r') as datum_file, open('sold.csv','r') as sold_file:
            # lees de datum die we opgeslagen hebben
            datum_from_file = datum_file.read()
            # lees de data uit sold.csv
            sold_reader = csv.DictReader(sold_file)
            rows_sold = list(sold_reader)
            # maak van de string(datum) een datum type
            datum_type_date = date.strptime(datum_from_file,"%Y-%m-%d")
            revenue = 0
            if args.today:
                reken_datum = datum_type_date
                # ga sold.csv door en tel alle verkoop prijzen op van de opgeslagen datum uit datum.txt
                for row in rows_sold:
                    if date.strptime(row["sell_date"],"%Y-%m-%d") == reken_datum:
                        revenue = revenue + float(row["sell_price"])
                # print de revenu - omzet
                print(f"De omzet van {reken_datum} is : {revenue}")


            if args.yesterday:
                # opgeslagen datum uit datum.txt met 1 dag verminderen.
                # ga sold.csv door en tel alle verkoop prijzen op
                reken_datum = datum_type_date + timedelta(days=-1) # gisteren is -1 dag tov vandaag
                # ga sold.csv door en tel alle verkoop prijzen op van de opgeslagen datum uit datum.txt
                for row in rows_sold:
                    if date.strptime(row["sell_date"],"%Y-%m-%d") == reken_datum:
                        revenue = revenue + float(row["sell_price"])
                # print de revenu - omzet
                print(f"De omzet van {reken_datum} is : {revenue}")

            if args.date:
                print(f"Omzet tonen van periode : {args.date}")
                # dan bepalen wat de reken periode is
                begin_reken_datum = date.strptime(args.date,"%Y-%m")
                volgende_maand = begin_reken_datum.replace(day=28) + timedelta(days=4)
                eind_reken_datum = volgende_maand - timedelta(days=volgende_maand.day)
                print(f"reken datum : van {begin_reken_datum} tot {eind_reken_datum}")
                # met reken periode door de sold database gaan en alle verkopen optellen
                for row in rows_sold:
                    if (date.strptime(row["sell_date"],"%Y-%m-%d") >= begin_reken_datum) and (date.strptime(row["sell_date"],"%Y-%m-%d") <= eind_reken_datum):
                        revenue = revenue + float(row["sell_price"])
                # print de revenu - omzet
                print(f"De omzet van {args.date} is : {revenue}")

    # Profit - winst
    if args.report_type == "profit":
        # eerst de dag uit datum.txt halen
        with open('datum.txt','r') as datum_file, open('sold.csv','r') as sold_file, open('bought.csv','r') as bought_file:
            # lees de datum die we opgeslagen hebben
            datum_from_file = datum_file.read()
            # lees de data uit sold.csv en bought.csv
            sold_reader = csv.DictReader(sold_file)
            rows_sold = list(sold_reader)
            bought_reader =csv.DictReader(bought_file)
            rows_bought = list(bought_reader)
            # maak van de string(datum) een datum type
            datum_type_date = date.strptime(datum_from_file,"%Y-%m-%d")
            profit = 0
            revenue = 0
            total_buy_price =0
            if args.today:
                reken_datum = datum_type_date
                # ga sold.csv door en tel alle verkoop prijzen op van de opgeslagen datum uit datum.txt
                for row_s in rows_sold:
                    if date.strptime(row_s["sell_date"],"%Y-%m-%d") == reken_datum:
                        revenue = revenue + float(row_s["sell_price"])
                        #print(f"verkoop prijs : {revenue}")
                        for row_b in rows_bought:
                            if row_s["bought_id"] == row_b["id"]:
                                total_buy_price = total_buy_price + float(row_b["buy_price"])
                                #print(f"aankoopprijs : {total_buy_price}")
                                break
                    profit = profit + (revenue - total_buy_price)
                    revenue = 0
                    total_buy_price =0
                    #print(f"winst : {profit}")
                # print de revenu - omzet
                print(f"De winst van {reken_datum} is : {round(profit,2)}")
        
            if args.yesterday:
                # opgeslagen datum uit datum.txt met 1 dag verminderen.
                # ga sold.csv door en tel alle verkoop prijzen op
                reken_datum = datum_type_date + timedelta(days=-1) # gisteren is -1 dag tov vandaag
                # ga sold.csv door en tel alle verkoop prijzen op van de opgeslagen datum uit datum.txt
                for row_s in rows_sold:
                    if date.strptime(row_s["sell_date"],"%Y-%m-%d") == reken_datum:
                        revenue = revenue + float(row_s["sell_price"])
                        for row_b in rows_bought:
                            if row_s["bought_id"] == row_b["id"]:
                                total_buy_price = total_buy_price + float(row_b["buy_price"])
                    profit = profit + (revenue - total_buy_price)
                    revenue = 0
                    total_buy_price =0
                # print de revenu - omzet
                print(f"De winst van {reken_datum} is : {round(profit,2)}")
        
            if args.date:
                print(f"Winst tonen van periode : {args.date}")
                # dan bepalen wat de reken periode is
                begin_reken_datum = date.strptime(args.date,"%Y-%m")
                volgende_maand = begin_reken_datum.replace(day=28) + timedelta(days=4)
                eind_reken_datum = volgende_maand - timedelta(days=volgende_maand.day)
                print(f"reken datum : van {begin_reken_datum} tot {eind_reken_datum}")
                # met reken periode door de sold database gaan en alle verkopen optellen
                for row_s in rows_sold:
                    if (date.strptime(row_s["sell_date"],"%Y-%m-%d") >= begin_reken_datum) and (date.strptime(row_s["sell_date"],"%Y-%m-%d") <= eind_reken_datum):
                        revenue = revenue + round(float(row_s["sell_price"]),2)
                        for row_b in rows_bought:
                            if row_s["bought_id"] == row_b["id"]:
                                total_buy_price = total_buy_price + round(float(row_b["buy_price"]),2)
                    profit = profit + (revenue - total_buy_price)
                    revenue = 0
                    total_buy_price =0
                # print de revenu - omzet
                print(f"De winst van {args.date} is : {round(profit,2)}")

    if args.report_type == "expired":
        print("Expired product's") 
        print("Product                         Aantal  Prijs   Expiration date")
        # voorraad zit in de file stock.csv
        with open('expired_products.csv', 'r') as expired_file:
            expired_reader = csv.DictReader(expired_file)
            rows_expired = list(expired_reader)
            # lijst per product
            # lijst voor de voorraad
            inventory = []
            count = 1
            for row in rows_expired:
                count = 1
                add_inventory = {'product_name': row["product_name"],'count': count,'buy_price': row["buy_price"],'expiration_date': row["expiration_date"]}
                if inventory == []:
                    inventory.append(add_inventory)
                else:
                    seek_row = 0
                    for i in inventory:
                        # zit product van de voorraad in de inventory lijst?
                        if (row['product_name'] == i["product_name"]) and (row["buy_price"] == i["buy_price"]) and (row["expiration_date"] == i["expiration_date"]):
                            count = int(inventory[seek_row]["count"]) + 1
                            product_found = True
                            break
                        else:
                            product_found = False
                            seek_row = seek_row + 1
                    if product_found:
                        # vind in inventory met index en wijzig count met 1 om hoog
                        inventory[seek_row]["count"] = str(count)
                    else:
                        inventory.append(add_inventory)
            for i in inventory:
                print(f"{i["product_name"]}\t\t\t\t{i["count"]}\t{i["buy_price"]}\t{i["expiration_date"]}")

    return