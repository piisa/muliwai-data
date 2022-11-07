import datasets
import random
from .source_dataset import SourceDataset

_CITATION = """\
@inproceedings{Casanueva2020,
    author      = {I{\~{n}}igo Casanueva and Tadas Temcinas and Daniela Gerz and Matthew Henderson and Ivan Vulic},
    title       = {Efficient Intent Detection with Dual Sentence Encoders},
    year        = {2020},
    month       = {mar},
    note        = {Data available at https://github.com/PolyAI-LDN/task-specific-datasets},
    url         = {https://arxiv.org/abs/2003.04807},
    booktitle   = {Proceedings of the 2nd Workshop on NLP for ConvAI - ACL 2020}
}
"""


class Banking77(SourceDataset):
    def __init__(self):
        super().__init__()
        self.citation = _CITATION
        self.replace_patterns_mapper = {
            "Apple Watch": "device",
            "bank account": "account",
            "Google Pay": "<ORG> account",
            "Apple pay": "<ORG> account",
            "American Express": "<ORG> account",
        }
        self.GPE_patterns = ["US", "EU", "UK", "European Union", "Europe"]
        self.ID_patterns = ["My id is <ID>.", "SSN: <ID>.", "My number is <ID>."]
        self.disclosure_patterns = [
            "My name is <PERSON>.",
            "My name is <PERSON>, DOB: <DATE>.",
            "<PERSON> here.",
            "I'm <PERSON>.",
        ]

        min_tokens = 3
        dataset = datasets.load_dataset("banking77")
        dataset = dataset.filter(
            lambda x: not x["text"].strip().startswith("Why")
            and len(x["text"].replace("  ", " ").split()) > min_tokens
        )
        # ignores splits
        dataset = datasets.concatenate_datasets([dataset[split] for split in dataset])
        self.dataset = dataset.map(self._process_example).filter(
            lambda x: x["text"] != x["template"]
        )

    def _process_text(self, text):
        if " id " in text or "ident" in text:
            return f"{text} " + random.choice(self.ID_patterns)
        elif any(f"{w} " in text for w in ["get", "order", "like", "want"]):
            if random.random() > 0.5:
                return random.choice(self.disclosure_patterns) + f" {text}"
            else:
                suffix = f"? {random.choice(self.disclosure_patterns)}"
                return text.strip(" ?.") + suffix
        return text

    def _process_example(self, example):
        return {
            "text": example["text"],
            "template": self._process_text(example["text"]),
            "label": example["label"],
        }
