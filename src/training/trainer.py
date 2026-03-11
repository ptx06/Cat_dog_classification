import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR
import os
import time
from ..utils.logger import setup_logger

class Trainer:
    def __init__(self, model, train_loader, val_loader, config, device):
        self.model = model.to(device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.config = config
        self.device = device
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.SGD(model.parameters(), lr=config['train']['lr'],
                                    momentum=config['train']['momentum'],
                                    weight_decay=config['train']['weight_decay'])
        self.scheduler = StepLR(self.optimizer, step_size=config['train']['lr_step_size'],
                                gamma=config['train']['lr_gamma'])
        self.epochs = config['train']['epochs']
        self.save_dir = config['train']['save_dir']
        os.makedirs(self.save_dir, exist_ok=True)
        self.logger = setup_logger('train', log_file=os.path.join(self.save_dir, 'train.log'))
        self.best_acc = 0.0

    def train_one_epoch(self, epoch):
        self.model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        for batch_idx, (images, labels) in enumerate(self.train_loader):
            images, labels = images.to(self.device), labels.to(self.device)
            self.optimizer.zero_grad()
            outputs = self.model(images)
            loss = self.criterion(outputs, labels)
            loss.backward()
            self.optimizer.step()

            running_loss += loss.item() * images.size(0)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

            if (batch_idx + 1) % self.config['train']['log_interval'] == 0:
                self.logger.info(f'Epoch {epoch} [{batch_idx+1}/{len(self.train_loader)}] Loss: {loss.item():.4f}')

        epoch_loss = running_loss / total
        epoch_acc = 100.0 * correct / total
        return epoch_loss, epoch_acc

    def validate(self):
        self.model.eval()
        running_loss = 0.0
        correct = 0
        total = 0
        with torch.no_grad():
            for images, labels in self.val_loader:
                images, labels = images.to(self.device), labels.to(self.device)
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)
                running_loss += loss.item() * images.size(0)
                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        epoch_loss = running_loss / total
        epoch_acc = 100.0 * correct / total
        return epoch_loss, epoch_acc

    def fit(self):
        self.logger.info("Starting training...")
        for epoch in range(1, self.epochs + 1):
            train_loss, train_acc = self.train_one_epoch(epoch)
            val_loss, val_acc = self.validate()
            self.scheduler.step()

            self.logger.info(f'Epoch {epoch}: Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}% | Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%')

            # 保存最佳模型
            if val_acc > self.best_acc:
                self.best_acc = val_acc
                checkpoint_path = os.path.join(self.save_dir, 'best_model.pth')
                torch.save(self.model.state_dict(), checkpoint_path)
                self.logger.info(f'Best model saved with accuracy {val_acc:.2f}%')

        self.logger.info("Training completed.")