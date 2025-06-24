# 自动化发布脚本使用说明

项目自动化发布脚本，支持一键完成编译、打包、上传发布和自动打标签的完整流程。

## 脚本文件

- `release.py` - Python版本的发布脚本（功能最完整）
- `release.sh` - Shell版本的发布脚本（轻量级）
- `README.md` - 本说明文档

## 功能特性

✅ **自动版本管理** - 自动更新 `pyproject.toml` 和 `__init__.py` 中的版本号  
✅ **Git状态检查** - 检查未提交的更改和当前分支状态  
✅ **自动化测试** - 发布前运行单元测试（可跳过）  
✅ **构建清理** - 自动清理旧的构建文件  
✅ **包构建** - 使用 Poetry 构建 wheel 和 tar.gz 包  
✅ **PyPI发布** - 支持发布到 PyPI 或 Test PyPI  
✅ **自动标签** - 发布成功后自动创建并推送 Git 标签  
✅ **版本提交** - 自动提交版本更改到 Git 仓库  

## 使用方法

### 1. 使用 Makefile（推荐）

项目根目录提供了 Makefile，这是最便捷的使用方式：

```bash
# 查看所有可用命令
make help

# 交互式发布（会提示输入版本号）
make release

# 指定版本号发布
make release VERSION=2.8.4

# 发布到 Test PyPI
make release-test VERSION=2.8.4

# 自动计算版本号发布
make release-patch    # 补丁版本 (2.8.3 -> 2.8.4)
make release-minor    # 次要版本 (2.8.3 -> 2.9.0)
make release-major    # 主要版本 (2.8.3 -> 3.0.0)

# 带自定义标签消息
make release VERSION=2.8.4 MESSAGE="修复重要bug"

# 快速发布（跳过测试）
make quick-release VERSION=2.8.4
```

### 2. 直接使用 Shell 脚本

```bash
# 交互式发布
./scripts/release.sh

# 指定版本号发布
./scripts/release.sh -v 2.8.4

# 发布到 Test PyPI
./scripts/release.sh -v 2.8.4 -t

# 跳过测试
./scripts/release.sh -v 2.8.4 -s

# 自定义标签消息
./scripts/release.sh -v 2.8.4 -m "修复重要bug"

# 查看帮助
./scripts/release.sh -h
```

### 3. 使用 Python 脚本

```bash
# 交互式发布
python scripts/release.py

# 指定版本号发布
python scripts/release.py --version 2.8.4

# 发布到 Test PyPI
python scripts/release.py --version 2.8.4 --test

# 跳过测试
python scripts/release.py --version 2.8.4 --skip-tests

# 自定义标签消息
python scripts/release.py --version 2.8.4 --tag-message "修复重要bug"

# 查看帮助
python scripts/release.py --help
```

## 发布流程

脚本会按以下顺序执行发布流程：

1. **🔍 检查Git状态** - 确认工作目录状态和当前分支
2. **📋 获取当前版本** - 从版本文件读取当前版本号
3. **🎯 确定新版本** - 指定或交互输入新版本号
4. **🧪 运行测试** - 执行单元测试（可跳过）
5. **📝 更新版本号** - 更新相关文件中的版本号
6. **📝 提交版本更改** - 提交版本更改到Git仓库
7. **🧹 清理构建文件** - 删除旧的构建产物
8. **📦 构建包** - 使用Poetry构建wheel和tar.gz包
9. **🚀 发布包** - 上传到PyPI或Test PyPI
10. **🏷️ 创建标签** - 创建并推送Git标签

## 配置要求

### Poetry 配置

确保已配置 Poetry 的 PyPI 认证信息：

```bash
# 配置 PyPI 认证
poetry config pypi-token.pypi your-pypi-token

# 配置 Test PyPI 认证（可选）
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi your-test-pypi-token
```

### Git 配置

确保 Git 已配置用户信息：

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 版本号规范

脚本支持语义化版本号（Semantic Versioning）：

- **主版本号（Major）**: 不兼容的API修改
- **次版本号（Minor）**: 向下兼容的功能性新增
- **修订号（Patch）**: 向下兼容的问题修正

示例：`2.8.3` -> `2.8.4`（补丁版本）

## 常见问题

### Q: 发布失败怎么办？

A: 脚本会在每个步骤显示详细的错误信息。常见问题：
- PyPI认证失败：检查token配置
- 版本号已存在：使用新的版本号
- 测试失败：修复测试或使用 `-s` 跳过测试

### Q: 如何回滚发布？

A: 如果发布有问题，可以：
1. 从PyPI删除有问题的版本（如果可能）
2. 发布一个修复版本
3. 删除对应的Git标签：`git tag -d vX.X.X && git push origin :refs/tags/vX.X.X`

### Q: 可以只构建不发布吗？

A: 可以使用 `make build` 或 `poetry build` 只构建包而不发布。

### Q: 如何查看发布历史？

A: 使用 `make release-history` 查看最近的发布标签。

## 安全注意事项

- 🔐 不要在脚本中硬编码认证信息
- 🔐 使用 Poetry 的 token 配置管理 PyPI 认证
- 🔐 确保在安全的环境中运行发布脚本
- 🔐 发布前仔细检查版本号和更改内容

## 自定义配置

如果需要自定义发布流程，可以修改脚本中的相关函数：

- `run_tests()` - 自定义测试命令
- `build_package()` - 自定义构建流程
- `publish_package()` - 自定义发布逻辑

## 支持与反馈

如果在使用过程中遇到问题，请：

1. 检查本文档的常见问题部分
2. 查看脚本的详细错误输出
3. 提交 Issue 到项目仓库 