"""
LFS文件加载脚本 - 用于Streamlit Cloud
在Streamlit Cloud上，git clone不会自动下载LFS文件。
这个脚本会检测并下载LFS指针文件指向的实际数据。
"""
import os
import subprocess
import sys
from pathlib import Path


def setup_git_lfs():
    """在Streamlit Cloud上设置Git LFS支持"""
    try:
        # 检查是否在云环境中
        if os.path.exists('/.streamlit'):
            print("检测到Streamlit Cloud环境，正在配置Git LFS...")
            
            # 安装git lfs（如果需要）
            try:
                subprocess.run(['git', 'lfs', 'version'], 
                             capture_output=True, check=True)
                print("✓ Git LFS已安装")
            except:
                print("正在安装Git LFS...")
                subprocess.run(['apt-get', 'update'], 
                             capture_output=True, check=False)
                subprocess.run(['apt-get', 'install', '-y', 'git-lfs'], 
                             capture_output=True, check=False)
            
            # 初始化并pull LFS文件
            try:
                subprocess.run(['git', 'lfs', 'install'], 
                             capture_output=True, check=False)
                subprocess.run(['git', 'lfs', 'pull'], 
                             capture_output=True, check=True)
                print("✓ Git LFS文件已拉取")
                return True
            except Exception as e:
                print(f"⚠ Git LFS拉取失败: {e}")
                return False
    except Exception as e:
        print(f"设置Git LFS时出错: {e}")
        return False


def check_lfs_files():
    """检查LFS文件是否正确加载"""
    pkl_files = list(Path('.').glob('RSF_*.pkl'))
    
    for pkl_file in pkl_files:
        size = pkl_file.stat().st_size
        # LFS指针文件通常只有几百字节
        if size < 1000:
            print(f"⚠ {pkl_file.name} 似乎是LFS指针文件（{size}字节），不是实际数据")
            return False
        else:
            print(f"✓ {pkl_file.name} 已正确加载（{size/1e6:.1f}MB）")
    
    return len(pkl_files) > 0


if __name__ == '__main__':
    print("=" * 60)
    print("Git LFS设置脚本")
    print("=" * 60)
    
    setup_git_lfs()
    
    if not check_lfs_files():
        print("\n⚠ 警告：PKL文件可能未正确加载！")
        print("解决方案:")
        print("1. 确保在Streamlit Cloud上启用了Git LFS")
        print("2. 或使用云存储来存储模型文件")
        sys.exit(1)
    else:
        print("\n✓ 所有文件都已正确加载！")
        sys.exit(0)
