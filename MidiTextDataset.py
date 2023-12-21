from torch.utils.data import Dataset
import pandas as pd

class MidiTextDataset(Dataset):
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
    # end init

    def __len__(self):
        return self.df.shape[0]
    # end len

    def __getitem__(self, index):
        midi = self.df.midi_text[index]
        text = self.df.text[index]
        return midi, text
    # end getitem
# end class