import os, sys
from torch import nn
import torch.optim as optim
from torch.utils.data import DataLoader
import torchvision
import torchvision.transforms as transforms
from modules.utility import timeit




class CNN(nn.Module):
    rel = nn.ReLU
    def __init__(self):
        super(CNN, self).__init__()

        #1->2
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(16)        
        self.conv2 = nn.Conv2d(16, 24, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(24)
        self.block1 = nn.Sequential(self.conv1,
                                    CNN.rel,
                                    self.bn1,
                                    self.conv2,
                                    CNN.rel,
                                    self.bn2)


        #3
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)

        #4->5
        self.conv3 = nn.Conv2d(24, 24, kernel_size=3, stride=1, padding=1)
        self.bn3 = nn.BatchNorm2d(24)
        self.conv4 = nn.Conv2d(24, 32, kernel_size=3, stride=1, padding=1)
        self.bn4 = nn.BatchNorm2d(32)
        self.block2 = nn.Sequential(self.pool1,
                                    self.conv3,
                                    CNN.rel,
                                    self.bn3,
                                    self.conv4,
                                    CNN.rel,
                                    self.bn4)        

        #6
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)

        #7->8
        self.conv5 = nn.Conv2d(32, 32, kernel_size=3, stride=1, padding=1)
        self.bn5 = nn.BatchNorm2d(32)
        self.conv6 = nn.Conv2d(32, 48, kernel_size=3, stride=1, padding=1)
        self.bn6 = nn.BatchNorm2d(48)
        self.block3 = nn.Sequential(self.pool2,
                                    self.conv5,
                                    CNN.rel,
                                    self.bn5,
                                    self.conv6,
                                    CNN.rel,
                                    self.bn6)
        #9
        self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2)

        #10->11
        self.conv7 = nn.Conv2d(48, 48, kernel_size=3, stride=1, padding=1)
        self.bn7 = nn.BatchNorm2d(48)
        self.conv8 = nn.Conv2d(48, 64, kernel_size=3, stride=1, padding=1)
        self.bn8 = nn.BatchNorm2d(64)
        self.block4 = nn.Sequential(self.pool3,
                                    self.conv7,
                                    CNN.rel,
                                    self.bn7,
                                    self.conv8,
                                    CNN.rel,
                                    self.bn8)

        #12
        self.pool4 = nn.MaxPool2d(kernel_size=2, stride=2)

        #13->14
        self.conv9 = nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1)
        self.bn9 = nn.BatchNorm2d(64)
        self.conv10 = nn.Conv2d(64, 96, kernel_size=3, stride=1, padding=1)
        self.bn10 = nn.BatchNorm2d(96)
        self.block5 = nn.Sequential(self.pool4,
                                    self.conv9,
                                    CNN.rel,
                                    self.bn9,
                                    self.conv10,
                                    CNN.rel,
                                    self.bn10)

        #15
        self.pool5 = nn.MaxPool2d(kernel_size=2, stride=2)

        #16->17
        self.conv11 = nn.Conv2d(96, 96, kernel_size=3, stride=1, padding=1)
        self.bn11 = nn.BatchNorm2d(96)
        self.conv12 = nn.Conv2d(96, 128, kernel_size=3, stride=1, padding=1)
        self.bn12 = nn.BatchNorm2d(128)
        self.block6 = nn.Sequential(self.pool5,
                                    self.conv11,
                                    CNN.rel,
                                    self.bn11,
                                    self.conv12,
                                    CNN.rel,
                                    self.bn12)

        #18
        self.Avg_pool = nn.AvgPool2d(kernel_size=2, stride=2)
        
        #19->20
        self.fc1 = nn.Linear(32 * 28 * 28, out_features=32 * 28 * 28)
        self.fc2 = nn.Linear(32 * 28 * 28, 15)
        self.full_control = self.fc1(self.fc2)
        #21
        self.softmax = nn.Softmax2d()
        self.output_block = nn.Sequential(self.Avg_pool,
                                          self.fc1,
                                          self.fc2,
                                          self.softmax)
        


    def train(self, mode = True):
        return super().train(mode)
    


    def forward(self, data):
        data = self.layer1(data)
        data = self.pool1(data)

        data = self.layer2(data)
        data = self.pool2(data)

        data = self.layer3(data)
        data = self.pool3(data)

        data = self.layer4(data)
        data = self.pool4(data)

        data = self.layer5(data)
        data = self.pool5(data)

        data = self.layer6(data)
        data = self.pool6(data)
        
        data = self.full_control(data)
        data = self.pool7(data)

        self.softmax(data)

        return data



def main(*args, **kwargs)-> None :
    CNN()




if __name__ == "__main__":
    main()