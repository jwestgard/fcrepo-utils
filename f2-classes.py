#!/usr/bin/env python3
import argparse
import csv
import requests
import sys
from time import sleep
import xml.etree.ElementTree as ET


#= Class ====================
# Class for any Fedora object
#============================
class fedora_object(object):
    
    def __init__(self, pid):
        print("Created {0} object called {1}.".format(self.type, self.name))


#= Class =====================
# Class for Fedora UMDM object
#=============================
class umdm(fedora_object):
    def __init__(self):
        

#= Class =====================
# Class for Fedora UMAM object
#=============================
class umam(fedora_object):
    def __init__(self):
        






def main():
    pass
    

if __name__ == "__main__":
    main()
