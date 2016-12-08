#!/usr/bin/env python
#
#     check_result.py
#
# crappy script to check offsets after corresting errors
#
# usage:
#   $ python check_result.py ../../data/files/jsondump/ocred_texts/Rajab.json \
#   $                        ../../data/files/errorsfixed/ocred_texts/Rajab.json 0 motives 0
#
############################################################################################

import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('before_file', type=argparse.FileType('r'))
parser.add_argument('after_file', type=argparse.FileType('r'))
parser.add_argument('index_error', type=int)
parser.add_argument('layer_annot')
parser.add_argument('index_annot', type=int)
args = parser.parse_args()

before = json.load(args.before_file)
after  = json.load(args.after_file)

# index for error
i = args.index_error

# type of annotation
label = args.layer_annot
# index for annotation
j = args.index_annot


print('>> ERROR :: Info error:', before['errors'][i])
print()
print('ERROR BEFOR :: Slice in text:', before['content'][before['errors'][i]['ini'] : before['errors'][i]['end']])
print('ERROR BEFOR :: Slice in text +- 10 chars:', before['content'][before['errors'][i]['ini']-10 : before['errors'][i]['end']+10])
print()
print('ERROR AFTER :: Slice in after text:', after['content'][after['errors'][i]['ini'] : after['errors'][i]['end']])
print('ERROR AFTER :: Slice in after text +- 10 chars:', after['content'][after['errors'][i]['ini']-10 : after['errors'][i]['end']+10])

print('\n=====================\n')

print('>> ANNOT :: Info annot:', before[label][j])
print()
print('ANNOT BEFOR :: Slice in text:', before['content'][before[label][j]['ini'] : before[label][j]['end']])
print('ANNOT BEFOR :: Slice in text +- 10 chars:', before['content'][before[label][j]['ini']-10 : before[label][j]['end']+10])
print()
print('ANNOT AFTER :: Slice in text:', after['content'][after[label][j]['ini'] : after[label][j]['end']])
print('ANNOT AFTER :: Slice in text +- 10 chars:', after['content'][after[label][j]['ini']-10 : after[label][j]['end']+10])

