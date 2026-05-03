# GIST RSF Survival Prediction App

## Overview
这是一个基于Streamlit的GIST（胃肠间质瘤）生存风险预测应用，支持OS（整体生存）和CSS（癌症特异性生存）两种预测任务。

## Features
- 📊 **两个预测模型**: OS和CSS任务
- 🔥 **SHAP特征解释**: 可视化特征对预测的影响
- 🎯 **自适应表单**: 根据选择的任务动态调整输入字段
- 📈 **生存概率计算**: 1年、3年、5年生存率预测

## 本地运行

### 前置条件
- Python 3.8+
- Git LFS（用于处理大文件）

### 安装与运行

1. **克隆仓库**（并拉取LFS文件）：
```bash
git clone https://github.com/Mosheris/GIST-OSCSS.git
cd GIST-OSCSS
git lfs pull
```

2. **安装依赖**：
```bash
pip install -r requirements.txt
```

3. **运行应用**：
```bash
streamlit run app.py
```

4. **访问应用**：
打开浏览器访问 `http://localhost:8501`

## Streamlit Cloud 部署

### 重要：处理Git LFS文件

Streamlit Cloud默认不支持Git LFS。请按以下步骤操作：

#### 方法1：在部署配置中启用LFS（推荐）

在Streamlit Cloud部署应用时，在"高级设置"中添加以下环境变量：
```
GIT_LFS_SKIP_SMUDGE=0
```

然后在"启动命令"中添加：
```bash
git lfs pull && streamlit run app.py
```

#### 方法2：使用 `packages.txt`

项目已包含 `packages.txt` 文件，会自动安装 `git-lfs`。

### 部署步骤

1. **将代码推送到GitHub**：
```bash
git push origin main
```

2. **在Streamlit Cloud上连接**：
- 访问 https://share.streamlit.io/
- 点击 "New app"
- 选择GitHub仓库: `Mosheris/GIST-OSCSS`
- 主文件路径: `app.py`
- 在"高级设置"中配置环境变量和启动命令

3. **监控部署**：
- 应用会自动在首次启动时拉取LFS文件
- 如果出现模型加载错误，检查日志中的LFS设置信息

## 文件结构

```
.
├── app.py                  # Streamlit主应用
├── setup_lfs.py           # Git LFS初始化脚本
├── requirements.txt       # Python依赖
├── packages.txt          # 系统依赖（apt）
├── feature_names.json    # 特征映射配置
├── .gitattributes        # Git LFS配置
├── .streamlit/           # Streamlit配置
│   └── config.toml
└── RSF_*.pkl             # 训练的模型文件（Git LFS）
    ├── RSF_OS.pkl        # OS任务模型 (~30MB)
    └── RSF_CSS.pkl       # CSS任务模型 (~76MB)
```

## 特征矩阵

### OS模型（10个特征）
- Age, Tumor.size, Race.1, Race.2
- Marital.status.1, Marital.status.2
- Gender, Site, Mitotic.rate, Liver.metastasis

### CSS模型（9个特征）
- Age, Tumor.size, Race.1, Race.2
- Gender, Site, Mitotic.rate, Liver.metastasis
- Systemic.treatment

## 故障排除

### 问题：`ModuleNotFoundError: No module named 'streamlit'`
**解决方案**：运行 `pip install -r requirements.txt`

### 问题：`pickle.UnpicklingError` 或模型文件大小异常
**原因**：Git LFS文件未正确加载（通常是Streamlit Cloud问题）

**解决方案**：
1. 确保在部署时启用了 `git lfs pull` 命令
2. 检查应用日志中的LFS相关错误
3. 在本地重新克隆并运行 `git lfs pull`

### 问题：应用启动缓慢
**原因**：首次启动时加载大模型文件

**解决方案**：这是正常的，LFS文件会被缓存，后续启动会更快

## API使用示例

如需集成到其他应用，可以直接加载模型：

```python
import pickle
from pathlib import Path

# 加载模型
model_file = Path("RSF_OS.pkl")
with open(model_file, 'rb') as f:
    model_pkg = pickle.load(f)

model = model_pkg["model"]
features = model_pkg["feature_cols"]

# 预测
import numpy as np
input_data = np.array([[60, 30, 0, 0, 1, 0, 1, 1, 50, 0]])  # 示例数据
risk_score = model.predict(input_data)
```

## 许可证
MIT

## 联系方式
For questions or issues, please contact: [your-email]