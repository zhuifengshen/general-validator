# Data-checker 项目 Makefile，提供便捷的开发和发布命令

.PHONY: help install test clean build release release-test release-major release-minor release-patch

# 默认目标
help:
	@echo "命令使用说明"
	@echo ""
	@echo "开发命令:"
	@echo "  install       安装项目依赖"
	@echo "  test          运行测试"
	@echo "  clean         清理构建文件"
	@echo "  build         构建包"
	@echo ""
	@echo "发布命令:"
	@echo "  release       交互式发布 (需要手动输入版本号)"
	@echo "  release-test  发布到 Test PyPI"
	@echo "  release-patch 发布补丁版本 (x.x.X)"
	@echo "  release-minor 发布次要版本 (x.X.0)"
	@echo "  release-major 发布主要版本 (X.0.0)"
	@echo ""
	@echo "自定义发布:"
	@echo "  make release VERSION=2.8.4"
	@echo "  make release-test VERSION=2.8.4"
	@echo "  make release VERSION=2.8.4 MESSAGE='修复重要bug'"
	@echo ""

# 安装依赖
install:
	@echo "📦 安装项目依赖..."
	poetry install

# 运行测试
test:
	@echo "🧪 运行测试..."
	python -m unittest discover tests/

# 清理构建文件
clean:
	@echo "🧹 清理构建文件..."
	rm -rf build/ dist/ *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

# 构建包
build: clean
	@echo "📦 构建包..."
	poetry build

# 获取当前版本号
current-version:
	@python -c "import re; content=open('src/data_checker/__init__.py').read(); print(re.search(r'__version__ = \"([^\"]+)\"', content).group(1))"

# 计算下一个版本号
next-patch:
	@python -c "import re; content=open('src/data_checker/__init__.py').read(); version=re.search(r'__version__ = \"([^\"]+)\"', content).group(1); parts=version.split('.'); parts[2]=str(int(parts[2])+1); print('.'.join(parts))"

next-minor:
	@python -c "import re; content=open('src/data_checker/__init__.py').read(); version=re.search(r'__version__ = \"([^\"]+)\"', content).group(1); parts=version.split('.'); parts[1]=str(int(parts[1])+1); parts[2]='0'; print('.'.join(parts))"

next-major:
	@python -c "import re; content=open('src/data_checker/__init__.py').read(); version=re.search(r'__version__ = \"([^\"]+)\"', content).group(1); parts=version.split('.'); parts[0]=str(int(parts[0])+1); parts[1]='0'; parts[2]='0'; print('.'.join(parts))"

# 交互式发布
release:
ifdef VERSION
	@echo "🚀 发布版本 $(VERSION)..."
ifdef MESSAGE
	./scripts/release.sh -v $(VERSION) -m "$(MESSAGE)"
else
	./scripts/release.sh -v $(VERSION)
endif
else
	@echo "🚀 交互式发布..."
	./scripts/release.sh
endif

# 发布到 Test PyPI
release-test:
ifdef VERSION
	@echo "🚀 发布版本 $(VERSION) 到 Test PyPI..."
ifdef MESSAGE
	./scripts/release.sh -v $(VERSION) -t -m "$(MESSAGE)"
else
	./scripts/release.sh -v $(VERSION) -t
endif
else
	@echo "🚀 交互式发布到 Test PyPI..."
	./scripts/release.sh -t
endif

# 发布补丁版本
release-patch:
	@echo "🚀 发布补丁版本..."
	$(eval NEXT_VERSION := $(shell make next-patch))
ifdef MESSAGE
	./scripts/release.sh -v $(NEXT_VERSION) -m "$(MESSAGE)"
else
	./scripts/release.sh -v $(NEXT_VERSION) -m "发布补丁版本 v$(NEXT_VERSION)"
endif

# 发布次要版本
release-minor:
	@echo "🚀 发布次要版本..."
	$(eval NEXT_VERSION := $(shell make next-minor))
ifdef MESSAGE
	./scripts/release.sh -v $(NEXT_VERSION) -m "$(MESSAGE)"
else
	./scripts/release.sh -v $(NEXT_VERSION) -m "发布次要版本 v$(NEXT_VERSION)"
endif

# 发布主要版本
release-major:
	@echo "🚀 发布主要版本..."
	$(eval NEXT_VERSION := $(shell make next-major))
ifdef MESSAGE
	./scripts/release.sh -v $(NEXT_VERSION) -m "$(MESSAGE)"
else
	./scripts/release.sh -v $(NEXT_VERSION) -m "发布主要版本 v$(NEXT_VERSION)"
endif

# 检查发布前的状态
pre-release-check:
	@echo "🔍 发布前检查..."
	@echo "当前版本: $(shell make current-version)"
	@echo "Git状态:"
	@git status --porcelain || echo "  工作目录干净"
	@echo "当前分支: $(shell git branch --show-current)"
	@echo "最近的标签: $(shell git describe --tags --abbrev=0 2>/dev/null || echo '无标签')"

# 显示发布历史
release-history:
	@echo "📋 发布历史:"
	@git tag -l "v*" --sort=-version:refname | head -10

# 快速发布命令 (跳过测试)
quick-release:
ifdef VERSION
	@echo "⚡ 快速发布版本 $(VERSION) (跳过测试)..."
ifdef MESSAGE
	./scripts/release.sh -v $(VERSION) -s -m "$(MESSAGE)"
else
	./scripts/release.sh -v $(VERSION) -s
endif
else
	@echo "❌ 请指定版本号: make quick-release VERSION=x.x.x"
endif 