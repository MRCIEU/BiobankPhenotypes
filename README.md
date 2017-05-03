# BiobankPhenotypes

Phenotype submission - https://github.com/MRCIEU/BiobankPhenotypes/wiki

Pipeline code -  https://github.com/MRCIEU/BiobankGWAS

Phenotype creation:

UK Biobank Pheno Extractor
===================

Extract required variables from UK Biobank R files without loading everything to memory. Still requires that there is enough RAM to fit extracted variables in.

## Requires
- Python 2.7
- Pandas (Python module)

## Run

```
usage: extractUKBBpheno_v0.2.py [-h] --indata <file> [<file> ...] --req <file>
                                --out <file> [--sep <str>]

Extract data from UKBB.

arguments:
  -h, --help            show this help message and exit
  --indata <file> [<file> ...]
                        Input data files
  --req <file>          File containing list of required variables
  --out <file>          Output file name including extension
  --link <file>         Link file for project ID -> genetic ID conversion
  --sep <str>           Column separator (default: tab)
```

### In data files
Input data must be tab file from the `.../data/derived/format/r/` directory. Multiple tab files can be provided and variables will be merged using column 1 (eid) as an index.

### Link file
Comma separated file with header on first line. Column 1 is your project specific ID, column 2 is the genetic IDs.

### Required variables list
Is a file where the first column is a list of variable IDs that are needed. IDs are the same as those in the Data Showcase.

### Example
`required_variables.txt`:

```
21
34
6141
2385
2395
3062
```

Script:

```
#!/usr/bin/env bash
#

datadir=/path/to/data/derived/format/r

python extractUKBBpheno_v0.1.py \
  --indata $datadir/data.4263.tab $datadir/data.4894.tab $datadir/data.5013.tab \
  --link linker_file.csv
  --req required_variables.txt \
  --out output_extracted_variables.tsv
```
