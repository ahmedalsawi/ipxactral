import xml.etree.ElementTree as ET
import json

import os
import sys
import datetime
import tempfile
from pathlib import Path

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


class Ipxact(object):
    def __init__(self, filename, templatedir, outdir):
        self.filename = filename
        self.outdir = outdir
        self.templatedir = templatedir

        self.xmlroot = None

        # Create output directory if not there already
        Path(self.outdir).mkdir(parents=True, exist_ok=True)

        # TODO check directory exists
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.templatedir)
        )

    def parse(self):
        tree = ET.parse(self.filename)
        self.xmlroot = tree.getroot()

    def jsonify(self):
        self.json = node_to_dict(self.xmlroot)
        jsonfile = os.path.join(self.outdir, "data.json")
        with open(jsonfile, "w") as outfile:
            json.dump(self.json, outfile, indent=2)

    def build_context(self):
        self.context = {}
        self.context["date"] = datetime.datetime.now(datetime.timezone.utc)

    def generate(self):
        filenames = [
            "README.md",
        ]
        for filen in filenames:
            template = self.jinja_env.get_template(filen + ".jinja")
            txt = template.render(context=self.context)
            with open(os.path.join(self.outdir, filen), "w") as outfile:
                outfile.write(txt)

    def run(self):
        self.parse()
        self.jsonify()
        self.build_context()
        self.generate()
