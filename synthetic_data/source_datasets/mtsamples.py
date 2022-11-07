import datasets
import re
import pandas as pd
from .source_dataset import SourceDataset

_CITATION = """\
@misc{MTSamples,
  title = "MTSamples: Transcribed Medical Transcription Sample Reports and Examples",
  howpublished = "https://mtsamples.com/"
}
"""


class MTSamples(SourceDataset):
    def __init__(self, filepath="./mtsamples.csv"):
        super().__init__()
        self.citation = _CITATION
        self.pattern_mapper = {
            # general rules in corpus
            "ABCD": "<ORG>",
            "MM/DD/YYYY": "<DATE>",
            "ABC": "<PERSON>",
            "Mr. A": "Mr. <PERSON5>",
            "Ms. A": "Ms. <PERSON5>",
            "XYZ": "<PERSON2>",
            "XXXX": "<PERSON3>",
            "Ms. X": "Ms. <PERSON4>",
            "Mr. X": "Mr. <PERSON4>",
            "Dr. X": "Dr. <PERSON3>",
            # specific cases requiring post processing
            "is from [A-Z]\w+": "lived in <LOC>",
            "lived in [A-Z]\w+": "lived in <LOC>",
            "<PERSON> Avenue": "<STREET_ADDRESS>",
            "at <PERSON'": "at <LOC",
            "in <PERSON": "<LOC",
            "<PERSON2> County": "<ORG2> County",
        }
        df = pd.read_csv(filepath, index_col=0)
        df = df[~df.transcription.isna()]
        df["template"] = df.transcription.apply(self._process_text)
        df = df[df.template != df.transcription].reset_index(drop=True)
        self.dataset = datasets.Dataset.from_pandas(df).map(self._process_example)

    def _process_text(self, text):
        for patt, repl in self.pattern_mapper.items():
            text = re.sub(patt, repl, text)
        return text

    def _process_example(self, example):
        out = {"text": example["transcription"]}
        for k, v in example.items():
            out[k] = v
        return out
