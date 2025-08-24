import torch, torch.nn
import torchvision


def build_model(num_classes=3):
    model = torchvision.models.resnet18(pretrained=True)
    input_size = model.fc.in_features
    model.fc = torch.nn.Linear(input_size, num_classes)             
    return model