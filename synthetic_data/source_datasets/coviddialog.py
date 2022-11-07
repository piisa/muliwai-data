import re
import datasets
import pandas as pd
from .meddialog import MedDialogBase

_CITATION = """\
@article{ju2020CovidDialog,
  title={CovidDialog: Medical Dialogue Datasets about COVID-19},
  author={Ju, Zeqian and Chakravorty, Subrato and He, Xuehai and Chen, Shu and Yang, Xingyi and Xie, Pengtao},
  journal={https://github.com/UCSD-AI4H/COVID-Dialogue}, 
  year={2020}
}
"""


class CovidDialog(MedDialogBase):
    def __init__(self, filepath="./COVID-Dialogue-Dataset-English.txt"):
        super().__init__()
        self.citation = _CITATION
        self.dialog = self._load_file(filepath)
        flattened_data = self.flatten(self.dialog)
        self.dataset = datasets.Dataset.from_pandas(pd.DataFrame(flattened_data))

    def _load_file(self, filepath):
        line_chunks = dict()
        curr_line_chunk = []
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                id_match = re.match("id=(\d{1,3})", line)
                if id_match is not None:
                    if curr_line_chunk:
                        line_chunks[id] = curr_line_chunk
                    curr_line_chunk = []
                    id = int(id_match.group(1))
                else:
                    if line and not line.startswith("http"):
                        curr_line_chunk.append(line)

        dialogs = []
        for id, line_chunk in line_chunks.items():
            skip_next_line = False
            utterances = []
            for i, line in enumerate(line_chunk):
                if skip_next_line or line == "Dialogue":
                    skip_next_line = False
                    continue
                if line == "Description":
                    description = line_chunk[i + 1]
                    skip_next_line = True
                elif line == "Patient:":
                    curr_speaker = self.patient
                elif line == "Doctor:":
                    curr_speaker = self.doctor
                else:
                    utterances.append(
                        {
                            "speaker": curr_speaker,
                            "text": line,
                            "template": self._process_text(line),
                        }
                    )
            # keep only dialogs with at least one utterance different from source
            if any(utt["text"] != utt["template"] for utt in utterances):
                dialogs.append(
                    {"id": id, "description": description, "utterances": utterances}
                )
        return dialogs
