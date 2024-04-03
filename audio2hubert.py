from transformers import AutoFeatureExtractor, AutoModel
import torch
import os
import numpy as np
from tqdm import tqdm

model_id = 'ntu-spml/distilhubert'
feature_extractor = AutoFeatureExtractor.from_pretrained(
    model_id, do_normalize=True, return_attention_mask=True
)

sampling_rate = feature_extractor.sampling_rate
model = AutoModel.from_pretrained(model_id)

from datasets import load_dataset, Audio

path = 'data/midis_wavs'
dataset = load_dataset('audiofolder', data_dir=path)

# resample audio files to desired sample rate
dataset = dataset.cast_column('audio', Audio(sampling_rate=sampling_rate))

def preprocess_function(examples):
    audio_arrays = [x["array"] for x in examples["audio"]]
    inputs = feature_extractor(
        audio_arrays,
        sampling_rate=feature_extractor.sampling_rate,
        return_attention_mask=True,
    )
    return inputs

dataset_encoded = dataset.map(
    preprocess_function,
    remove_columns=['audio'],
    batched=True,
    batch_size=100,
    num_proc=1,
)

dataset_encoded

import librosa

result_dict = {}

print('running model on dataset')
for i in tqdm(range(len(dataset_encoded['test']))):
    t = torch.FloatTensor(dataset_encoded['test'][i]['input_values'] )
    tt = t.view(1, t.shape[0])
    
    wav = dataset['test'][i]['audio']['path']

    h = model(tt).last_hidden_state
    h_mean = np.mean(h.squeeze().detach().numpy(), axis = 0)
    
    result_dict[ wav.split('/')[-1].split('.')[0] ] = h_mean

import pandas as pd

df = pd.DataFrame.from_dict(result_dict, orient='index', dtype=np.float32).reset_index()
df.to_csv('data/' + path.split('/')[-1] + '.csv', index=False)