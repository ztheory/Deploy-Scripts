#! /usr/bin/env python
#
# Copyright (c) 2012 OpenDNS, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the OpenDNS nor the names of its contributors may be
#      used to endorse or promote products derived from this software without
#      specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL OPENDNS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

""" Module for encoding/decoding LabTech XML files """

__author__ = 'bhartvigsen@opendns.com (Brian Hartvigsen)'
__copyright__ = 'Copyright (c) 2013 OpenDNS, Inc.'
__version__ = '1.0.0'

import sys
import os
import gzip
from StringIO import StringIO
from base64 import b64decode, b64encode
from xml.dom.minidom import parse, parseString


class LabTechXml(object):
    def __init__(self, filename):
        self.__dom = parse(filename)
        self.__scriptData = self.__dom.getElementsByTagName("ScriptData")[0]
        self.__licenseData = self.__dom.getElementsByTagName("LicenseData")[0]
        self.__files = self.__dom.getElementsByTagName("File")

        if len(self.__scriptData.childNodes) > 1 and len(self.__licenseData.childNodes) > 1:
            self.__input_path = self.__get_dir(filename)
            self.__encoded = False
        elif len(self.__scriptData.childNodes) == 1 and len(self.__licenseData.childNodes) == 1:
            self.__encoded = True
        else:
            raise Exception('This is not a valid LabTech XML file')

    @staticmethod
    def __get_dir(path):
        path = os.path.dirname(path)
        if path is None or path == "":
            path = os.getcwd()

        return path

    @staticmethod
    def __check_dir(path):
        if not os.path.isdir(path):
            if not os.path.exists(path):
                os.makedirs(path)
            else:
                raise Exception("%s is not a directory!" % path)

    @staticmethod
    def __deflate(data):
        compressed = StringIO()
        with gzip.GzipFile(mode='wb', fileobj=compressed) as fp:
            fp.write(data)

        compressed.seek(0)
        return b64encode(compressed.read())

    @staticmethod
    def __inflate(data):
        compressed = StringIO(b64decode(data))
        with gzip.GzipFile(mode='rb', fileobj=compressed) as fp:
            return fp.read()

    def process(self, output):
        self.__output_path = self.__get_dir(output)
        self.__check_dir(self.__output_path)

        if self.__encoded:
            self.__decode(output)
        else:
            self.__encode(output)

    def __encodeNode(self, name, previousNode):
        node = self.__dom.createElement(name)
        node.appendChild(self.__dom.createTextNode(self.__deflate(previousNode.toxml().replace("\n", "\r\n"))))
        previousNode.parentNode.replaceChild(node, previousNode)

    def __encodeFiles(self):
        for f in self.__files:
            name = f.getAttribute("Name").split("\\")
            name[0] = self.__input_path
            name = os.sep.join(name)
            if os.path.isfile(name):
                with open(name, "r") as fp:
                    data = fp.read()
                    f.setAttribute("Bytes", b64encode(data))
            else:
                raise Exception("%s does not exist!", name)

    def __encode(self, output):
        self.__encodeNode("ScriptData", self.__scriptData)
        self.__encodeNode("LicenseData", self.__licenseData)
        self.__encodeFiles()

        with open(output, "w") as fp:
            fp.write(self.__dom.toxml())

    def __decodeNode(self, node):
        data = parseString(self.__inflate(node.firstChild.data))
        node.parentNode.replaceChild(data.firstChild, node)

    def __decodeFiles(self):
        for f in self.__files:
            data = f.getAttribute("Bytes")
            name = f.getAttribute("Name").split("\\")
            name[0] = self.__output_path
            name = os.sep.join(name)
            f.removeAttribute("Bytes")

            self.__check_dir(os.path.dirname(name))

            with open(name, "w") as fp:
                fp.write(b64decode(data))

    def __decode(self, output):
        self.__decodeNode(self.__scriptData)
        self.__decodeNode(self.__licenseData)
        self.__decodeFiles()

        with open(output, "w") as fp:
            fp.write(self.__dom.toxml())


def main():
    def usage():
        print "%s [input] [output]" % sys.argv[0]

    if len(sys.argv) != 3:
        usage()
        sys.exit(-1)

    if not os.path.isfile(os.path.expanduser(sys.argv[1])):
        usage()
        sys.exit(-1)

    xml = LabTechXml(os.path.expanduser(sys.argv[1]))
    xml.process(sys.argv[2])

if __name__ == '__main__':
    main()
