import re
import json
import pandas as pd
import datasets
from .source_dataset import SourceDataset

_CITATION = """\
@inproceedings{zeng-etal-2020-meddialog,
  title = "{M}ed{D}ialog: Large-scale Medical Dialogue Datasets",
  author = "Zeng, Guangtao  and
    Yang, Wenmian  and
    Ju, Zeqian  and
    Yang, Yue  and
    Wang, Sicheng  and
    Zhang, Ruisi  and
    Zhou, Meng  and
    Zeng, Jiaqi  and
    Dong, Xiangyu  and
    Zhang, Ruoyu  and
    Fang, Hongchao  and
    Zhu, Penghui  and
    Chen, Shu  and
    Xie, Pengtao",
  booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
  month = nov,
  year = "2020",
  address = "Online",
  publisher = "Association for Computational Linguistics",
  url = "https://aclanthology.org/2020.emnlp-main.743",
  doi = "10.18653/v1/2020.emnlp-main.743",
  pages = "9241--9250",
}
"""


class MedDialogBase(SourceDataset):
    def __init__(self):
        self.citation = _CITATION
        self.patient = "patient"
        self.doctor = "doctor"
        self.replace_patterns_mapper = {
            # general tags
            "<DISEASE>": [
                "Coronavirus",
                "COVID-19",
                "COVID 19",
                "COVID19",
                "Covid 19",
                "COVID" "Corona-virus",
            ],
            "<LOCATION>": ["Asian", "Bali"],
            "<GPE>": [
                "France",
                "Vietnam",
                "India",
                "Germany",
                "South Africa",
                "United States",
            ],
            " <GPE> ": [" the US ", " the UK ", " the Netherlands "],
            # specific heuristics
            "<PERSON>, male ": ["My son ", "husband "],
            "<PERSON>, female ": ["My daughter ", "wife "],
            " <PERSON>, male ": [" Son ", " dad "],
            " <PERSON>, female ": [" Daughter ", " mom "],
            "<PERSON>, male": ["Boyfriend"],
            "<PERSON>, female": ["Girlfriend"],
        }

    def get_dataset(self, do_dialog=False):
        if do_dialog:
            return self.dialog
        else:
            return self.dataset

    def _process_text(self, text):
        for repl, patterns in self.replace_patterns_mapper.items():
            for pattern in patterns:
                text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
        text = re.sub("^(she) ", "<PERSON>, a female, ", text, flags=re.IGNORECASE)
        text = re.sub("^(he) ", "<PERSON>, a male, ", text, flags=re.IGNORECASE)
        return text

    @staticmethod
    def flatten(dialog):
        return [
            {
                "id": str(d["id"]),
                "description": d["description"],
                "speaker": utt["speaker"],
                "text": utt["text"],
                "template": utt["template"],
            }
            for d in dialog
            for utt in d["utterances"]
        ]


class MedicalDialog(MedDialogBase):
    def __init__(
        self, filepaths=["english-train.json", "english-dev.json", "english-test.json"]
    ):
        super().__init__()
        self.dialog = [d for filepath in filepaths for d in self._load_file(filepath)]
        flattened_data = self.flatten(self.dialog)
        self.dataset = datasets.Dataset.from_pandas(pd.DataFrame(flattened_data))

    def _load_file(self, filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
        dialogs = []
        for id, d in enumerate(data):
            utterances = []
            for utt in d["utterances"]:
                for pattern, speaker in [
                    ("^patient:(.+)", self.patient),
                    ("^doctor:(.+)", self.doctor),
                ]:
                    match = re.match(pattern, utt.strip())
                    if match is not None:
                        text = match.group(1)
                        utterances.append(
                            {
                                "speaker": speaker,
                                "text": text,
                                "template": self._process_text(text),
                            }
                        )
            # keep only dialogs with at least one utterance different from source
            if any(utt["text"] != utt["template"] for utt in utterances):
                dialogs.append(
                    {
                        "id": id,
                        "description": d["description"],
                        "utterances": utterances,
                    }
                )
        return dialogs
