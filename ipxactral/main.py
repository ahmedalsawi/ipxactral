

def main():
    import argparse
    import os
    
    from ipxactral import ipxact

    parser = argparse.ArgumentParser(description='ipxact parser and generator')

    parser.add_argument('ipxactfile')
    parser.add_argument('--json', nargs='?', help='Generate json')

    args = parser.parse_args()

    o = ipxact.Ipxact(args.ipxactfile)
    o.parse()

    if args.json:
        o.dump_jsonify(args.json)
