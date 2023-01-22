import torchvision
from matplotlib import transforms
import os
import torch
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
import PIL
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

#dataset = torchvision.datasets.ImageFolder(root="C:\\Users\\ssuz0008\\PycharmProjects\\UVVis_3.0\\PyTorch\\Image_Dataset\\Sample", transform=transforms.ToTensor())

class FacesDataset(Dataset):

    def __init__(self, root, image_dir, csv_file, transform=None):
        self.root = root
        self.image_dir = image_dir
        self.image_files = os.listdir(image_dir)
        self.data = pd.read_csv(csv_file).iloc[:, 1]
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        image_name = os.path.join(self.image_dir, self.image_files[index])
        image = PIL.Image.open(image_name)
        label = self.data[index]
        if self.transform:
            image = self.transform(image)
        return (image, label)


root = Path(os.getcwd())
image_dir = root/'sample'
csv_file = root/'file.csv'
transform_img = transforms.Compose([
                            transforms.Resize(80),
                            transforms.CenterCrop(80),
                            transforms.ToTensor()
])


dset = FacesDataset(root, image_dir, csv_file, transform= transform_img)

train_dataset, test_dataset = torch.utils.data.random_split(dset, [1, 1])


def show_image(image, label, dataset):
    print(f"Label: {label}")
    plt.imshow(image.permute(1, 2, 0))
    plt.show()


show_image(*train_dataset[0], train_dataset)

