class SourceDataset:
    def __init__(self):
        self.dataset = None
        self.citation = None
        self.keep_columns = ["text", "template"]

    def __len__(self):
        return len(self.dataset)

    def __repr__(self):
        return str(self.dataset)

    def get_dataset(self):
        return self.dataset

    def prune_columns(self, keep_columns=None):
        if keep_columns is None:
            keep_columns = self.keep_columns
        return self.dataset.remove_columns(
            [c for c in self.dataset.features if c not in keep_columns]
        )
