import re
import random
import datasets
from .source_dataset import SourceDataset

_CITATION = """\
@article{Malo2014GoodDO,
  title={Good debt or bad debt: Detecting semantic orientations in economic texts},
  author={P. Malo and A. Sinha and P. Korhonen and J. Wallenius and P. Takala},
  journal={Journal of the Association for Information Science and Technology},
  year={2014},
  volume={65}
}
"""


class FinancialPhrasebank(SourceDataset):
    def __init__(self):
        super().__init__()
        self.citation = _CITATION
        self.say_words = [
            "said",
            "stated",
            "remarked",
            "wrote",
            "announced",
            "acknowledged",
        ]
        self.titles = ["mr", "mrs", "ms", "ceo", "manager", "director"]
        self.say_word_prefixes = [
            "According to <ORG> spokesperson <PERSON>, ",
            "Said company spokesperson <PERSON>, ",
            "Said CEO <PERSON>, ",
            "Chairwoman <PERSON>: ",
            "<PERSON> stated: ",
        ]
        self.say_word_suffixes = [
            " according to spokesperson <PERSON>",
            ", said company spokesman <PERSON>",
            " said spokeswoman <PERSON>",
            ", acknowledged <PERSON>",
            ", reiterated <ORG> CEO <PERSON>",
            " said Ms. <PERSON>",
            ", said Mr. <PERSON>",
            ", stated Ms. <PERSON>",
            " stated Mr. <PERSON>",
        ]
        # 1. select sentences at least ``min_tokens'' long
        # 2. add templates based on ``say_word'' and ``titles''
        min_tokens = 3
        dataset = datasets.load_dataset("financial_phrasebank", "sentences_allagree")
        dataset = dataset.filter(
            lambda x: len(x["sentence"].replace("  ", " ").split()) > min_tokens
        )
        # ignores splits
        dataset = datasets.concatenate_datasets([dataset[split] for split in dataset])
        self.dataset = dataset.map(self._process_example).filter(
            lambda x: x["text"] != x["template"]
        )

    def _process_text(self, text):
        has_say_word = False
        for say_word in self.say_words:
            if has_say_word or say_word not in text.lower():
                continue
            curr_say_pattern = f"(he|she) (also|further) ({say_word})"
            curr_ignore_patterns = [
                f", {say_word}",
                f"'' {say_word}",
                f"and {say_word}",
            ]
            curr_replace_patterns = [
                f"'s spokeswoman <PERSON> {say_word}",
                f"'s spokesman <PERSON> {say_word}",
                f"'s spokesperson <PERSON> {say_word}",
            ]
            if re.match(curr_say_pattern, text):
                text = re.sub(curr_say_pattern, r"<PERSON> \2 \3", text)
                has_say_word = True
            elif say_word in text.lower():
                if any(t in text.lower() for t in self.titles) and not any(
                    p in text.lower() for p in curr_ignore_patterns
                ):
                    text = text.replace(say_word, random.choice(curr_replace_patterns))
                    has_say_word = True
        if not has_say_word:
            if random.random() > 0.5:
                text = text.strip(" .") + random.choice(self.say_word_suffixes)
            else:
                prefix = random.choice(self.say_word_prefixes)
                text = prefix + text.strip()[0].lower() + text[1:]
        return text

    def _process_example(self, example):
        return {
            "text": example["sentence"],
            "template": self._process_text(example["sentence"]),
            "label": example["label"],
        }
