import xml.etree.ElementTree as ET
import json

import os
import sys
import datetime
import tempfile
from pathlib import Path
import logging

import jinja2

from ipxactral import config

ns = {"ipxact": "http://www.accellera.org/XMLSchema/IPXACT/1685-2014"}


def node_to_dict(node):
    data = {}
    data["tag"] = node.tag

    text = node.text
    if text:
        text = text.strip()
    if text == "":
        text = None
    data["text"] = text

    data["attrib"] = node.attrib
    data["children"] = [node_to_dict(c) for c in node]
    return data


def find_first(start, tag):
    for child in start:
        if tag in child.tag:
            return child
        else:
            find_first(child, tag)


def access2short(access):
    return "R" if access == "read-only" else "RW"


class Ipxact(object):
    def __init__(self, filename, templatedir, outdir):
        self.filename = filename
        self.outdir = outdir
        self.templatedir = templatedir

        self.xmlroot = None
        self.treeDict = {}

        # Create output directory if not there already
        Path(self.outdir).mkdir(parents=True, exist_ok=True)

        # TODO check directory exists
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.templatedir)
        )

    def parse(self):
        tree = ET.parse(self.filename)
        self.xmlroot = tree.getroot()

    def jsonify(self, filename="data.json"):
        self.treeDict = node_to_dict(self.xmlroot)
        jsonfile = os.path.join(self.outdir, filename)
        with open(jsonfile, "w") as outfile:
            json.dump(self.treeDict, outfile, indent=2)

    def build_memorymaps(self):
        # Extract MemoryMaps
        mmaps = find_first(self.xmlroot, "memoryMaps")
        if mmaps is None:
            logging.warning("No MemoryMaps found in IPXACT file.")
            return

        for mmap in mmaps.findall("ipxact:memoryMap", ns):
            mmap_context = {}
            mmap_context["name"] = mmap.find("ipxact:name", ns).text
            mmap_context["addressUnitBits"] = mmap.find(
                "ipxact:addressUnitBits", ns
            ).text
            for addressBlock in mmap.findall("ipxact:addressBlock", ns):
                block_context = {}
                block_context["name"] = addressBlock.find("ipxact:name", ns).text
                block_context["baseAddress"] = addressBlock.find(
                    "ipxact:baseAddress", ns
                ).text
                block_context["range"] = addressBlock.find("ipxact:range", ns).text
                block_context["width"] = addressBlock.find("ipxact:width", ns).text
                block_context["access"] = access2short(
                    addressBlock.find("ipxact:access", ns).text
                )
                block_context["registers"] = []
                for reg in addressBlock.findall("ipxact:register", ns):
                    reg_context = {}
                    block_context["registers"].append(reg_context)
                    reg_context["name"] = reg.find("ipxact:name", ns).text
                    reg_context["size"] = reg.find("ipxact:size", ns).text
                    reg_context["addressOffset"] = reg.find(
                        "ipxact:addressOffset", ns
                    ).text
                    reg_context["fields"] = []
                    for field in reg.findall("ipxact:field", ns):
                        field_context = {}
                        reg_context["fields"].append(field_context)
                        field_context["name"] = field.find("ipxact:name", ns).text
                        field_context["description"] = field.find(
                            "ipxact:description", ns
                        ).text
                        field_context["bitOffset"] = field.find(
                            "ipxact:bitOffset", ns
                        ).text
                        field_context["bitWidth"] = field.find(
                            "ipxact:bitWidth", ns
                        ).text
                        field_context["access"] = access2short(
                            field.find("ipxact:access", ns).text
                        )
                        field_context["reset"] = (
                            field.find("ipxact:resets", ns)
                            .find("ipxact:reset", ns)
                            .find("ipxact:value", ns)
                            .text
                        )
                    reg_template = self.jinja_env.get_template("reg.sv.jinja")
                    txt = reg_template.render(context=reg_context)
                    print(txt)
                block_template = self.jinja_env.get_template("reg_block.sv.jinja")
                txt = block_template.render(context=block_context)
                print(txt)

    def build_context(self):
        self.context = {}
        self.context["date"] = datetime.datetime.now(datetime.timezone.utc)

        self.build_memorymaps()

    def generate(self):
        filenames = ["README.md.jinja"]
        for filen in filenames:
            template = self.jinja_env.get_template(filen)
            txt = template.render(context=self.context)
            with open(os.path.join(self.outdir, filen[:-6]), "w") as outfile:
                outfile.write(txt)

    def run(self):
        self.parse()
        self.jsonify()
        self.build_context()
        self.generate()
