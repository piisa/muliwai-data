import json
import pandas as pd
import datasets
from .source_dataset import SourceDataset

_CITATION = """\
@incollection{Klimt2004,
  author = {Klimt, Bryan and Yang, Yiming},
  doi = {10.1.1.61.1645},
  journal = {Machine Learning: ECML 2004},
  pages = {217--226},
  title = {The Enron Corpus: A New Dataset for Email Classification Research},
  volume = {Volume 3201/2004},
  year = 2004
}

@inproceedings{OrtizSuarezSagotRomary2019,
  author    = {Pedro Javier {Ortiz Su{\'a}rez} and Beno{\^i}t Sagot and Laurent Romary},
  title     = {Asynchronous pipelines for processing huge corpora on medium to low resource infrastructures},
  series = {Proceedings of the Workshop on Challenges in the Management of Large Corpora (CMLC-7) 2019. Cardiff, 22nd July 2019},
  doi       = {10.14618/ids-pub-9021},
  url       = {http://nbn-resolving.de/urn:nbn:de:bsz:mh39-90215},
  pages     = {9--16},
  year      = {2019},
}

@article{DBLP:journals/corr/abs-1903-04561,
  author    = {Daniel Borkan and
               Lucas Dixon and
               Jeffrey Sorensen and
               Nithum Thain and
               Lucy Vasserman},
  title     = {Nuanced Metrics for Measuring Unintended Bias with Real Data for Text
               Classification},
  journal   = {CoRR},
  volume    = {abs/1903.04561},
  year      = {2019},
  url       = {http://arxiv.org/abs/1903.04561}
}
"""


class PiiHackathon(SourceDataset):
    def __init__(self, filepaths=["en_pii_final.jsonl"]):
        super().__init__()
        self.citation = _CITATION
        data = []
        for filepath in filepaths:
            with open(filepath, "r") as f:
                data.extend([json.loads(line) for line in f])
        df = pd.DataFrame(data)
        dataset = datasets.Dataset.from_pandas(df).map(self._process_example)
        self.dataset = dataset.filter(lambda x: x["text"] != x["template"])

    def _process_example(self, example):
        templated_text = ""
        text = example["text"]
        spans = example["formatted_spans"]
        prev_end = 0
        for i, span in enumerate(spans):
            s, e = span["start"], span["end"]
            # multiple annotations are possible; select ``top'' label for now
            labels = span["ent_types"]
            label = max(labels, key=lambda l: l["score"])['label']
            templated_text += text[prev_end:s] + f"<{label}>"
            prev_end = e
            if i == len(spans) - 1:
                templated_text += text[prev_end:]
        example["template"] = templated_text
        return example
