import argparse
from nltk.tokenize.treebank import TreebankWordDetokenizer
from sacrebleu import corpus_bleu

def main(args):
    with open(args.hyp, 'r') as f:
        hyps = [TreebankWordDetokenizer().detokenize(l.strip().split()) for l in f.readlines()]
    with open(args.ref, 'r') as f:
        refs = [TreebankWordDetokenizer().detokenize(l.strip().split()) for l in f.readlines()]
        mref = []
        ref = []
        for l in refs:
            if l != '':
                ref.append(l)
            else:
                mref.append(ref)
                ref = []
        mref.append(ref)
    assert len(mref) * args.beam_size == len(hyps)

    output_file = open(args.output_path, 'w')
    for i, hyp in enumerate(hyps):
        print(f'scoring progress: %{100*(i+1)/len(hyps):.2f} ({i+1}/{len(hyps)})', end='\r')
        ref = mref[int(i / args.beam_size)]
        bleu = corpus_bleu([hyp], [[x] for x in ref])
        output_file.write(str(bleu.score) + '\n')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-path', type=str)
    parser.add_argument('--beam-size', type=int)
    parser.add_argument('--hyp', type=str)
    parser.add_argument('--ref', type=str)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main(parse_args())
