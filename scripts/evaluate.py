import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import torch
from src.data.dataset import create_dataloaders
from src.models.model import build_model
from src.evaluation.evaluator import evaluate
from src.utils.config import load_config

def main():
    config = load_config('configs/train_config.yaml')
    device = torch.device(config['device'] if torch.cuda.is_available() else 'cpu')

    # 只加载测试集
    _, _, test_loader, classes = create_dataloaders(
        data_root=config['data']['root'],
        batch_size=config['data']['batch_size'],
        num_workers=config['data']['num_workers']
    )

    model = build_model(num_classes=config['model']['num_classes'], pretrained=False)
    checkpoint = torch.load(os.path.join(config['train']['save_dir'], 'best_model.pth'),
                            map_location=device)
    model.load_state_dict(checkpoint)
    model = model.to(device)

    acc, cm, report = evaluate(model, test_loader, device, classes)
    print(f'Test Accuracy: {acc*100:.2f}%')
    print('Confusion Matrix:\n', cm)
    print('Classification Report:\n', report)

if __name__ == '__main__':
    main()