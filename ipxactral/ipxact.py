import xml.etree.ElementTree as ET

import json

class Ipxact(object):
    def __init__(self,filename):
        self.filename = filename

    def parse(self):
        tree = ET.parse(self.filename)
        self.root = tree.getroot()
        self.Santize()

    def rSantize(self, node):
        """
        Remove spaces and newlines from element text
        """
        if node.text:
            node.text = node.text.strip()
        if node.text == "":
            node.text = None

        for child in node:
            self.rSantize(child)

    def Santize(self):
        self.rSantize(self.root)

    def json(self):
        pass
