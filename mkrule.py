import math
import argparse
import ipaddress


def split_range(ipv4_str, count):
    ipv4 = ipaddress.IPv4Address(ipv4_str)
    numerical = int(ipv4)
    ranges = []
    while count > 0:
        max_range = math.floor(math.log2(count))
        right_most_1 = int(math.log2(numerical & -numerical))
        c = min(max_range, right_most_1)

        mask = 32 - c
        ranges.append(f'{ipv4}/{mask}')
        ipv4 += 2**c
        count -= 2 ** c
    return ranges


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--country', required=True)
parser.add_argument('-f', '--file', required=True)
parser.add_argument('-t', '--table', default='filter')
parser.add_argument('-p', '--family', default='inet')
args = parser.parse_args()

country = args.country

ip4set = []
ip6set = []

print(f'add set {args.family} {args.table} IP4SET_{country} {{ type ipv4_addr; flags constant, interval; }}')
print(f'add set {args.family} {args.table} IP6SET_{country} {{ type ipv6_addr; flags constant, interval; }}')

with open(args.file, 'rt') as f:
    for line in f.readlines():
        cols = line.strip().split('|')

        if len(cols) > 1 and cols[1] == country:
            protocol = cols[2]
            if protocol == 'ipv4':
                addr, count = cols[3], int(cols[4])
                ranges = split_range(addr, count)
                ip4set.extend(ranges)

            elif protocol == 'ipv6':
                addr = cols[3]
                mask = int(cols[4])
                iprange = f'{addr}/{mask}'
                ip6set.append(iprange)

if len(ip4set):
    print(f'add element {args.family} {args.table} IP4SET_{country} {{ {", ".join(ip4set)} }}')
if len(ip6set):
    print(f'add element {args.family} {args.table} IP6SET_{country} {{ {", ".join(ip6set)} }}')
