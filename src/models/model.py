import torch.nn as nn
from torchvision import models

def build_model(num_classes, pretrained=True):
    model = models.mobilenet_v2(weights='IMAGENET1K_V1' if pretrained else None)
    in_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(0.2),
        nn.Linear(in_features, num_classes)
    )
    return model