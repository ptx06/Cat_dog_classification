import os
import shutil
import random
from pathlib import Path

def create_val_set(train_dir, val_dir, val_ratio=0.1, random_seed=42):
    """
    从训练集拆分验证集
    :param train_dir: 训练集根目录（如 ./data/train）
    :param val_dir: 验证集根目录（如 ./data/val）
    :param val_ratio: 验证集占训练集的比例
    :param random_seed: 随机种子（保证拆分结果可复现）
    """
    # 固定随机种子
    random.seed(random_seed)
    
    # 定义类别（cats/dogs）
    classes = ["cats", "dogs"]
    
    # 创建验证集目录
    val_dir = Path(val_dir)
    for cls in classes:
        cls_val_dir = val_dir / cls
        cls_val_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ 创建验证集目录：{cls_val_dir}")
    
    # 遍历每个类别，拆分文件
    for cls in classes:
        # 训练集类别目录
        cls_train_dir = Path(train_dir) / cls
        # 获取该类别下所有文件（过滤隐藏文件）
        all_files = [f for f in os.listdir(cls_train_dir) if not f.startswith('.')]
        # 计算验证集文件数量
        val_num = int(len(all_files) * val_ratio)
        # 随机选择验证集文件
        val_files = random.sample(all_files, val_num)
        # 训练集剩余文件
        train_remain_files = [f for f in all_files if f not in val_files]
        
        print(f"\n📌 类别 {cls}：")
        print(f"   训练集总数：{len(all_files)}")
        print(f"   拆分验证集数量：{val_num}")
        print(f"   剩余训练集数量：{len(train_remain_files)}")
        
        # 复制文件到验证集
        for file_name in val_files:
            src_path = cls_train_dir / file_name
            dst_path = val_dir / cls / file_name
            shutil.copy2(src_path, dst_path)  # copy2 保留文件元信息
            # 如需从训练集移除验证集文件，取消下面注释：
            # os.remove(src_path)
        
        print(f"✅ 已将 {val_num} 个 {cls} 文件复制到验证集")

if __name__ == "__main__":
    # 配置路径（适配你的项目结构）
    train_dir = "/root/autodl-tmp/Cat_dog_classification/data/train"
    val_dir = "/root/autodl-tmp/Cat_dog_classification/data/val"
    
    # 执行拆分（验证集比例 10%）
    create_val_set(train_dir, val_dir, val_ratio=0.1, random_seed=42)
    
    print("\n🎉 验证集构造完成！")
    print(f"验证集路径：{val_dir}")
    print("可运行之前的 folder_show.py 脚本查看验证集文件数量。")