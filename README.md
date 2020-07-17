## WebNLG Challenge 2020

### Data Preprocessing

The latest and other releases of the WebNLG data are tracked in [this repository](https://gitlab.com/shimorina/webnlg-dataset).

```bash
cp -r https://gitlab.com/shimorina/webnlg-dataset/release_v2.1/json data/v2_1
bash scripts/prepare.v2_1.sh

cp -r https://gitlab.com/shimorina/webnlg-dataset/release_v2.1_constrained/json data/v2_1_constr
bash scripts/prepare.v2_1_constr.sh

cp -r https://github.com/ThiagoCF05/webnlg/data/v1.5/en data/2017_v1_5
bash scripts/prepare.2017_v1_5.sh
```
