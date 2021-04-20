<h1>WebNLG Challenge 2020</h1>

This repo provides data and scripts used in the paper `Leveraging Large Pretrained Models for WebNLG 2020` by Xintong Li, Aleksandre Maskharashvili, Symon Jory Stevens-Guille, and Michael White, published at INLG2020.

## Reference

```
@inproceedings{li-etal-2020-leveraging-large,
    title = "Leveraging Large Pretrained Models for {W}eb{NLG} 2020",
    author = "Li, Xintong  and
      Maskharashvili, Aleksandre  and
      Jory Stevens-Guille, Symon  and
      White, Michael",
    booktitle = "Proceedings of the 3rd International Workshop on Natural Language Generation from the Semantic Web (WebNLG+)",
    month = "12",
    year = "2020",
    address = "Dublin, Ireland (Virtual)",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.webnlg-1.12",
    pages = "117--124",
    abstract = "In this paper, we report experiments on finetuning large pretrained models to realize resource description framework (RDF) triples to natural language. We provide the details of how to build one of the top-ranked English generation models in WebNLG Challenge 2020. We also show that there appears to be considerable potential for reranking to improve the current state of the art both in terms of statistical metrics and model-based metrics. Our human analyses of the generated texts show that for Russian, pretrained models showed some success, both in terms of lexical and morpho-syntactic choices for generation, as well as for content aggregation. Nevertheless, in a number of cases, the model can be unpredictable, both in terms of failure or success. Omissions of the content and hallucinations, which in many cases occurred at the same time, were major problems. By contrast, the models for English showed near perfect performance on the validation set.",
}
```

## WebNLG 2020

### Data

The latest and other releases of the WebNLG 2020 data can be tracked in [this repository](https://gitlab.com/shimorina/webnlg-dataset), e.g. [shimorina/webnlg-dataset/releases_v2.1/json](https://gitlab.com/shimorina/webnlg-dataset/-/tree/master/release_v2.1/json).
The offical challenge data can be download from the following links:
[train&dev](https://webnlg-challenge.loria.fr/files/challenge2020_train_dev_v2.zip) and
[test](https://webnlg-challenge.loria.fr/files/rdf-to-text-generation-test-data-without-refs.zip).

### Setup

[huggingface/transformers](https://github.com/huggingface/transformers) should be [installed from the source](https://huggingface.co/transformers/installation.html#installing-from-source).
The code has been tested on commit `3babef81` of [huggingface/transformers](https://github.com/huggingface/transformers).

```bash
git clone https://github.com/huggingface/transformers.git
cd transformers
git checkout -b webnlg 3babef81
pip install -e .
cd ..
git clone https://github.com/znculee/finetune-transformers.git
```

### Data Preprocessing

```bash
bash scripts/prepare.2020_v2.en.sh
```

### [Fine-tune huggingface/transformers](https://github.com/znculee/finetune-transformers)

```bash
bash scripts/train.2020_v2.t5_large.sh
bash scripts/generate.2020_v2.t5_large.sh
```

## WebNLG 2017

### Data

[ThiagoCF05/webnlg/data/v1.5/en](https://github.com/ThiagoCF05/webnlg/tree/master/data/v1.5/en)

### Data Preprocessing


```bash
cp -r path/to/ThiagoCF05/webnlg/data/v1.5/en data/2017_v1_5
bash scripts/prepare.2017_v1_5.sh
```

### [Fine-tune huggingface/transformers](https://github.com/znculee/finetune-transformers)

```bash
bash scripts/train.2017_v1_5.t5_small.sh
bash scripts/generate.2017_v1_5.t5_small.sh
```
