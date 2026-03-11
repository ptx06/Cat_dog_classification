import os
from pathlib import Path
import argparse

def count_files_folders_recursive(root_path):
    """
    递归统计文件夹内的文件和子文件夹数量（含所有层级）
    :param root_path: 目标文件夹路径（str/Path对象）
    :return: 统计结果字典 {
        'total_files': 总文件数,
        'total_folders': 总文件夹数,
        'details': 各目录的详细统计列表
    }
    """
    root_path = Path(root_path).resolve()
    if not root_path.is_dir():
        raise ValueError(f"错误：{root_path} 不是有效的文件夹路径！")

    # 初始化统计结果
    stats = {
        "total_files": 0,
        "total_folders": 0,
        "details": []
    }

    # 递归遍历所有目录
    for dir_path, dir_names, file_names in os.walk(root_path):
        # 转换为Path对象，方便处理
        dir_path = Path(dir_path)
        # 当前目录的层级（根目录为0级）
        level = len(dir_path.relative_to(root_path).parts)
        # 缩进，用于格式化输出
        indent = "  " * level

        # 统计当前目录的文件夹数和文件数
        curr_folder_count = len(dir_names)
        curr_file_count = len(file_names)

        # 累计到总数（总文件夹数需包含当前目录）
        stats["total_folders"] += 1  # 当前目录本身算一个文件夹
        stats["total_files"] += curr_file_count

        # 记录当前目录的详情
        stats["details"].append({
            "path": str(dir_path),
            "level": level,
            "indent": indent,
            "current_folder": dir_path.name,
            "subfolders_count": curr_folder_count,
            "files_count": curr_file_count
        })

    return stats

def print_stats(stats, root_path):
    """
    格式化输出统计结果
    :param stats: count_files_folders_recursive 返回的统计字典
    :param root_path: 目标根路径
    """
    print("=" * 80)
    print(f"📁 目标文件夹：{root_path}")
    print("=" * 80)
    print(f"📊 总统计结果：")
    print(f"   总文件夹数（含所有层级）：{stats['total_folders']}")
    print(f"   总文件数（含所有层级）：{stats['total_files']}")
    print("=" * 80)
    print(f"📋 各目录详细统计（层级缩进展示）：")
    print("-" * 80)

    for detail in stats["details"]:
        print(f"{detail['indent']}📂 {detail['current_folder']} "
              f"(路径：{detail['path']})")
        print(f"{detail['indent']}  ├─ 子文件夹数：{detail['subfolders_count']}")
        print(f"{detail['indent']}  └─ 文件数：{detail['files_count']}")
    print("=" * 80)

if __name__ == "__main__":
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="递归统计文件夹内的文件和子文件夹数量（含所有层级）")
    parser.add_argument("folder_path", type=str, help="要统计的文件夹路径（绝对路径/相对路径均可）")
    args = parser.parse_args()

    try:
        # 执行统计（修正：用 args.folder_path 而非 args.data）
        stats_result = count_files_folders_recursive(args.folder_path)
        # 格式化输出
        print_stats(stats_result, args.folder_path)
    except Exception as e:
        print(f"❌ 执行出错：{e}")