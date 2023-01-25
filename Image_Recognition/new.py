import os
import pandas as pd
import torch
from torchvision.io import read_image
from torch.utils.data import Dataset
from torchvision import transforms
from torchvision import datasets
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt
from pathlib import Path
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import matplotlib

import numpy as np
from PIL import Image



# 0) prepare data

# class CustomImageDataset(Dataset):
#     def __init__(self, annotations_file, img_dir, transform=None, target_transform=None):
#         self.img_labels = pd.read_csv(annotations_file)
#         self.img_dir = img_dir
#         self.transform = transform
#         self.target_transform = target_transform
#
#     def __len__(self):
#         return len(self.img_labels)
#
#     def __getitem__(self, idx):
#         img_path = os.path.join(self.img_dir, self.img_labels.iloc[idx, 0])
#         image = read_image(img_path)
#         label = self.img_labels.iloc[idx, 1]
#         if self.transform:
#             image = self.transform(image)
#         if self.target_transform:
#             label = self.target_transform(label)
#         return image, label
#

root = Path(os.getcwd())
image_dir = root / 'sample'
csv_file = root / 'file.csv'
transform = transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
# dataset = CustomImageDataset(csv_file, image_dir, transform)

idx = 0
img_dir = '/Image_Recognition/Sample'
img_csv = pd.read_csv('/Image_Recognition/file.csv')
label = str(img_csv.iloc[idx, 0])
img_path = os.path.join(img_dir, label)


img = Image.open(img_path)



# transform = transforms.Compose([            #[1]
#  transforms.Resize(256),                    #[2]
#  transforms.CenterCrop(224),                #[3]
#  transforms.ToTensor(),                     #[4]
#  transforms.Normalize(                      #[5]
#  mean=[0.485, 0.456, 0.406],                #[6]
#  std=[0.229, 0.224, 0.225]                  #[7]
#  )])

transform = transforms.Compose([
 transforms.Resize(256),
 transforms.CenterCrop(224),
 transforms.ToTensor()])


img_tensor = transform(img)

img_r = img_tensor[0, :, :]
img_g = img_tensor[1, :, :]
img_b = img_tensor[2, :, :]

img_r_mean = torch.mean(img_r).item()
img_g_mean = torch.mean(img_g).item()
img_b_mean = torch.mean(img_b).item()

img_r_std = torch.std(img_r).item()
img_g_std = torch.std(img_g).item()
img_b_std = torch.std(img_b).item()

normalize = transforms.Normalize(
  mean=[img_r_mean, img_g_mean, img_b_mean],
  std=[img_r_std, img_g_std, img_b_std])





