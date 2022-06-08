import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
import pandas as pd

class TextDataset(Dataset):
    def __init__(self, dataset_file,
                 tokenize_fn=None,
                 vectorizer_fn=None,
                 preprocess_fn=None):
        self.dataset_file = dataset_file
        self.preprocess_fn = preprocess_fn
        self.tokenize_fn = tokenize_fn
        self.vectorizer_fn = vectorizer_fn

        self.df = pd.read_csv(dataset_file)

        target_conversion = {
            'neutral': 0,
            'positive': 1,
            'negative': 2
        }
        if 'sentiment' in self.df:
            self.df["label"] = self.df['sentiment'].map(target_conversion)
    
    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, idx):
        res = {}
        res["text"] = self.df["text"].iloc[idx]
        text = res["text"]
        if 'label' in self.df:
            res["labels"] = torch.tensor(self.df["label"].iloc[idx])
        
        if self.preprocess_fn is not None:
            text = self.preprocess_fn(text)
            res["preproc_text"] = text
        
        if self.vectorizer_fn is not None:
            if self.tokenize_fn is not None:
                text = self.tokenize_fn(text)
            x = self.vectorizer_fn(text)
            if type(x) in [np.ndarray, list]:
                res["feat"] = torch.tensor(x)
            else:
                # Merge the resulting dict
                new_dict = {key: torch.tensor(val) for key, val in x.items()}
                res = {**res, **new_dict}
            # else:
            #     raise RuntimeError("The vectorizer fn returns an unknown type " + type(x))
        
        return res
