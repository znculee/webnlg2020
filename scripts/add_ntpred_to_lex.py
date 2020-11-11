"""
add non-terminal predicates to target lexicalizations by alignments
e.g.
The runway length of Andrews County airport is 929.0 .
The runway __runwayLength__ length of Andrews County airport is 929.0 .
"""

import argparse
from itertools import chain

import numpy as np


def flatten(A):
    rt = []
    for i in A:
        if isinstance(i, list): rt.extend(flatten(i))
        else: rt.append(i)
    return rt

def add_ntpred_to_lex(args):

    with open(args.input_corpus, 'r') as f:
        corpus = [l.strip().split(' ||| ') for l in f.readlines()]
    source = [l[0].split() for l in corpus]
    target = [l[1].split() for l in corpus]

    with open(args.input_align, 'r') as f:
        align = [l.strip().split() for l in f.readlines()]

    nonterminals = set()
    output_target = []

    for src, tgt, aln in zip(source, target, align):

        alnmtx = np.zeros((len(src), len(tgt)))
        for a in aln:
            i, j = (int(x) for x in a.split('-'))
            alnmtx[i, j] = 1

        predidx = np.where(np.array(src) == '__predicate__')[0] + 1
        assert alnmtx[predidx, :].any(1).all() == True # no null alignment
        assert (alnmtx[predidx, :].sum(1) == 1).all() == True # single mapping

        for i in predidx:
            j = int(np.where(alnmtx[i, :] == 1)[0])
            ntpred = '__pred_' + src[i] + '__'
            nonterminals.add(ntpred)
            tgt[j] = [ntpred, tgt[j]]
        tgt = flatten(tgt)
        output_target.append(tgt)

    with open(args.output_nonterminals, 'w') as f:
        f.writelines([x + '\n' for x in nonterminals])

    with open(args.output_target, 'w') as f:
        f.writelines([' '.join(x) + '\n' for x in output_target])

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-corpus')
    parser.add_argument('--input-align')
    parser.add_argument('--output-nonterminals', type=str)
    parser.add_argument('--output-target', type=str)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    add_ntpred_to_lex(parse_args())
