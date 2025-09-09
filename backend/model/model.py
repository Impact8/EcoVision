import torch.nn as nn
from torchvision import models


def build_model(num_classes=2):
    weights = models.ResNet18_Weights.DEFAULT
    model = models.resnet18(weights=weights)
    input_size = model.fc.in_features
    model.fc = nn.Linear(input_size, num_classes)             
    return model