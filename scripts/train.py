import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import torch
from src.data.dataset import create_dataloaders
from src.models.model import build_model
from src.training.trainer import Trainer
from src.utils.config import load_config

def main():
    config = load_config('configs/train_config.yaml')
    device = torch.device(config['device'] if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    train_loader, val_loader, test_loader, classes = create_dataloaders(
        data_root=config['data']['root'],
        batch_size=config['data']['batch_size'],
        num_workers=config['data']['num_workers']
    )
    print(f"Classes: {classes}")

    model = build_model(num_classes=config['model']['num_classes'],
                        pretrained=config['model']['pretrained'])

    trainer = Trainer(model, train_loader, val_loader, config, device)
    trainer.fit()

if __name__ == '__main__':
    main()