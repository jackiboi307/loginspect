#!/bin/python

import argparse
import tomllib
import sys
import re

RESET = '\x1b[0m'
UNDERLINE = '\x1b[4m'
BOLD = '\x1b[1m'
FG_ID = '\x1b[38;5;{}m'
FG_YELLOW_B = '\x1b[93m'
IP_COLORS = [197, 201, 67, 77, 121, 221, 208]
ALLOWED_STATUS = [200, 302]

pat = re.compile(
    r"(\d+\.\d+\.\d+\.\d+) - - \[([^]]*)\] \"(\S*) (.*) HTTP.* (\d+) -",
)

ips = {}
color_i = 0
last_day = ""

with open("config.toml", "rb") as file:
    conf = tomllib.load(file)
    excl_ips = conf["excluded_ips"]

parser = argparse.ArgumentParser(
    color=False,
    prog='loginspect')
parser.add_argument("--filter", metavar="IP", help="filter by ip address")
parser.add_argument("--min", type=int, default=1, metavar="AMOUNT",
    help="minimum occurences")
parser.add_argument("--method", choices=["GET", "POST"], help="filter by method")
args = parser.parse_args()

while True:
    try:
        inp = input()
        if match := pat.match(inp):
            ip, date, method, uri, status = match.groups()
            day, time = date.split()

            excl = False
            for excluded in excl_ips:
                if ip == excluded or \
                        excluded.endswith("*") and ip.startswith(excluded[:-1]):
                    excl = True
                    break

            if not excl and int(status) in ALLOWED_STATUS and \
                    (not args.method or method.endswith(args.method)):

                if not args.filter or ip == args.filter:
                    if day != last_day:
                        if last_day != "":
                            print()
                        print(f"{BOLD}[{day}]{RESET}")
                    last_day = day

                if ip not in ips:
                    ips[ip] = [1, FG_ID.format(IP_COLORS[color_i])]
                    color_i = (color_i + 1) % len(IP_COLORS)
                else:
                    ips[ip][0] += 1
                
                if not args.filter or args.filter == ip:
                    print(f"{ips[ip][1]}{ip:15}{RESET}  {time}  \
{FG_YELLOW_B}{uri}{RESET}")

    except EOFError:
        break

if not args.filter:
    print(f"\n{UNDERLINE}ip address{RESET}       {UNDERLINE}occurences{RESET}")
    for ip, occ_col in sorted(ips.items(), key=lambda x: x[1][0], reverse=True):
        occurences, color = occ_col
        if args.min <= occurences:
            print(f"{color}{ip:15}{RESET}  {occurences}")

