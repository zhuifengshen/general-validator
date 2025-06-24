#!/bin/bash
# Poetry 发布环境配置脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

echo -e "${BLUE}🔧 Poetry 发布环境配置向导${NC}"
echo ""

# 检查 Poetry 是否已安装
if ! command -v poetry &> /dev/null; then
    log_error "Poetry 未安装，请先安装 Poetry"
    echo "安装命令: curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

log_success "Poetry 已安装: $(poetry --version)"

# 配置 PyPI Token
echo ""
log_info "配置 PyPI 认证信息"
echo "请访问 https://pypi.org/manage/account/token/ 创建 API Token"
echo ""

read -p "请输入您的 PyPI API Token (或按回车跳过): " -s pypi_token
echo ""

if [[ -n "$pypi_token" ]]; then
    poetry config pypi-token.pypi "$pypi_token"
    log_success "PyPI Token 配置完成"
else
    log_warning "跳过 PyPI Token 配置"
fi

# 配置 Test PyPI (可选)
echo ""
read -p "是否配置 Test PyPI? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    log_info "配置 Test PyPI"
    echo "请访问 https://test.pypi.org/manage/account/token/ 创建 Test PyPI Token"
    echo ""
    
    read -p "请输入您的 Test PyPI API Token: " -s test_pypi_token
    echo ""
    
    if [[ -n "$test_pypi_token" ]]; then
        poetry config repositories.testpypi https://test.pypi.org/legacy/
        poetry config pypi-token.testpypi "$test_pypi_token"
        log_success "Test PyPI Token 配置完成"
    else
        log_warning "Test PyPI Token 为空，跳过配置"
    fi
fi

# 显示当前配置
echo ""
log_info "当前 Poetry 配置:"
poetry config --list | grep -E "(pypi-token|repositories)" || echo "  无相关配置"

# 验证配置
echo ""
log_info "验证配置..."

# 检查项目依赖
if [[ -f "pyproject.toml" ]]; then
    log_success "找到 pyproject.toml 文件"
    
    # 安装依赖
    log_info "安装项目依赖..."
    poetry install
    log_success "依赖安装完成"
    
    # 尝试构建
    log_info "测试构建..."
    poetry build --dry-run
    log_success "构建测试通过"
else
    log_warning "未找到 pyproject.toml 文件"
fi

echo ""
log_success "Poetry 配置完成！"
echo ""
echo "现在您可以使用以下命令进行发布:"
echo "  make release VERSION=x.x.x    # 发布到 PyPI"
echo "  make release-test VERSION=x.x.x  # 发布到 Test PyPI"
echo "  ./scripts/release.sh -h       # 查看更多选项" 