import os 
import time 
import json
import argparse
from pathlib import Path 
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms as T
import numpy as np
import torchvision



data_dir = "data"
out_dir = "outputs"
epochs = 15
BATCH_SIZE = 32
lr = 3e-4
workers = 4
per_worker = (workers > 0)
shuffle_train = True
shuffle_val = False
PIN_MEMORY = False


def get_device():
    if torch.cuda.is_available():
        return "cuda"
    elif torch.backends.mps.is_available():
        return "mps"
    else:
        return "cpu"
    
device = get_device()


transform = T.Compose([
T.Resize(256),
T.CenterCrop(224),
T.ToTensor(),
T.Normalize(mean=[0.485, 0.456, 0.406],
std=[0.229, 0.224, 0.225]
    ) 
])

train_folder = datasets.ImageFolder("data/train", transform=transform)
val_folder = datasets.ImageFolder("data/val", transform=transform)

print("Train samples:", len(train_folder))
print("Val samples:", len(val_folder))
print("Train classes:", train_folder.classes)
print("Val classes:", val_folder.classes)

assert set(train_folder.classes) == {"recycle", "landfill"}

def loaders():
    train_loader = DataLoader(
        dataset=train_folder,
        batch_size=BATCH_SIZE,
        shuffle=shuffle_train,
        pin_memory=PIN_MEMORY,
        num_workers=workers,
        persistent_workers=per_worker,
        drop_last=False
    )

    val_loader = DataLoader(
        dataset=val_folder,
        batch_size=BATCH_SIZE,
        shuffle=shuffle_val,
        pin_memory=PIN_MEMORY,
        num_workers=workers,
        persistent_workers=per_worker,
        drop_last=False
    )
    return train_loader, val_loader

train_loader, val_loader = loaders()


def build_model(num_classes=2):
    weights = models.ResNet18_Weights.DEFAULT
    model = models.resnet18(weights=weights)    
    input_size = model.fc.in_features
    model.fc = nn.Linear(input_size, num_classes)             
    return model

model = build_model().to(device)

def get_weight():
    label_count = train_folder.targets
    counts = torch.tensor(label_count, dtype=torch.long)

    landfill_count = torch.bincount(counts)[0]
    recycle_count = torch.bincount(counts)[1]

    landfill_weight = 1/landfill_count
    recycle_weight = 1/recycle_count

    weight  = torch.tensor([landfill_weight, recycle_weight])
    weight = weight.to(device)
    return weight

weight = get_weight()

print("Class weights:", weight)


loss_function = nn.CrossEntropyLoss(weight=weight)
train_optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)

training_samples = len(train_folder)
val_samples = len(val_folder)


def training_mode(model):
    model.train()
    loss_total = 0.0
    correct_total = 0
    
    for images, labels in train_loader:
        images = images.to(device)
        labels = labels.to(device)
        logits = model(images)
        loss = loss_function(logits, labels)
        train_optimizer.zero_grad()
        loss.backward()
        train_optimizer.step()

        loss_total += loss.item() * len(images)
        predictions = logits.argmax(dim=1)
        correct = (predictions == labels).sum().item()
        correct_total += correct

    train_loss = loss_total / training_samples
    train_accuracy = correct_total / training_samples

    return train_loss, train_accuracy

def val_mode(model):
    model.eval()

    loss_total = 0.0
    correct_total = 0

    for images, labels in val_loader:
        images = images.to(device)
        labels = labels.to(device)
        with torch.no_grad():  
            logits = model(images)
            loss = loss_function(logits, labels)

        loss_total += loss.item() * len(images)
        predictions = logits.argmax(dim=1)
        correct = (predictions == labels).sum().item()
        correct_total += correct

    val_loss = loss_total / val_samples
    val_accuracy = correct_total / val_samples

    return val_loss, val_accuracy


def epoch_loop(model, epochs):
    best_for_val = float("inf")
    save_dir = Path("backend/models")
    save_dir.mkdir(parents=True, exist_ok=True)

    for each in range(epochs):
        train_loss, train_acc = training_mode(model)
        val_loss, val_acc = val_mode(model)
        print(f"Epoch {each+1}/{epochs} | "
              f"Train Loss: {train_loss:.4f} Acc: {train_acc:.4f} | "
              f"Val Loss: {val_loss:.4f} Acc: {val_acc:.4f}")
        
        if val_loss < best_for_val:
            best_for_val = val_loss
            torch.save(model.state_dict(), (save_dir / "trashnet_best.pt").as_posix())
            print("Saved new val_loss")

            idx_to_class = {v: k for k, v in train_folder.class_to_idx.items()}
            with open((save_dir / "classes.json").as_posix(), "w") as f:
                json.dump(idx_to_class, f)

    print(f"Best val loss: {best_for_val:.4f}")



# temp
mapping = {
    0: "landfill",
    1: "recycle"
}

def prediction(model):
    if model == 0:
        print("Landfill")
    else:
        print("Recycle")


if __name__ == "__main__":
    num_epochs = 15 
    epoch_loop(model, num_epochs)


        

        
        
        











    