import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
import cv2
import os


class ClassifiedSudokuCell:
    def __init__(self, index, value):
        self.index = index
        self.value = value


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x)


class Classifier:

    def __init__(self):
        self.loader = transforms.Compose([
            transforms.Resize(28), 
            transforms.ToTensor(), 
            transforms.Normalize((0.1307,), (0.3081,))
        ])

        self.model = Net()
        self.model.load_state_dict(torch.load("models/classifier.model"))
        self.model.eval()


    def predict(self, img):
        with torch.no_grad():
            cv2.imwrite('temp.png', img)
            img = Image.open('temp.png')
            input = self.loader(img)
            prediction = self.model(input)
            return int(np.argmax(prediction))


def classify_cells(cells):
    result = []
    classifier = Classifier()
    for cell in cells:
        prediction = classifier.predict(cell.img)
        result.append(ClassifiedSudokuCell(cell.index, prediction))
    os.remove('temp.png')
    return result
