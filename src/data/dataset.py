import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd

class TextDataset(Dataset):
    def __init__(self, dataset_file,
                 tokenize_fn,
                 vectorizer_fn,
                 preprocess_fn=None,
                 sparse=False):
        self.dataset_file = dataset_file
        
        self.preprocess_fn = preprocess_fn
        self.tokenize_fn = tokenize_fn
        self.vectorizer_fn = vectorizer_fn
        self.sparse = sparse
        
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
        text = self.df.loc[idx, "text"]
        label = self.df.loc[idx, "label"] if 'label' in self.df else None
        
        if self.preprocess_fn is not None:
            text = self.preprocess_fn(text)
            
        tokens = self.tokenize_fn(text)
        x = self.vectorizer_fn(tokens)
        
        x = torch.from_numpy(x.toarray().squeeze())
        if self.sparse:
            x = x.to_sparse()
        
        if label is None:
            return x
        else:
            return x, label
