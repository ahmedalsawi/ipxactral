import xml.etree.ElementTree as ET
import json

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

    def parse(self):
        tree = ET.parse(self.filename)
        self.xmlroot = tree.getroot()
        self.json = node_to_dict(self.xmlroot)

    def dump_jsonify(self,jsonfile):
        with open(jsonfile, 'w') as outfile:
            json.dump(self.json, outfile,indent=2)
