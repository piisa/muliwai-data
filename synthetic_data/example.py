import re
import json
import random
from lexica.checklist import FIRST_NAMES, LAST_NAMES
from pii_data.types import PiiEnum, PiiEntity
from pii_data.types.piicollection import PiiCollection
from source_datasets import *


class FilledTemplate:
    def __init__(
        self, template: str, processed_text: str, pii_collection: PiiCollection
    ):
        self.template = template
        self.processed_text = processed_text
        self.pii_collection = pii_collection

    def as_dict(self):
        return {
            "template": self.template,
            "processed_text": self.processed_text,
            "pii_list": [pii.as_dict() for pii in self.pii_collection.pii],
        }

    def __repr__(self):
        return json.dumps(self.as_dict(), indent=4)


def substitute_person(x, idx, spans, random_seed=None):
    if random_seed is not None:
        random.seed(random_seed)

    match = re.search("<PERSON>", x)
    if match is None:
        return x, idx, spans

    start, end = match.span()
    head, tail = x[:end], x[end:]
    if idx:
        start_from = idx[-1][1]
        start += start_from
        end += start_from
    curr_substitution = random.choice(FIRST_NAMES["men"])
    idx.append((start, end))
    spans.append(curr_substitution)

    head = re.sub("<PERSON>", curr_substitution, head)
    tail, idx, spans = substitute_person(tail, idx, spans)
    return head + tail, idx, spans


def process(
    example, chunk=1, lang=None, country=None, docid=None, subtype=None, random_seed=42
):
    template = example["template"]
    # this example supports PERSON only;
    # future versions with actual processing scripts will check + support additional ents
    processed_text, pii_idx, spans = substitute_person(
        x=template, idx=[], spans=[], random_seed=random_seed
    )
    pii_collection = PiiCollection(lang=lang, docid=docid)
    for (start, end), span in zip(pii_idx, spans):
        entity = PiiEntity(
            ptype=PiiEnum.PERSON,
            chunk=chunk,
            pos=start,
            value=span,
            subtype=subtype,
            lang=lang,
            country=country,
            docid=docid,
        )
        pii_collection.entity(entity)
    return FilledTemplate(
        template=template, processed_text=processed_text, pii_collection=pii_collection
    )
