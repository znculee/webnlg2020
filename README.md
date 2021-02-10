<h1>WebNLG Challenge 2020</h1>

This repo provides data and scripts used in the paper `Leveraging Large Pretrained Models for WebNLG 2020` by Xintong Li, Aleksandre Maskharashvili, Symon Jory Stevens-Guille, and Michael White, published at INLG2020.

Bibtex will be available soon.

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
