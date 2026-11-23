# Imports
from argparse import *
import csv
from datetime import *
from report_functions import *
from time_functions import *
from sales_functions import *

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

parser = ArgumentParser(description="Supermarkt CLI tool")
parser.add_argument("--set_time", type=str, help="specify what date today is")
parser.add_argument("--advance_time",type=int, help="number of days to advance the date")
parser.add_argument("--check_expired", action="store_true", help="check if there are expired products in stock and delete them from stock")
subparsers = parser.add_subparsers(dest="command")

# define parsers
# create buy parser
buy_parser = subparsers.add_parser("buy", help="Used to buy a product (--product_name, --price, --expiration_date, --quantity)")
buy_parser.add_argument("--product_name", type=str, help="specify the product you buy")
buy_parser.add_argument("--price", type=float, help="specify the price of the product")
buy_parser.add_argument("--expiration_date", type=str, help="expiration date of the product")
buy_parser.add_argument("--quantity", type= int, default=1, help="How many of the product you buy")

# create sell parser
sell_parser = subparsers.add_parser("sell", help="Used to sell a product (--product_name, --price)")
sell_parser.add_argument("--product_name", type=str, help="specify the product you buy")
sell_parser.add_argument("--price", type=float, help="specify the price of the product")

# create report parser
report_parser = subparsers.add_parser("report", help="Used to report your inventory, revenue or profit (--today, --yesterday, --date yyyy-mm)")
report_parser.add_argument("report_type", type=str, help="Specify what you want to report")
report_parser.add_argument("--today","--now", action="store_true")
report_parser.add_argument("--yesterday", action="store_true")
report_parser.add_argument("--date", type=str, help="Specify the month and year, use format yyyy-mm")
report_parser.add_argument("--export", action="store_true", help="Export you report to pdf file")

# Your code below this line.
def main():
    args = parser.parse_args()

    # save current date in a file if not already set
    save_date()

    # which command is given
    if args.command == "buy":
        buy(args)
    if args.command == "sell":
        sell(args)
    if args.command == "report":
        report(args)
    if args.advance_time != None:
        verzet_tijd(args)
    if args.set_time != None:
        specify_time(args)
    if args.check_expired != False:
        # check if the are products who are expired and delete them from the stock
        expired()


if __name__ == "__main__":
    main()
