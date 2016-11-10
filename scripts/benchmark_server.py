#!/usr/bin/python

from __future__ import print_function

import os.path as op
import requests
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="""

    Usage:

    cp api/db.sqlite3 api/db.sqlite3.bak
    wget https://s3.amazonaws.com/pkerp/public/db.sqlite3
    mv db.sqlite3 api
    
    python benchmark_server.py url path tileset-id [tile_ids]
""")

    parser.add_argument('url')
    parser.add_argument('tileset_id')
    parser.add_argument('tile_ids', nargs='*')
    parser.add_argument('--tile-id-file')
    parser.add_argument('--iterations')
    #parser.add_argument('-o', '--options', default='yo',
    #					 help="Some option", type='str')
    #parser.add_argument('-u', '--useless', action='store_true', 
    #					 help='Another useless option')
    args = parser.parse_args()

    # parse requests on the command line
    for tile_id in args.tile_ids:
        get_url = op.join(args.url, 'tilesets/x/render/?d=' + args.tileset_id + '.' + tile_id)

        r = requests.get(get_url)
        print("r:", r)
    
    # parse requests from a file
    if args.tile_id_file is not None:
        with open(args.tile_id_file, 'r') as f:
            for line in f:
                get_url = op.join(args.url, 'tilesets/x/render/?d=' + args.tileset_id + '.' + line.strip())

                r = requests.get(get_url)
                print("r:", r)

    

if __name__ == '__main__':
    main()


