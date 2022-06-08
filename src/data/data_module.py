from pathlib import Path

import pytorch_lightning as pl
from torch.utils.data import random_split, DataLoader
from .dataset import TextDataset

from nltk.tokenize import word_tokenize
from src.features.preprocess import preprocess
from src.features.vectorizer import get_glove_vectorizer

class TextDataModule(pl.LightningDataModule):
    def __init__(self, data_dir: str = "../data/raw", 
                 tokenize_fn=None,
                 vectorizer_fn=None,
                 preprocess_fn=None,
                 maxlen=10,
                 batch_size: int = 32,
                 num_workers=8):
        super().__init__()
        self.data_dir = Path(data_dir)
        self.batch_size = batch_size
        self.num_workers = num_workers

        # Default choices
        # if preprocess_fn is None:
        #     preprocess_fn = preprocess
        # if tokenize_fn is None:
        #     tokenize_fn = word_tokenize
        # if vectorizer_fn is None:
        #     vectorizer_fn = get_glove_vectorizer()

        self.subsets = {}
        for subset_name in ["train", "test"]:
            self.subsets[subset_name] = TextDataset(
                self.data_dir / f"{subset_name}.csv",
                preprocess_fn=preprocess_fn,
                tokenize_fn=tokenize_fn,
                vectorizer_fn=vectorizer_fn,
            )
        self.subsets["train_full"] = self.subsets["train"]
        val_ratio = 0.2
        num_val = int(val_ratio * len(self.subsets["train_full"]))
        num_train = len(self.subsets["train_full"]) - num_val
        self.subsets["train"], self.subsets["val"] = \
            random_split(self.subsets["train_full"], [num_train, num_val])

    def train_dataloader(self):
        return DataLoader(self.subsets["train"],
                          batch_size=self.batch_size,
                          num_workers=self.num_workers,
                          shuffle=True)

    def val_dataloader(self):
        return DataLoader(self.subsets["val"],
                          num_workers=self.num_workers,
                          batch_size=self.batch_size)

    def test_dataloader(self):
        return DataLoader(self.subsets["test"],
                          num_workers=self.num_workers,
                          batch_size=self.batch_size)
