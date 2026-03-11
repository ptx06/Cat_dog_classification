from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
from .transforms import get_train_transform, get_val_transform

def create_dataloaders(data_root, batch_size=32, num_workers=4):
    train_dataset = ImageFolder(root=f'{data_root}/train', transform=get_train_transform())
    val_dataset = ImageFolder(root=f'{data_root}/val', transform=get_val_transform())
    test_dataset = ImageFolder(root=f'{data_root}/test', transform=get_val_transform())

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True,
                              num_workers=num_workers, pin_memory=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False,
                            num_workers=num_workers, pin_memory=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False,
                             num_workers=num_workers, pin_memory=True)
    return train_loader, val_loader, test_loader, train_dataset.classes
