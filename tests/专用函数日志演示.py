#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专用函数日志演示脚本
展示check_list和check_nested函数的详细日志输出
"""

import sys
import os

# 添加当前目录到系统路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from general_validator.logger import setup_logger
from general_validator.checker import check, check_list, check_nested, check_when

def demo_check_list():
    """演示check_list函数的日志输出"""
    print("\n=== check_list 函数日志演示 ===")
    
    # 测试数据
    product_list = [
        {"id": 1, "name": "商品1", "price": 10.5, "status": "active"},
        {"id": 2, "name": "商品2", "price": 20.0, "status": "active"},
        {"id": 0, "name": "", "price": -5.0, "status": "inactive"}  # 包含会失败的数据
    ]
    
    print("调用: check_list(product_list, 'id', 'name', price='> 0', status=\"== 'active'\")")
    result = check_list(product_list, 
                       "id", "name",                    # 默认非空校验
                       price="> 0", status="== 'active'")  # 带校验器
    
    print(f"结果: {result}")

def demo_check_nested():
    """演示check_nested函数的日志输出"""
    print("\n=== check_nested 函数日志演示 ===")
    
    # 测试数据
    response = {
        "data": {
            "productList": [
                {
                    "id": 1,
                    "name": "商品1",
                    "purchasePlan": [
                        {"id": 101, "name": "计划1", "amount": 100},
                        {"id": 102, "name": "计划2", "amount": 200}
                    ]
                },
                {
                    "id": 2,
                    "name": "商品2",
                    "purchasePlan": [
                        {"id": 201, "name": "", "amount": 50}  # 空名称和低金额
                    ]
                }
            ]
        }
    }
    
    print("调用: check_nested(response, 'data.productList', 'purchasePlan', 'id > 0', 'name', 'amount >= 100')")
    result = check_nested(response, "data.productList", "purchasePlan",
                          "id > 0", "name", "amount >= 100")
    
    print(f"结果: {result}")

def test_log_levels():
    """测试不同日志级别的输出效果"""
    
    test_data = {
        "user": {"name": "张三", "age": 25},
        "products": [
            {"id": 1, "name": "商品A", "price": 99.9, "status": "active"},
            {"id": 2, "name": "商品B", "price": 0, "status": "inactive"}
        ]
    }
    
    print("🔍 专用函数日志演示")
    print("=" * 50)
    
    # 测试不同日志级别
    log_levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
    
    for level in log_levels:
        print(f"\n📊 日志级别: {level}")
        print("-" * 30)
        
        # 设置日志级别
        setup_logger(level)
        
        # 1. 基础校验
        print("1. 基础校验:")
        result = check(test_data, "user.name", "user.age > 0")
        print(f"   结果: {result}")
        
        # 2. 条件校验
        print("2. 条件校验:")
        result = check_when(test_data, "user.age >= 18", "user.name")
        print(f"   结果: {result}")
        
        # 3. 条件校验异常处理
        print("3. 条件校验异常处理:")
        try:
            result = check_when(test_data, "user.nonexistent == 'value'", "user.name")
            print(f"   结果: {result} (未抛出异常)")
        except Exception as e:
            print(f"   ✓ 正确抛出异常: {type(e).__name__}")
        
        # 4. 校验失败情况
        print("4. 校验失败情况:")
        result = check(test_data, "products.*.price > 0")  # 有商品价格为0，会失败
        print(f"   结果: {result}")
        
        print()

def test_conditional_validation_exceptions():
    """专门测试条件校验的异常处理"""
    
    print("\n🚨 条件校验异常处理专项测试")
    print("=" * 50)
    
    # 设置INFO级别以减少输出
    setup_logger("INFO")
    
    test_data = {"user": {"name": "张三", "age": 25}}
    
    print("\n1. 条件字段不存在（应该抛出异常）:")
    try:
        result = check_when(test_data, "user.nonexistent == 'value'", "user.name")
        print(f"   ❌ 未抛出异常，结果: {result}")
    except Exception as e:
        print(f"   ✓ 正确抛出异常: {type(e).__name__}")
        print(f"   异常信息: 数据结构异常")
    
    print("\n2. then字段不存在（应该抛出异常）:")
    try:
        result = check_when(test_data, "user.name == '张三'", "user.nonexistent")
        print(f"   ❌ 未抛出异常，结果: {result}")
    except Exception as e:
        print(f"   ✓ 正确抛出异常: {type(e).__name__}")
        print(f"   异常信息: 数据结构异常")
    
    print("\n3. 条件不满足（应该跳过校验，返回True）:")
    try:
        result = check_when(test_data, "user.age < 18", "user.nonexistent")  # 条件不满足
        print(f"   ✓ 条件不满足，跳过校验，结果: {result}")
    except Exception as e:
        print(f"   ❌ 不应该抛出异常: {e}")
    
    print("\n4. 正常条件校验:")
    try:
        result = check_when(test_data, "user.age >= 18", "user.name")
        print(f"   ✓ 正常校验通过，结果: {result}")
    except Exception as e:
        print(f"   ❌ 不应该抛出异常: {e}")

def main():
    """主函数"""
    print("📋 专用函数日志演示")
    print("=" * 60)
    
    # 设置DEBUG级别以查看详细日志
    setup_logger("DEBUG")
    
    demo_check_list()
    demo_check_nested()
    
    # 测试日志级别
    test_log_levels()
    
    # 专项测试条件校验异常
    test_conditional_validation_exceptions()
    
    print("\n" + "=" * 60)
    print("💡 通过DEBUG级别可以看到:")
    print("- 函数参数概览")
    print("- 校验规则的构建过程")
    print("- 每个字段的详细校验信息")
    print("- 路径解析和值匹配过程")

if __name__ == "__main__":
    # 测试日志级别
    test_log_levels()
    
    # 专项测试条件校验异常
    test_conditional_validation_exceptions()
    
    print("\n" + "=" * 50)
    print("✅ 专用函数日志演示完成")
    print("\n💡 使用说明:")
    print("- 可通过 --log-level 参数控制日志输出级别")
    print("- DEBUG: 显示详细的校验过程")
    print("- INFO: 显示校验任务和结果概览")
    print("- WARNING: 只显示校验失败信息")
    print("- ERROR: 只显示数据结构异常")
    print("\n🎯 条件校验异常处理:")
    print("- 条件字段不存在: 抛出数据结构异常")
    print("- then字段不存在: 抛出数据结构异常")
    print("- 条件不满足: 跳过校验，返回True")
    print("- 校验失败: 返回False") 