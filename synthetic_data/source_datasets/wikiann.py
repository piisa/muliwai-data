import re
import datasets
from sacremoses import MosesDetokenizer
from .source_dataset import SourceDataset

_CITATION = """\
@inproceedings{pan-etal-2017-cross,
  title = "Cross-lingual Name Tagging and Linking for 282 Languages",
  author = "Pan, Xiaoman  and
    Zhang, Boliang  and
    May, Jonathan  and
    Nothman, Joel  and
    Knight, Kevin  and
    Ji, Heng",
  booktitle = "Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
  month = jul,
  year = "2017",
  address = "Vancouver, Canada",
  publisher = "Association for Computational Linguistics",
  url = "https://www.aclweb.org/anthology/P17-1178",
  doi = "10.18653/v1/P17-1178",
  pages = "1946--1958",
}
@inproceedings{rahimi-etal-2019-massively,
  title = "Massively Multilingual Transfer for {NER}",
  author = "Rahimi, Afshin  and
    Li, Yuan  and
    Cohn, Trevor",
  booktitle = "Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics",
  month = jul,
  year = "2019",
  address = "Florence, Italy",
  publisher = "Association for Computational Linguistics",
  url = "https://www.aclweb.org/anthology/P19-1015",
  pages = "151--164",
}
"""


class WikiAnn(SourceDataset):
    def __init__(self, languages=["en"], relevant_tags=["LOC", "PER"]):
        super().__init__()
        self.citation = _CITATION
        self.languages = languages
        self.relevant_tags = relevant_tags
        self.detokenizers = {lang: MosesDetokenizer(lang=lang) for lang in languages}
        self.ner_tagset_mapper = {
            0: "O",
            1: "<PERSON>",  # B-PER
            2: "<PERSON>",  # I-PER
            3: "<ORG>",  # B-ORG
            4: "<ORG>",  # I-ORG
            5: "<LOC>",  # B-LOC
            6: "<LOC>",  # I-LOC
        }
        # load all splits + ignore split distinction
        dataset = datasets.concatenate_datasets(
            [
                datasets.load_dataset("wikiann", lang, split=split)
                for lang in languages
                for split in ["train", "validation", "test"]
            ]
        )
        self.dataset = dataset.map(self._process_example).filter(
            lambda x: x["formatted_spans"]
        )

    @staticmethod
    def is_whitespace_lang(lang):
        # non-exhaustive list of languages without spaces in entity spans
        return (lang.startswith("zh")) or (lang in ["ja", "th", "ko"])

    def _process_example(self, example):
        out = dict()
        lang = example["langs"][0]
        detokenize_func = self.detokenizers[lang].detokenize
        do_remove_whitespace = self.is_whitespace_lang(lang)

        for k, v in example.items():
            if k == "tokens":
                templated_tokens = []
                prev_tag = None
                for token, tag in zip(v, example["ner_tags"]):
                    if tag == 0:
                        templated_tokens.append(token)
                    elif tag in [2, 4, 6] and prev_tag != tag:
                        # in <PERSON> / <ORG> / <LOC>
                        templated_tokens.append(self.ner_tagset_mapper[tag])
                    prev_tag = tag
                out["text"] = detokenize_func(v)
                out["template"] = detokenize_func(templated_tokens)
            elif k == "spans":
                gold_entities = []
                for span in example["spans"]:
                    m = re.match("(\w+):(.+)", span)
                    ent_type = m.group(1)
                    if ent_type not in self.relevant_tags:
                        continue
                    ent, (start, end) = m.group(2), m.span(2)
                    if do_remove_whitespace:
                        ent = re.sub(" ", "", ent)
                    gold_entities.append(
                        {
                            "entity_type": ent_type,
                            "value": ent.strip(),
                            "start": start,
                            "end": end,
                        }
                    )
                out["formatted_spans"] = gold_entities
            out[k] = v
        return out
