#!/usr/bin/env python3

'''Given a Fedora-provided turtle file listing contained resources, read the 
   list of URIs, query Fedora for RDF metadata, and use that metadata to 
   determine the type of object, recording resource number, URI, and type in 
   an output CSV file.  Supports resuming with an existing output file. 
   
   USAGE: ./list_contained_resources.py INPUT OUTPUT'''

import csv
import os
import sys
import rdflib
import requests

INFILE = sys.argv[1]
OUTFILE = sys.argv[2]

def get_contained_resources(rdffile):
    '''parse rdf document and return list of ldp:contains uris'''
    predicate = rdflib.URIRef('http://www.w3.org/ns/ldp#contains')
    print('Parsing input from {0}... '.format(rdffile), end='')
    source = rdflib.graph.Graph().parse(rdffile, format='text/turtle')
    result = [str(uri) for uri in source.objects(predicate=predicate)]
    print('{0} uris found.'.format(len(result)))
    return result

def get_completed_items(csvfile):
    '''return list of uris already checked from CSV summary file'''
    print('Reading existing output file {0}... '.format(csvfile), end='')
    with open(csvfile, 'rt') as f:
        reader = csv.reader(f)
        uris = [row[1] for row in reader]
    print('{0} files already checked.'.format(len(uris)))
    return uris

def get_resource_type(uri):
    '''determine repository resource type based on rdftype predicates'''
    predicate = rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
    print("Checking {0} => ".format(uri), end='')
    head_response = requests.head(uri)
    if 'describedby' in head_response.links:
        type = 'file'
    else:
        response = requests.get(uri)
        g = rdflib.graph.Graph().parse(data=response.text, format='text/turtle')
        typeset = [str(obj) for obj in g.objects(predicate=predicate)]
        if 'http://purl.org/ontology/bibo/Article' in typeset:
            type = 'article'
        elif 'http://purl.org/ontology/bibo/Issue' in typeset:
            type = 'issue'
        elif 'http://www.openarchives.org/ore/terms/Proxy' in typeset:
            type = 'proxy'
        elif 'http://chroniclingamerica.loc.gov/terms/Page' in typeset:
            type = 'page'
        elif 'http://purl.org/spar/fabio/Metadata' in typeset:
            type = 'metadata'
        else:
            type = 'unknown'
    print(type)
    return type

def main():
    '''get set of all uris minus already checked, get type, write to output'''
    all_uris = set(get_contained_resources(INFILE))
    if os.path.exists(OUTFILE):
        complete = set(get_completed_items(OUTFILE))
    else:
        complete = set()
    to_check = all_uris - complete
    counter = len(complete) + 1
    with open(OUTFILE, 'at') as f:
        writer = csv.writer(f, lineterminator='\n')
        for uri in to_check:
            type = get_resource_type(uri)
            writer.writerow([counter, uri, type])
            f.flush()
            counter += 1

if __name__ == "__main__":
    main()
