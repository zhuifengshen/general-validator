#!/bin/bash
# -*- coding: utf-8 -*-
# 自动化发布脚本 (Shell版本)，功能：编译、打包、上传发布、自动打标签和推送标签

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYPROJECT_FILE="$PROJECT_ROOT/pyproject.toml"
VERSION_FILE="$PROJECT_ROOT/src/data_checker/__init__.py"

# 日志函数
log_info() {
    echo -e "${BLUE}🔄 $1${NC}"
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

# 显示帮助信息
show_help() {
    cat << EOF
Data-checker 自动化发布脚本

用法: $0 [选项]

选项:
    -v, --version VERSION    指定新版本号
    -t, --test              发布到 Test PyPI
    -s, --skip-tests        跳过测试
    -m, --message MESSAGE   标签消息
    -h, --help              显示此帮助信息

示例:
    $0 -v 2.8.4                    # 发布版本 2.8.4
    $0 -v 2.8.4 -t                 # 发布到 Test PyPI
    $0 -v 2.8.4 -m "修复重要bug"    # 带自定义标签消息
    $0 -v 2.8.4 -s                 # 跳过测试
EOF
}

# 获取当前版本号
get_current_version() {
    if [[ -f "$VERSION_FILE" ]]; then
        grep -o '__version__ = "[^"]*"' "$VERSION_FILE" | cut -d'"' -f2
    elif [[ -f "$PYPROJECT_FILE" ]]; then
        grep -o 'version = "[^"]*"' "$PYPROJECT_FILE" | cut -d'"' -f2
    else
        log_error "无法找到版本文件"
        exit 1
    fi
}

# 更新版本号
update_version() {
    local new_version="$1"
    log_info "更新版本号到: $new_version"
    
    # 更新 __init__.py
    if [[ -f "$VERSION_FILE" ]]; then
        sed -i.bak "s/__version__ = \"[^\"]*\"/__version__ = \"$new_version\"/" "$VERSION_FILE"
        rm -f "$VERSION_FILE.bak"
        log_success "已更新 $VERSION_FILE"
    fi
    
    # 更新 pyproject.toml
    if [[ -f "$PYPROJECT_FILE" ]]; then
        sed -i.bak "s/version = \"[^\"]*\"/version = \"$new_version\"/" "$PYPROJECT_FILE"
        rm -f "$PYPROJECT_FILE.bak"
        log_success "已更新 $PYPROJECT_FILE"
    fi
}

# 检查Git状态
check_git_status() {
    log_info "检查Git状态..."
    
    # 检查是否有未提交的更改
    if [[ -n "$(git status --porcelain)" ]]; then
        log_warning "检测到未提交的更改:"
        git status --porcelain
        read -p "是否继续发布? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_error "发布已取消"
            exit 1
        fi
    fi
    
    # 显示当前分支
    local current_branch=$(git branch --show-current)
    log_info "当前分支: $current_branch"
}

# 运行测试
run_tests() {
    log_info "运行测试..."
    
    # 创建临时文件存储测试输出
    local test_output=$(mktemp)
    local test_error=$(mktemp)
    
    # 运行测试并捕获输出
    if python -m unittest discover tests/ > "$test_output" 2> "$test_error"; then
        log_success "测试通过"
        # 清理临时文件
        rm -f "$test_output" "$test_error"
    else
        log_error "测试失败"
        echo ""
        echo "测试输出:"
        tail -20 "$test_output" 2>/dev/null || echo "无标准输出"
        echo ""
        echo "错误信息:"
        tail -10 "$test_error" 2>/dev/null || echo "无错误输出"
        echo ""
        
        # 清理临时文件
        rm -f "$test_output" "$test_error"
        
        read -p "测试失败，是否继续发布? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# 清理构建文件
clean_build() {
    log_info "清理构建文件..."
    rm -rf build/ dist/ *.egg-info/
    log_success "构建文件已清理"
}

# 构建包
build_package() {
    log_info "构建包..."
    
    if ! poetry build; then
        log_error "构建失败"
        exit 1
    fi
    
    # 检查构建结果
    if [[ ! -d "dist" ]] || [[ -z "$(ls dist/*.whl 2>/dev/null)" ]]; then
        log_error "构建失败，未找到构建文件"
        exit 1
    fi
    
    log_success "包构建完成"
}

# 发布包
publish_package() {
    local test_pypi="$1"
    
    if [[ "$test_pypi" == "true" ]]; then
        log_info "发布包到 Test PyPI..."
        if poetry publish --repository testpypi; then
            log_success "包发布到 Test PyPI 成功"
            return 0
        else
            log_error "包发布到 Test PyPI 失败"
            return 1
        fi
    else
        log_info "发布包到 PyPI..."
        if poetry publish; then
            log_success "包发布到 PyPI 成功"
            return 0
        else
            log_error "包发布到 PyPI 失败"
            return 1
        fi
    fi
}

# 创建并推送标签
create_and_push_tag() {
    local version="$1"
    local message="$2"
    local tag_name="v$version"
    
    log_info "创建标签: $tag_name"
    
    # 检查标签是否已存在
    if git tag -l "$tag_name" | grep -q "$tag_name"; then
        log_warning "标签 $tag_name 已存在"
        read -p "是否删除现有标签并重新创建? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git tag -d "$tag_name"
            git push origin ":refs/tags/$tag_name" 2>/dev/null || true
        else
            log_error "标签创建已取消"
            return 1
        fi
    fi
    
    # 创建标签
    if [[ -n "$message" ]]; then
        git tag -a "$tag_name" -m "$message"
    else
        git tag -a "$tag_name" -m "发布版本 $tag_name"
    fi
    
    # 推送标签
    git push origin "$tag_name"
    
    log_success "标签 $tag_name 创建并推送成功"
}

# 提交版本更改
commit_version_changes() {
    local version="$1"
    log_info "提交版本更改..."
    
    # 添加更改的文件
    [[ -f "$VERSION_FILE" ]] && git add "${VERSION_FILE##$PROJECT_ROOT/}"
    [[ -f "$PYPROJECT_FILE" ]] && git add "$(basename "$PYPROJECT_FILE")"
    
    # 提交更改
    git commit -m "chore: bump version to $version"
    
    # 推送更改
    git push
    
    log_success "版本更改已提交并推送"
}

# 主发布流程
release() {
    local new_version="$1"
    local test_pypi="$2"
    local skip_tests="$3"
    local tag_message="$4"
    
    echo -e "${BLUE}🚀 开始自动化发布流程...${NC}"
    
    # 切换到项目根目录
    cd "$PROJECT_ROOT"
    
    # 1. 检查Git状态
    check_git_status
    
    # 2. 获取当前版本
    local current_version=$(get_current_version)
    log_info "当前版本: $current_version"
    
    # 3. 确定新版本号
    if [[ -z "$new_version" ]]; then
        echo "请输入新版本号 (当前版本: $current_version)"
        read -p "新版本号: " new_version
        if [[ -z "$new_version" ]]; then
            log_error "版本号不能为空"
            exit 1
        fi
    fi
    
    log_info "目标版本: $new_version"
    
    # 4. 运行测试
    if [[ "$skip_tests" != "true" ]]; then
        run_tests
    fi
    
    # 5. 更新版本号
    update_version "$new_version"
    
    # 6. 提交版本更改
    commit_version_changes "$new_version"
    
    # 7. 清理构建文件
    clean_build
    
    # 8. 构建包
    build_package
    
    # 9. 发布包
    if publish_package "$test_pypi"; then
        # 10. 创建并推送标签
        create_and_push_tag "$new_version" "$tag_message"
        
        echo -e "${GREEN}🎉 发布流程完成!${NC}"
        log_success "版本 $new_version 已成功发布"
        
        if [[ "$test_pypi" == "true" ]]; then
            echo -e "${BLUE}📦 测试安装命令:${NC}"
            echo "pip install -i https://test.pypi.org/simple/ data-checker==$new_version"
        else
            echo -e "${BLUE}📦 安装命令:${NC}"
            echo "pip install data-checker==$new_version"
        fi
    else
        log_error "发布失败"
        exit 1
    fi
}

# 解析命令行参数
NEW_VERSION=""
TEST_PYPI="false"
SKIP_TESTS="false"
TAG_MESSAGE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--version)
            NEW_VERSION="$2"
            shift 2
            ;;
        -t|--test)
            TEST_PYPI="true"
            shift
            ;;
        -s|--skip-tests)
            SKIP_TESTS="true"
            shift
            ;;
        -m|--message)
            TAG_MESSAGE="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            log_error "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
done

# 执行发布流程
release "$NEW_VERSION" "$TEST_PYPI" "$SKIP_TESTS" "$TAG_MESSAGE" 