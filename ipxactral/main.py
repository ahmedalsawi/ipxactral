def main():
    import argparse
    import os

    from ipxactral import ipxact
    from ipxactral import config

    # Command line parser
    parser = argparse.ArgumentParser(description="ipxact parser and generator")

    parser.add_argument("ipxactfile")
    parser.add_argument(
        "--outdir", nargs="?", help="Path for output directory", required=True
    )
    parser.add_argument(
        "--templatedir", nargs="?", help="Path for templates", required=True
    )
    args = parser.parse_args()

    # Create ipxact per file
    ipxactObj = ipxact.Ipxact(args.ipxactfile, args.templatedir, args.outdir)

    ipxactObj.run()
