#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
日志级别控制演示脚本
展示不同日志级别下的输出效果
"""

import sys
import os

# 添加当前目录到系统路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from general_validator.logger import setup_logger
from general_validator.checker import check

def demo_validation():
    """演示校验功能"""
    # 测试数据
    response = {
        "status_code": 200,
        "message": "success",
        "data": {
            "product": {
                "id": 0,  # 这个会导致校验失败
                "name": "商品A",
                "price": 99.99
            },
            "productList": [
                {"id": 1, "name": "商品1", "price": 10.5},
                {"id": 2, "name": "", "price": 20.0}  # 空名称会导致校验失败
            ]
        }
    }
    
    print("执行数据校验（包含会失败的校验）...")
    result = check(response,
                   "status_code == 200",        # 通过
                   "data.product.id > 0",       # 失败：id=0
                   "data.product.name",         # 通过
                   "data.productList.*.id > 0", # 通过
                   "data.productList.*.name")   # 失败：第二个商品名称为空
    
    print(f"校验结果: {result}")

def main():
    """主函数"""
    print("📋 日志级别控制演示")
    print("=" * 60)
    
    levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
    
    for level in levels:
        print(f"\n🔍 {level} 级别输出:")
        print("-" * 40)
        # 使用项目的日志设置
        setup_logger(level)
        demo_validation()
    
    print("\n" + "=" * 60)
    print("💡 在实际使用中，可以通过以下命令控制日志级别:")
    print("apimeter run testcase.yml --log-level DEBUG")
    print("apimeter run testcase.yml --log-level INFO")
    print("apimeter run testcase.yml --log-level WARNING")
    print("apimeter run testcase.yml --log-level ERROR")
    print("\n不同日志级别的效果：")
    print("- DEBUG: 显示详细的校验过程信息")
    print("- INFO: 显示校验开始和完成的汇总信息（默认级别）")
    print("- WARNING: 只显示校验失败的警告信息")
    print("- ERROR: 只显示数据结构异常等严重错误")

if __name__ == "__main__":
    main() 