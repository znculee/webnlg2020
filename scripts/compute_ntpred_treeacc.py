import argparse
import numpy as np
import os
import re
import sys

import ipdb

os.chdir(os.path.dirname(os.path.realpath(os.path.join(__file__, '..'))))
sys.path.append(os.path.realpath('constrained_decoding'))
from constraint_checking import TreeConstraints


def main(args):
    with open(args.source, 'r') as f:
        sources = [l.strip() for l in f.readlines()]
    with open(args.target, 'r') as f:
        targets = [l.strip() for l in f.readlines()]
    assert len(sources) == len(targets)
    if args.output_path:
        output_file = open(args.output_path, 'w')

    correct = 0
    for src, tgt in zip(sources, targets):
        src_list = src.split()
        predidx = np.where(np.array(src_list) == '__predicate__')[0] + 1
        src_nt = '[__ROOT__ ' + ' '.join(['[__pred_' + src_list[i] + '__ ]' for i in predidx]) + ' ]'
        src_tree = TreeConstraints(src_nt.strip())
        tgt_nt = \
            '[__ROOT__ ' + \
            ' '.join(['[' + x + ' ]' for x in re.compile(r'(__pred_\S+)').findall(tgt.strip())]) + \
            ' ]'
        tgt_nt_list = tgt_nt.split()
        for i, w in enumerate(tgt_nt_list):
            if not src_tree.next_token(w, i):
                score = 0
                break
        else:
            if src_tree.meets_all():
                correct += 1
                score = 1
            else:
                score = 0
        if args.output_path:
            output_file.write(str(score) + '\n')

    if args.output_path:
        output_file.close()
    else:
        print('Tree accuracy: {:.2f} ({} / {})'.format(correct / len(sources) * 100, correct, len(sources)))

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str)
    parser.add_argument('--target', type=str)
    parser.add_argument('--output-path', type=str, default=None)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main(parse_args())
