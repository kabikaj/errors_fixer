#!/usr/bin/env python
#
#     errorfixer.py
#
# fix errors in Cobhuni text corpus and adjust offsets accordingly
#
# example:
#   $ python errorfixer.py ../../data/files/jsondump/ocred_texts/ \
#   $                      ../../data/files/errorsfixed/ocred_texts/
#
#####################################################################

import os
import sys
import json
import argparse
import operator
import configparser

#
# constants
#

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

CONFIG = configparser.ConfigParser(inline_comment_prefixes=('#'))

try:
    CONFIG.read(os.path.join(DIR_PATH, 'config.ini'))
except configparser.MissingSectionHeaderError:
    print('Error in process {__file__}: no sections in config file'.format(**globals()), file=sys.stderr)
    sys.exit(1)

if not CONFIG.sections():
    print('Error in process {__file__}: config file missing or empty'.format(**globals()), file=sys.stderr)
    sys.exit(1)

try:
    TEXT = CONFIG.get('doc attribs', 'text')
    ERRORS = CONFIG.get('doc attribs', 'errors')
    PERSONS = CONFIG.get('doc attribs', 'persons')
    MOTIVES = CONFIG.get('doc attribs', 'motives')
    METAMOTIVES = CONFIG.get('doc attribs', 'metamotives')
    VALUE = CONFIG.get('annotation attribs', 'value')
    START = CONFIG.get('annotation attribs', 'start')
    END = CONFIG.get('annotation attribs', 'end')
except (configparser.NoSectionError, configparser.NoOptionError) as err:
    print('Error in process {__file__}: invalid information. {err}'.format(**globals()), file=sys.stderr)
    sys.exit(1)    

#
# main
#

if __name__ == '__main__':    

    # parse args
    parser = argparse.ArgumentParser(description='fix errors in Cobhuni text corpus and adjust offsets')
    parser.add_argument('input_dir', help='path containing json input files')
    parser.add_argument('output_dir', help='path to save json output files')
    args = parser.parse_args()

    files = ((f.path, f.name) for f in os.scandir(args.input_dir) if f.is_file())

    infiles = ((fpath, fname) for fpath,fname in files if os.path.splitext(fname)[1] == '.json')


    for fpath,fname in infiles:
        print('** processing file {fpath}'.format(fpath=fpath), file=sys.stderr)

        with open(fpath) as fp:

            jobj = json.load(fp)
            text = jobj[TEXT]

            # sort errors from end to the beginning of text
            jobj[ERRORS].sort(key=operator.itemgetter(START), reverse=True)

            for error in jobj[ERRORS]:

                jobj[TEXT] = jobj[TEXT][:error[START]] + error[VALUE] + jobj[TEXT][error[END]:]

                # get offset shift for current error
                shift = len(error[VALUE]) - (error[END] - error[START])

                if shift == 0:
                    continue

                # adjust offsets
                for layer in (jobj[PERSONS], jobj[MOTIVES], jobj[METAMOTIVES]):

                    for ann in layer:

                        if ann[START] >= error[END]:
                            ann[START] += shift
                            ann[END] += shift
                        
                        elif ann[END] >= error[END]:
                            ann[END] += shift

            # sort errors back to increasing order
            jobj[ERRORS].sort(key=operator.itemgetter(START))

            # remove error layer
            jobj.pop(ERRORS)

            with open(os.path.join(args.output_dir, fname), 'w') as outfp:
                json.dump(jobj, outfp, ensure_ascii=False)

