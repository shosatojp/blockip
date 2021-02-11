import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--country', required=True)
parser.add_argument('-f', '--file', required=True)
args = parser.parse_args()

country = args.country

with open(args.file, 'rt') as f:
    for line in f.readlines():
        cols = line.strip().split('|')

        if len(cols) > 1 and cols[1] == country:
            protocol = cols[2]
            if protocol == 'ipv4':
                addr = cols[3]
                mask = 32 - int(math.log2(int(cols[4])))
                iprange = f'{addr}/{mask}'
                print(f'nft add rule inet filter BLOCK ip saddr {iprange} log prefix "BLOCK {country}: " drop')

            elif protocol == 'ipv6':
                addr = cols[3]
                mask = int(cols[4])
                iprange = f'{addr}/{mask}'

                print(f'nft add rule inet filter BLOCK ip6 saddr {iprange} log prefix "BLOCK {country}: " drop')
