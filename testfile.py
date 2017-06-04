import argparse

parser=argparse.ArgumentParser()
# parser.add_argument("name")
# parser.add_argument("date")
# args = parser.parse_args()
# print(args)

subparsers=parser.add_subparsers(dest="command",help="list of commands")

get_parser=subparsers.add_parser("get", help ="")
get_parser.add_argument("name",help= "returns the date")
get_args=parser.parse_args()
get_args=vars(get_args)
print(get_args)

