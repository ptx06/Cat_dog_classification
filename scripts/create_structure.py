import os

# 核心修改：获取项目根目录（不管脚本放哪，都以根目录为基准）
# 脚本在 scripts/ 里，根目录 = 脚本所在目录的上一级
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# 定义文件夹和文件结构（和之前一致，无需改）
structure = {
    # 根目录文件
    ".gitignore": "",
    "README.md": "",
    "requirements.txt": "",
    "setup.py": "",

    # 文件夹层级
    "configs": {
        "train_config.yaml": ""
    },
    "data": {
        "train": {"cats": {}, "dogs": {}},
        "val": {"cats": {}, "dogs": {}},
        "test": {"cats": {}, "dogs": {}}
    },
    "src": {
        "__init__.py": "",
        "data": {"__init__.py": "", "dataset.py": "", "transforms.py": ""},
        "models": {"__init__.py": "", "model.py": ""},
        "training": {"__init__.py": "", "trainer.py": "", "utils.py": ""},
        "evaluation": {"__init__.py": "", "evaluator.py": ""},
        "utils": {"__init__.py": "", "config.py": "", "logger.py": ""}
    },
    "scripts": {  # 即使已有 scripts 文件夹，也会兼容（exist_ok=True）
        "train.py": "",
        "evaluate.py": "",
        "predict.py": ""
    },
    "experiments": {
        "exp_001": {"config.yaml": "", "checkpoints": {}, "logs": {}}
    },
    "deployments": {
        "simple_api": {"app.py": "", "requirements.txt": ""}
    }
}


# 递归创建文件夹和空文件（基准路径改为 ROOT_DIR）
def create_structure(base_path, structure_dict):
    for name, content in structure_dict.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            # 创建文件夹（exist_ok=True：已有文件夹也不报错）
            os.makedirs(path, exist_ok=True)
            # 递归创建子内容
            create_structure(path, content)
        else:
            # 创建空文件（如果文件已存在，不会覆盖）
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)


if __name__ == "__main__":
    # 以项目根目录为基准创建结构
    create_structure(ROOT_DIR, structure)
    print(f"✅ 文件夹结构创建完成！\n📌 生成路径：{ROOT_DIR}")