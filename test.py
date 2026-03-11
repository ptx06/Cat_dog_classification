from src.data.dataset import create_dataloaders
train_loader, val_loader, test_loader, classes = create_dataloaders('data', batch_size=4)
print(f"类别: {classes}")
print(f"训练集 batch 数: {len(train_loader)}")