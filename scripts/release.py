#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化发布脚本
功能：编译、打包、上传发布、自动打标签和推送标签
"""

import sys
import subprocess
import re
import argparse
from pathlib import Path
from typing import Tuple


class ReleaseManager:
    """发布管理器"""
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.pyproject_path = self.project_root / "pyproject.toml"
        self.version_file = self.project_root / "src" / "data_checker" / "__init__.py"
        
    def run_command(self, command: str, check: bool = True) -> Tuple[int, str, str]:
        """执行命令并返回结果"""
        print(f"🔄 执行命令: {command}")
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True,
                cwd=self.project_root
            )
            
            if result.stdout:
                print(f"📤 输出: {result.stdout.strip()}")
            if result.stderr and result.returncode != 0:
                print(f"❌ 错误: {result.stderr.strip()}")
                
            if check and result.returncode != 0:
                raise subprocess.CalledProcessError(result.returncode, command)
                
            return result.returncode, result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            print(f"❌ 命令执行失败: {e}")
            sys.exit(1)
    
    def get_current_version(self) -> str:
        """获取当前版本号"""
        try:
            # 从 __init__.py 获取版本号
            if self.version_file.exists():
                content = self.version_file.read_text(encoding='utf-8')
                match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
                if match:
                    return match.group(1)
            
            # 从 pyproject.toml 获取版本号
            if self.pyproject_path.exists():
                content = self.pyproject_path.read_text(encoding='utf-8')
                match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
                if match:
                    return match.group(1)
                    
            raise ValueError("无法找到版本号")
        except Exception as e:
            print(f"❌ 获取版本号失败: {e}")
            sys.exit(1)
    
    def update_version(self, new_version: str):
        """更新版本号"""
        print(f"📝 更新版本号到: {new_version}")
        
        # 更新 __init__.py
        if self.version_file.exists():
            content = self.version_file.read_text(encoding='utf-8')
            new_content = re.sub(
                r'__version__\s*=\s*["\'][^"\']+["\']',
                f'__version__ = "{new_version}"',
                content
            )
            self.version_file.write_text(new_content, encoding='utf-8')
            print(f"✅ 已更新 {self.version_file}")
        
        # 更新 pyproject.toml
        if self.pyproject_path.exists():
            content = self.pyproject_path.read_text(encoding='utf-8')
            new_content = re.sub(
                r'version\s*=\s*["\'][^"\']+["\']',
                f'version = "{new_version}"',
                content
            )
            self.pyproject_path.write_text(new_content, encoding='utf-8')
            print(f"✅ 已更新 {self.pyproject_path}")
    
    def check_git_status(self):
        """检查Git状态"""
        print("🔍 检查Git状态...")
        
        # 检查是否有未提交的更改
        returncode, stdout, _ = self.run_command("git status --porcelain", check=False)
        if stdout.strip():
            print("⚠️  检测到未提交的更改:")
            print(stdout)
            response = input("是否继续发布? (y/N): ")
            if response.lower() != 'y':
                print("❌ 发布已取消")
                sys.exit(1)
        
        # 检查当前分支
        _, stdout, _ = self.run_command("git branch --show-current")
        current_branch = stdout.strip()
        print(f"📍 当前分支: {current_branch}")
        
        return current_branch
    
    def run_tests(self):
        """运行测试"""
        print("🧪 运行测试...")
        try:
            returncode, stdout, stderr = self.run_command("python -m unittest discover tests/", check=False)
            if returncode == 0:
                print("✅ 测试通过")
            else:
                print("❌ 测试失败")
                print("\n测试输出:")
                if stdout:
                    # 显示最后20行输出
                    lines = stdout.strip().split('\n')
                    for line in lines[-20:]:
                        print(line)
                else:
                    print("无标准输出")
                
                if stderr:
                    print("\n错误信息:")
                    error_lines = stderr.strip().split('\n')
                    for line in error_lines[-10:]:
                        print(line)
                
                print("")
                response = input("测试失败，是否继续发布? (y/N): ")
                if response.lower() != 'y':
                    sys.exit(1)
        except Exception as e:
            print(f"❌ 运行测试时出错: {e}")
            response = input("测试运行出错，是否继续发布? (y/N): ")
            if response.lower() != 'y':
                sys.exit(1)
    
    def clean_build(self):
        """清理构建文件"""
        print("🧹 清理构建文件...")
        
        # 清理目录
        clean_dirs = ["build", "dist", "*.egg-info"]
        for pattern in clean_dirs:
            self.run_command(f"rm -rf {pattern}", check=False)
        
        print("✅ 构建文件已清理")
    
    def build_package(self):
        """构建包"""
        print("📦 构建包...")
        
        # 使用 poetry build
        self.run_command("poetry build")
        
        # 检查构建结果
        dist_dir = self.project_root / "dist"
        if not dist_dir.exists() or not list(dist_dir.glob("*.whl")):
            print("❌ 构建失败，未找到构建文件")
            sys.exit(1)
            
        print("✅ 包构建完成")
    
    def publish_package(self, test_pypi: bool = False):
        """发布包"""
        repository = "testpypi" if test_pypi else "pypi"
        print(f"🚀 发布包到 {'Test PyPI' if test_pypi else 'PyPI'}...")
        
        try:
            if test_pypi:
                self.run_command("poetry publish --repository testpypi")
            else:
                self.run_command("poetry publish")
            print("✅ 包发布成功")
            return True
        except subprocess.CalledProcessError:
            print("❌ 包发布失败")
            return False
    
    def create_and_push_tag(self, version: str, message: str = None):
        """创建并推送标签"""
        tag_name = f"v{version}"
        
        print(f"🏷️  创建标签: {tag_name}")
        
        # 检查标签是否已存在
        _, stdout, _ = self.run_command(f"git tag -l {tag_name}", check=False)
        if stdout.strip():  # 如果有输出，说明标签存在
            print(f"⚠️  标签 {tag_name} 已存在")
            response = input("是否删除现有标签并重新创建? (y/N): ")
            if response.lower() == 'y':
                self.run_command(f"git tag -d {tag_name}")
                self.run_command(f"git push origin :refs/tags/{tag_name}", check=False)
            else:
                print("❌ 标签创建已取消")
                return False
        
        # 创建标签
        if message:
            self.run_command(f'git tag -a {tag_name} -m "{message}"')
        else:
            self.run_command(f'git tag -a {tag_name} -m "发布版本 {tag_name}"')
        
        # 推送标签
        self.run_command(f"git push origin {tag_name}")
        
        print(f"✅ 标签 {tag_name} 创建并推送成功")
        return True
    
    def commit_version_changes(self, version: str):
        """提交版本更改"""
        print("📝 提交版本更改...")
        
        # 添加更改的文件
        files_to_add = []
        if self.version_file.exists():
            files_to_add.append(str(self.version_file.relative_to(self.project_root)))
        if self.pyproject_path.exists():
            files_to_add.append(str(self.pyproject_path.relative_to(self.project_root)))
        
        for file_path in files_to_add:
            self.run_command(f"git add {file_path}")
        
        # 提交更改
        commit_message = f"chore: bump version to {version}"
        self.run_command(f'git commit -m "{commit_message}"')
        
        # 推送更改
        self.run_command("git push")
        
        print("✅ 版本更改已提交并推送")
    
    def release(self, new_version: str = None, test_pypi: bool = False, 
                skip_tests: bool = False, tag_message: str = None):
        """执行完整的发布流程"""
        print("🚀 开始自动化发布流程...")
        
        # 1. 检查Git状态
        current_branch = self.check_git_status()
        
        # 2. 获取当前版本
        current_version = self.get_current_version()
        print(f"📋 当前版本: {current_version}")
        
        # 3. 确定新版本号
        if not new_version:
            print("请输入新版本号 (当前版本: {})".format(current_version))
            new_version = input("新版本号: ").strip()
            if not new_version:
                print("❌ 版本号不能为空")
                sys.exit(1)
        
        print(f"🎯 目标版本: {new_version}")
        
        # 4. 运行测试
        if not skip_tests:
            self.run_tests()
        
        # 5. 更新版本号
        self.update_version(new_version)
        
        # 6. 提交版本更改
        self.commit_version_changes(new_version)
        
        # 7. 清理构建文件
        self.clean_build()
        
        # 8. 构建包
        self.build_package()
        
        # 9. 发布包
        if self.publish_package(test_pypi):
            # 10. 创建并推送标签
            self.create_and_push_tag(new_version, tag_message)
            
            print("🎉 发布流程完成!")
            print(f"✅ 版本 {new_version} 已成功发布")
            
            if test_pypi:
                print("📦 测试安装命令:")
                print(f"pip install -i https://test.pypi.org/simple/ data-checker=={new_version}")
            else:
                print("📦 安装命令:")
                print(f"pip install data-checker=={new_version}")
        else:
            print("❌ 发布失败")
            sys.exit(1)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="自动化发布脚本")
    parser.add_argument("--version", "-v", help="新版本号")
    parser.add_argument("--test", action="store_true", help="发布到 Test PyPI")
    parser.add_argument("--skip-tests", action="store_true", help="跳过测试")
    parser.add_argument("--tag-message", "-m", help="标签消息")
    parser.add_argument("--project-root", help="项目根目录路径")
    
    args = parser.parse_args()
    
    try:
        release_manager = ReleaseManager(args.project_root)
        release_manager.release(
            new_version=args.version,
            test_pypi=args.test,
            skip_tests=args.skip_tests,
            tag_message=args.tag_message
        )
    except KeyboardInterrupt:
        print("\n❌ 发布已被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 发布过程中出现错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 