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
        mmaps_node = find_first(self.xmlroot, "memoryMaps")
        if mmaps_node is None:
            logging.warning("No MemoryMaps found in IPXACT file.")
            return
        print(mmaps_node.tag)

    def build_context(self):
        self.context = {}
        self.context["date"] = datetime.datetime.now(datetime.timezone.utc)

        self.build_memorymaps()

    def generate(self):
        filenames = ["README.md.jinja"]
        # for file in os.listdir(self.templatedir):
        #     if file.endswith(".jinja"):
        #         filenames.append(file)
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
