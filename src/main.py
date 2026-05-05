import os, sys
from torch import nn
import torch.optim as optim
from torch.utils.data import DataLoader
import torchvision
import torchvision.transforms as transforms
from modules.utility import timeit




class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()

        #1->2
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(16)
        self.rel1 = nn.ReLU()       
        self.conv2 = nn.Conv2d(16, 24, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(24)
        self.rel2 = nn.ReLU()

        #3
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)

        #4->5
        self.conv3 = nn.Conv2d(24, 24, kernel_size=3, stride=1, padding=1)
        self.bn3 = nn.BatchNorm2d(24)
        self.rel3 = nn.ReLU()       
        self.conv4 = nn.Conv2d(24, 32, kernel_size=3, stride=1, padding=1)
        self.bn4 = nn.BatchNorm2d(32)
        self.rel4 = nn.ReLU()

        #6
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)

        #7->8
        self.conv5 = nn.Conv2d(32, 32, kernel_size=3, stride=1, padding=1)
        self.bn5 = nn.BatchNorm2d(32)
        self.rel5 = nn.ReLU()       
        self.conv6 = nn.Conv2d(32, 48, kernel_size=3, stride=1, padding=1)
        self.bn6 = nn.BatchNorm2d(48)
        self.rel6 = nn.ReLU()

        #9
        self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2)

        #10->11
        self.conv7 = nn.Conv2d(48, 48, kernel_size=3, stride=1, padding=1)
        self.bn7 = nn.BatchNorm2d(48)
        self.rel7 = nn.ReLU()       
        self.conv8 = nn.Conv2d(48, 64, kernel_size=3, stride=1, padding=1)
        self.bn8 = nn.BatchNorm2d(64)
        self.rel8 = nn.ReLU()

        #12
        self.pool4 = nn.MaxPool2d(kernel_size=2, stride=2)

        #13->14
        self.conv9 = nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1)
        self.bn9 = nn.BatchNorm2d(64)
        self.rel9 = nn.ReLU()       
        self.conv10 = nn.Conv2d(64, 96, kernel_size=3, stride=1, padding=1)
        self.bn10 = nn.BatchNorm2d(96)
        self.rel10 = nn.ReLU()

        #15
        self.pool5 = nn.MaxPool2d(kernel_size=2, stride=2)

        #16->17
        self.conv11 = nn.Conv2d(96, 96, kernel_size=3, stride=1, padding=1)
        self.bn11 = nn.BatchNorm2d(96)
        self.rel11 = nn.ReLU()       
        self.conv12 = nn.Conv2d(96, 128, kernel_size=3, stride=1, padding=1)
        self.bn12 = nn.BatchNorm2d(128)
        self.rel12 = nn.ReLU()

        #18
        self.pool6 = nn.AvgPool2d(kernel_size=2, stride=2)
        
        #19->20
        self.fc1 = nn.Linear(32 * 28 * 28, out_features=32 * 28 * 28)
        self.fc2 = nn.Linear(32 * 28 * 28, 15)

        #21
        self.pool7 = nn.MaxPool2d(kernel_size=2, stride=2)

        #22
        self.softmax = nn.Softmax2d()
        


    def train(self, mode = True):
        return super().train(mode)
    


    def forward():
        ...


def main(*args, **kwargs)-> None :
    ...




if __name__ == "__main__":
    main()