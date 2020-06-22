

def main():
    import argparse
    import os
    
    from ipxactral import ipxact

    parser = argparse.ArgumentParser(description='ipxact parser and generator')

    parser.add_argument('ipxactfile')

    args = parser.parse_args()

    o = ipxact.Ipxact(args.ipxactfile)
    o.parse()
