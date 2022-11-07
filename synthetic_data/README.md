# About
Contains processing scripts that create templated data.

1. `Banking77` - financial
2. `CovidDialog` - medical
3. `FinancialPhrasebank` - financial
4. `MedicalDialog` - medical
5. `MTSamples` - medical
6. `WikiAnn` - wikipedia
7. `PiiHackathon` - cross domain (civil comments, enron, oscar) annotated data from bigscience privacy WG hackathon

## Requirements
* Python 3 
* `pip install -r requirements.txt`
* [piisa/pii-data](https://github.com/piisa/pii-data)
* Some datasets need to be [downloaded manually](#Manual-Downloading).

## Usage
Load single dataset before template filling:
```python
mt = MTSamples()
mt.get_dataset()
```
Minimum example - name substitution:
```python
import datasets
from source_datasets import Banking77, FinancialPhrasebank
from example import process

# load dataset
fp = FinancialPhrasebank()
dataset = fp.get_dataset()

# name substitution example
processed = list(map(lambda x: process(x, lang="en"), dataset))
print(processed_dataset[0])
```
This will show something like the below:
```json
{
    "template": "My name is <PERSON>. How do I know if I will get my card, or if it is lost?",
    "processed_text": "My name is Rushil. How do I know if I will get my card, or if it is lost?",
    "pii_list": [
        {
            "type": "PERSON",
            "value": "Rushil",
            "chunkid": 1,
            "start": 11,
            "end": 17
        }
    ]
}
```

### Schema
Currently, the processed datasets obtained via `.get_dataset()` each have *at least* fields `text` and `template`. If there are additional fields from their source dataset (eg `label`), they are preserved as well.
```json
{
    "text": "Alice and Bob live in New York",
    "template": "<PERSON> and <PERSON> live in <LOC>"
}
```
These datasets are loaded by default as standalone sentences/texts. To load the dialog datasets as dialogs, set `do_dialog=True`, e.g., `md = MedicalDialog(); md.get_dataset(do_dialog=True)`. This will load the data in the following format:
```json
{
    "id": "an id", 
    "description": "a string description",
    "utterances": [
        {
            "speaker": "patient",
            "text": "hello dr smith",
            "template": "hello dr <PERSON>"
        }
    ]
}
```
The filled templates will look like what is shown above in the example section. 


### Manual Downloading
Some datasets need to be acquired separately. 
- MTSamples: download the csv from [kaggle](https://www.kaggle.com/tboyle10/medicaltranscriptions#mtsamples.csv) and specify the filepath, e.g., `MTSamples(filepath="./mtsamples.csv")`
- MedDialog: download following instructions on the project [repo](https://github.com/UCSD-AI4H/Medical-Dialogue-System). Specify the filepaths, e.g., `MedDialogs(filepaths=["./english-train.json", "./english-dev.json", "./english-test.json"])`
- COVID-Dialogue: download following instructions on the project [repo](https://github.com/UCSD-AI4H/COVID-Dialogue/), or directly via `wget -O COVID-Dialogue-Dataset-English.txt https://raw.githubusercontent.com/UCSD-AI4H/COVID-Dialogue/master/COVID-Dialogue-Dataset-English.txt` Specify the filepath e.g., `CovidDialog(filepath="./COVID-Dialogue-Dataset-English.txt")`
- PiiHackathon: on shared drive; contact [@j-chim](https://github.com/j-chim/).


## TODO
- Incorporate into overall framework
- Add testing
- Improve domain coverage
- Improve templating
    - Standardize PII tags
    - Lexica with more entity coverage + more categories
    - Lexica for ORG, GPE, etc
- Display evaluation results
