#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Ed Mountjoy
#
# Efficiently extract phenotype data from UKBB files
#

import sys
import argparse
import pandas as pd

def main():

    # Args
    args = parse_arguments()

    print('Load list of required variables')
    reqvars = load_file_to_list(args.req, 0, args.sep)

    print('Check required variales are in data files')
    check_variables_available(reqvars, args.indata, args.sep)

    print('Extract required variables from each dataset separately')
    reqdata = []
    for infile in args.indata:
        # Find names of columns to extract
        reqcols = find_col_names(reqvars, infile, args.sep)
        # Load data using pandas
        df = pd.read_csv(infile, sep=args.sep, index_col=0, usecols=reqcols,
                         header=0, dtype=str)
        reqdata.append(df)

    print('Concatenate into a single data frame')
    outdf = pd.concat(reqdata, axis=1)
    # Order columns based on input list
    colorder = sorted(list(outdf.columns),
                      key=lambda col: reqvars.index(col.split(".")[1]))
    outdf = outdf.loc[:, colorder]

    print('Link projectID to geneticID')
    outdf.insert(0, "projectID", outdf.index)
    if args.link:
        # Load linker IDs to dictionary
        mapdf = pd.read_csv(args.link, sep=",", header=0)
        mapdict = dict(zip(mapdf.iloc[:, 0], mapdf.iloc[:, 1]))
        # Make genetic ID list
        genID = [mapdict.get(projID, "NA") for projID in outdf["projectID"]]
        # Add genetic IDs
        outdf.insert(1, "geneticID", genID)

    # Write output
    outdf.to_csv(args.out, sep=args.sep, na_rep="NA", index=False)

    return 0

def find_col_names(reqvars, indata, sep="\t"):
    """ Returns list of column names that need extracting.
    """
    # Covert req to set
    reqset = set(reqvars)
    # Load header
    header = load_header(indata, sep)
    # Get list of required colnames
    reqcols = [header[0]]
    for col in header[1:]:
        if col.split(".")[1] in reqset:
            reqcols.append(col)
    return reqcols

def check_variables_available(reqvars, indata, sep="\t", quit=True):
    """ Checks that all required variables are available in data.
        If quit == True, then quit if any variables are missing.
    """
    # Load available variables from data sets
    availvars = set([])
    for infile in indata:
        header = load_header(infile, sep)
        for col in header[1:]:
            var = col.split(".")[1]
            availvars.add(var)
    # Check required vars are availabe
    notpresent = []
    for reqvar in reqvars:
        if not reqvar in availvars:
            notpresent.append(reqvar)
    # Quit if any variables not present
    if len(notpresent) > 0:
        print("Error: Variables not present in datasets:")
        for var in notpresent:
            print(" {0}".format(var))
        if quit:
            sys.exit("Exiting!")

    return 0

def load_header(infile, sep="\t"):
    """ Loads header from file
    """
    with open(infile, "r") as in_h:
        header = in_h.readline().rstrip().split(sep)
        return header

def load_file_to_list(infile, col=0, sep="\t"):
    """ Loads a file to a list
    """
    l = []
    with open(infile, "r") as in_h:
        for line in in_h:
            l.append(line.rstrip().split(sep)[col])
    return l

def parse_arguments():
    """ Parses command line arguments.
    """
    # Create top level parser.
    parser = argparse.ArgumentParser(description="Extract data from UKBB.")

    # Add options
    parser.add_argument('--indata', metavar="<file>",
        help=('Input data files'),
        required=True,
        nargs="+",
        type=str)
    parser.add_argument('--req', metavar="<file>",
        help=('File containing list of required variables'),
        required=True,
        type=str)
    parser.add_argument('--out', metavar="<file>",
        help=('Output file name including extension'),
        required=True,
        type=str)
    parser.add_argument('--link', metavar="<file>",
        help=('Link file for project ID -> genetic ID conversion'),
        required=False,
        type=str)
    parser.add_argument('--sep', metavar="<str>",
        help=('Column separator (default: tab)'),
        default='\t',
        type=str)

    # Parse the arguments
    args = parser.parse_args()

    # Parse the arguments
    return args

if __name__ == '__main__':

    main()
