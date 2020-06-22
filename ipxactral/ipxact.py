import xml.etree.ElementTree as ET
import json

import os
import sys
import tempfile

import jinja2

def node_to_dict(node):
    data = {}
    data['tag'] = node.tag

    text = node.text
    if text:
        text = text.strip()
    if text == "":
        text = None
    data['text'] = text

    data['attrib']= node.attrib
    data['children'] = [node_to_dict(c) for c in node]
    return data

class Ipxact(object):
    def __init__(self,filename):
        self.filename = filename
        self.xmlroot = None

        ## FIXME init the tempalate correctly
        self.TEMPLATE_PATH = "templates"
        self.jinja_env  = jinja2.Environment(loader=jinja2.FileSystemLoader(self.TEMPLATE_PATH))

    def parse(self):
        tree = ET.parse(self.filename)
        self.xmlroot = tree.getroot()
        self.json = node_to_dict(self.xmlroot)

    def dump_jsonify(self,jsonfile):
        with open(jsonfile, 'w') as outfile:
            json.dump(self.json, outfile,indent=2)

    def generate(self ):
        template= self.jinja_env.get_template('ral.sv.jinja')
        txt = template.render(root="fff")
        print(txt)
