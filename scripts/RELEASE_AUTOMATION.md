# 自动化发布系统

## 📋 概述

自动化发布系统，实现一键完成编译、打包、上传发布和自动打标签的完整流程。

## 🎯 核心功能

### ✅ 完整的发布流程自动化
- 🔍 **Git状态检查** - 自动检查工作目录状态和分支信息
- 📝 **版本管理** - 自动更新 `pyproject.toml` 和 `__init__.py` 中的版本号
- 🧪 **自动化测试** - 发布前运行单元测试（可选跳过）
- 🧹 **构建清理** - 自动清理旧的构建文件
- 📦 **包构建** - 使用 Poetry 构建 wheel 和 tar.gz 包
- 🚀 **PyPI发布** - 支持发布到 PyPI 或 Test PyPI
- 🏷️ **自动标签** - 发布成功后自动创建并推送 Git 标签
- 📝 **版本提交** - 自动提交版本更改到 Git 仓库

### ✅ 多种使用方式
- **Makefile** - 最便捷的使用方式，支持语义化版本自动递增
- **Shell脚本** - 轻量级，跨平台兼容性好
- **Python脚本** - 功能最完整，错误处理最详细

## 📁 文件结构

```
├── Makefile                    # 便捷的发布命令
├── scripts/
│   ├── release.py             # Python版本发布脚本（推荐）
│   ├── release.sh             # Shell版本发布脚本
│   ├── setup-poetry.sh        # Poetry环境配置脚本
│   └── README.md              # 详细使用说明
└── RELEASE_AUTOMATION.md      # 本文档
```

## 🚀 快速开始

### 1. 环境配置

```bash
# 配置 Poetry 发布环境
./scripts/setup-poetry.sh

# 或手动配置
poetry config pypi-token.pypi your-pypi-token
```

### 2. 发布命令

```bash
# 最简单的方式 - 使用 Makefile
make release VERSION=2.8.4

# 自动版本递增
make release-patch    # 2.8.3 -> 2.8.4
make release-minor    # 2.8.3 -> 2.9.0
make release-major    # 2.8.3 -> 3.0.0

# 发布到 Test PyPI
make release-test VERSION=2.8.4

# 带自定义消息
make release VERSION=2.8.4 MESSAGE="修复重要bug"
```

## 📊 使用示例

### 场景1：发布补丁版本
```bash
# 当前版本：2.8.3
# 目标：发布 2.8.4 修复bug

make release-patch MESSAGE="修复API响应解析问题"

# 自动执行：
# 1. 版本号更新为 2.8.4
# 2. 运行测试
# 3. 构建包
# 4. 发布到 PyPI
# 5. 创建标签 v2.8.4
# 6. 推送到 Git 仓库
```

### 场景2：发布到测试环境
```bash
# 先在 Test PyPI 测试
make release-test VERSION=2.9.0

# 测试安装
pip install -i https://test.pypi.org/simple/ general-validator==2.9.0

# 确认无问题后发布到正式环境
make release VERSION=2.9.0
```

### 场景3：紧急发布（跳过测试）
```bash
# 紧急修复，跳过测试
make quick-release VERSION=2.8.5
```

## 🔧 高级功能

### 版本号管理
- **自动递增**: `make release-patch/minor/major`
- **语义化版本**: 遵循 SemVer 规范
- **双文件同步**: 同时更新 `pyproject.toml` 和 `__init__.py`

### Git 集成
- **状态检查**: 自动检查未提交的更改
- **分支识别**: 显示当前工作分支
- **自动标签**: 发布成功后创建 `vX.X.X` 格式标签
- **冲突处理**: 智能处理已存在的标签

### 错误处理
- **步骤回滚**: 发布失败时的清理机制
- **详细日志**: 每个步骤的详细输出
- **交互确认**: 关键操作前的用户确认

## 📋 完整命令参考

### Makefile 命令
```bash
make help              # 显示帮助信息
make install           # 安装项目依赖
make test              # 运行测试
make clean             # 清理构建文件
make build             # 构建包
make current-version   # 显示当前版本
make pre-release-check # 发布前检查
make release-history   # 显示发布历史

# 发布命令
make release [VERSION=x.x.x] [MESSAGE="消息"]
make release-test [VERSION=x.x.x] [MESSAGE="消息"]
make release-patch [MESSAGE="消息"]
make release-minor [MESSAGE="消息"]
make release-major [MESSAGE="消息"]
make quick-release VERSION=x.x.x [MESSAGE="消息"]
```

### Shell 脚本参数
```bash
./scripts/release.sh [选项]

选项:
  -v, --version VERSION    指定新版本号
  -t, --test              发布到 Test PyPI
  -s, --skip-tests        跳过测试
  -m, --message MESSAGE   标签消息
  -h, --help              显示帮助信息
```

### Python 脚本参数
```bash
python scripts/release.py [选项]

选项:
  --version VERSION        指定新版本号
  --test                  发布到 Test PyPI
  --skip-tests            跳过测试
  --tag-message MESSAGE   标签消息
  --project-root PATH     项目根目录路径
  --help                  显示帮助信息
```

## 🔒 安全最佳实践

1. **Token 管理**
   - 使用 Poetry 的配置管理 PyPI Token
   - 不在脚本中硬编码认证信息
   - 定期轮换 API Token

2. **发布前检查**
   - 运行完整的测试套件
   - 检查版本号的唯一性
   - 确认更改日志的完整性

3. **权限控制**
   - 限制发布脚本的执行权限
   - 在安全的环境中运行发布流程
   - 记录发布操作的审计日志

## 🐛 故障排除

### 常见问题

1. **PyPI 认证失败**
   ```bash
   # 重新配置 Token
   poetry config pypi-token.pypi your-new-token
   ```

2. **版本号已存在**
   ```bash
   # 使用新的版本号
   make release VERSION=2.8.5
   ```

3. **测试失败**
   ```bash
   # 修复测试或跳过测试
   make quick-release VERSION=2.8.4
   ```

4. **Git 标签冲突**
   ```bash
   # 脚本会自动处理，或手动删除
   git tag -d v2.8.4
   git push origin :refs/tags/v2.8.4
   ```

### 回滚操作

如果发布出现问题：

1. **删除 PyPI 版本**（如果可能）
2. **发布修复版本**
3. **删除错误的 Git 标签**
   ```bash
   git tag -d vX.X.X
   git push origin :refs/tags/vX.X.X
   ```

## 📈 监控和日志

- **发布日志**: 每个步骤的详细输出
- **版本历史**: `make release-history` 查看发布记录
- **状态检查**: `make pre-release-check` 发布前状态检查

## 🔄 持续改进

### 未来增强功能
- [ ] 集成 CI/CD 流水线
- [ ] 自动生成 CHANGELOG
- [ ] 发布通知（Slack/邮件）
- [ ] 回滚自动化
- [ ] 多环境发布支持

### 自定义扩展
脚本设计为模块化，可以轻松扩展：
- 自定义测试命令
- 添加构建后处理
- 集成代码质量检查
- 添加发布通知

## 📞 支持

如果在使用过程中遇到问题：

1. 查看 `scripts/README.md` 详细文档
2. 检查脚本输出的错误信息
3. 提交 Issue 到项目仓库

---

**现在您可以享受一键发布的便利了！** 