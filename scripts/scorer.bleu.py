import argparse
from nltk.tokenize.treebank import TreebankWordDetokenizer
from sacrebleu import corpus_bleu

def main(args):
    with open(args.hyp, 'r') as f:
        hyps = [TreebankWordDetokenizer().detokenize(l.strip().split()) for l in f.readlines()]
    with open(args.ref, 'r') as f:
        refs = [TreebankWordDetokenizer().detokenize(l.strip().split()) for l in f.readlines()]

    output_file = open(args.output_path, 'w')
    for i, (hyp, ref) in enumerate(zip(hyps, refs)):
        bleu = corpus_bleu([hyp], [[ref]])
        output_file.write(str(bleu.score) + '\n')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-path', type=str)
    parser.add_argument('--hyp', type=str)
    parser.add_argument('--ref', type=str)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main(parse_args())
