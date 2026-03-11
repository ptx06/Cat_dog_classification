import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))  # 添加项目根目录

from fastapi import FastAPI, File, UploadFile
import torch
import torchvision.transforms as T
from PIL import Image
import io
import uvicorn

from src.models.model import build_model

app = FastAPI()

# 加载模型和配置
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = build_model(num_classes=2, pretrained=False)
model.load_state_dict(torch.load('experiments/exp_001/best_model.pth', map_location=device))
model.to(device)
model.eval()

# 定义与训练一致的transform
transform = T.Compose([
    T.Resize(256),
    T.CenterCrop(224),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

class_names = ['cat', 'dog']  # 与训练时一致

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    input_tensor = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(input_tensor)
        _, pred = torch.max(outputs, 1)
    return {"class": class_names[pred.item()]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)