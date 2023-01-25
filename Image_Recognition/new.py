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

# 0) prepare data

class CustomImageDataset(Dataset):
    def __init__(self, annotations_file, img_dir, transform=None, target_transform=None):
        self.img_labels = pd.read_csv(annotations_file)
        self.img_dir = img_dir
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.img_labels.iloc[idx, 0])
        image = read_image(img_path)
        label = self.img_labels.iloc[idx, 1]
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return image, label


root = Path(os.getcwd())
image_dir = root / 'sample'
csv_file = root / 'file.csv'
transform = transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
dataset = CustomImageDataset(csv_file, image_dir, transform)


idx = 0
img_dir = 'C:\\Users\\ssuz0008\\PycharmProjects\\UVVis_3.0\\PyTorch\\Image_Dataset\\Sample'
img_label = pd.read_csv('C:\\Users\\ssuz0008\\PycharmProjects\\UVVis_3.0\\PyTorch\\Image_Dataset\\file.csv')
label = str(img_label.iloc[idx, 0])
img_path = os.path.join(img_dir, label)
image = read_image(img_path)

