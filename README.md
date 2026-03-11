
# Cat vs Dog 图像分类器

一个完整的、工业级别的猫狗图像分类项目，包含数据处理、模型训练、评估以及 RESTful API 部署。该项目使用 MobileNetV2 作为骨干网络，在测试集上达到 98.5% 的准确率，并提供了可交互的 API 服务。

---

##  项目亮点

- **完整的工程结构**：模块化设计，配置与代码分离，易于扩展和维护。

- **可复现的实验管理**：所有超参数保存在配置文件中，训练日志和最佳模型自动归档。

- **开箱即用的 API**：基于 FastAPI 提供 RESTful 服务，支持在线图片预测。

- **专业文档**：清晰的 README 和代码注释，符合工业标准。

---

##  项目结构

cat-dog-classifier/
├── configs/ # 配置文件（训练参数、路径等）
├── data/ # 数据集（训练/验证/测试）
├── src/ # 源代码
│   ├── data/ # 数据加载与预处理
│   ├── models/ # 模型定义
│   ├── training/ # 训练逻辑
│   ├── evaluation/ # 评估指标
│   └── utils/ # 工具函数（配置、日志）
├── scripts/ # 可执行脚本（训练、评估、预测）
├── experiments/ # 实验记录（模型权重、日志）
├── deployments/ # 部署相关
│   └── simple_api/ # FastAPI 服务
├── requirements.txt # 依赖列表
└── README.md # 项目说明

---

##  数据集

- 来源：[Kaggle Dogs vs Cats](https://www.kaggle.com/c/dogs-vs-cats/data)

- 划分：
        

  - 训练集：14000 张（7000 猫 + 7000 狗）

  - 验证集：3000 张（1500 猫 + 1500 狗）

  - 测试集：3000 张（1500 猫 + 1500 狗）

- 预处理：统一缩放到 224×224，采用 ImageNet 归一化，训练集使用随机翻转、旋转等数据增强。

---

##  模型性能

模型

测试准确率

推理速度 (RTX 3050)

模型大小

MobileNetV2

98.5%

~5ms/张

13.6 MB

混淆矩阵：

        预测猫  预测狗
实际猫    1480     20
实际狗     25    1475

分类报告：

              precision    recall  f1-score   support

          猫       0.98      0.99      0.99      1500
          狗       0.99      0.98      0.99      1500

---

##  快速开始

### 环境配置

# 克隆仓库（如果是自己下载的代码，跳过这步）
git clone https://github.com/你的用户名/cat-dog-classifier.git
cd cat-dog-classifier

# 创建 conda 环境
conda create -n catdog python=3.8 -y
conda activate catdog

# 安装依赖
pip install -r requirements.txt

### 训练模型

python scripts/train.py

训练过程中最佳模型会自动保存到 experiments/exp_001/best_model.pth。

### 评估模型

python scripts/evaluate.py

### 启动 API 服务

cd deployments/simple_api
python app.py

服务启动后，访问 http://localhost:8000/docs 即可看到交互式 API 文档。

---

##  API 使用示例

### 请求

- URL: http://localhost:8000/predict

- 方法: POST

- 参数: file（图片文件，支持 jpg/png）

### 响应

{
  "class": "cat"  // 或 "dog"
}

### Python 调用示例

import requests

url = "http://localhost:8000/predict"
files = {"file": open("my_dog.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())  # {'class': 'dog'}

---

## 🛠 后续改进方向

- 尝试更强大的骨干网络（如 ResNet50、EfficientNet）。

- 增加更多数据增强策略（MixUp、CutMix）。

- 部署到云端（如阿里云、AWS），提供公网 API。

- 添加简单的 Web 前端，提升用户体验。

---

##  许可证

本项目采用 MIT 许可证。欢迎 fork 和二次开发。

---

##  致谢

感谢 PyTorch 和 FastAPI 社区提供的优秀工具。感谢你对此项目的关注！
