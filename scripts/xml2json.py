import argparse
import json
import os

import xmltodict


def xml2json(args):
    json_data = {'entries': []}
    for path, subdirs, files in os.walk(args.xml):
        for name in files:
            xml_file_path = os.path.join(path, name)
            if not xml_file_path.endswith('.xml'):
                continue
            with open(xml_file_path, 'r') as xml_file:
                xml_data = xmltodict.parse(xml_file.read())
            json_data['entries'].extend(xml_data['benchmark']['entries']['entry'])
    entries = []
    valid_idx = 1
    for idx, entry in enumerate(json_data['entries']):
        if not isinstance(entry, dict):
            continue
        mtriple = entry['modifiedtripleset']['mtriple']
        if not isinstance(mtriple, list):
            entry['modifiedtripleset']['mtriple'] = [mtriple]
        if not args.nolex:
            lex = entry['lex']
            if not isinstance(lex, list):
                json_data['entries'][idx]['lex'] = [lex]
        entry.update({'idx': valid_idx})
        entries.append(entry)
        valid_idx += 1
    json_data['entries'] = entries
    with open(args.json, 'w') as json_file:
        json.dump(json_data, json_file, indent=4, ensure_ascii=False)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('xml')
    parser.add_argument('json')
    parser.add_argument('--nolex', action='store_true')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    xml2json(parse_args())
