#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试智能数值比较功能

gt、ge、lt、le 四个比较校验器支持智能类型转换，而 eq 和 ne 校验器不支撑

数值比较操作符（>, >=, <, <=）和等值比较操作符（==, !=）的使用场景本质上不同：

  1. 数值比较：主要用于范围检查、阈值判断等，用户更关心数值大小关系（支持智能类型转换）
  check(data, "age > 18")      # 年龄大于18
  check(data, "price <= 100")  # 价格不超过100
  check(data, "score >= 60")   # 分数及格

  2. 等值比较：用于精确匹配，类型本身可能就是判断条件的一部分（不支持智能类型转换）
  check(data, "status == 'active'")    # 状态必须是字符串 'active'
  check(data, "id == 12345")           # ID可能需要严格类型匹配
  check(data, "version != '1.0'")      # 版本号可能需要字符串匹配

  3. 注意：等值比较要执行严格匹配，不支持智能类型转换
  check(data, "count == 10")    # count="10" 时匹配失败，因为count是字符串，而10是整数
  check(data, "price != 0")     # price="0" 时匹配成功，因为price是字符串，而0是整数
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from general_validator.checker import check

def test_string_numeric_comparison():
    """测试字符串数字比较功能"""
    print("=== 测试智能数值比较功能 ===")
    
    # 测试数据 - 包含字符串格式的数字
    test_data = [
        {"duration": "25", "price": "99.5", "count": "10"},
        {"duration": "35", "price": "150.0", "count": "5"},
        {"duration": "15", "price": "50", "count": "20"}
    ]
    
    print(f"测试数据: {test_data}")
    print()
    
    # 测试1: 原来会报错的情况
    print("测试1: 字符串数字与整数比较")
    try:
        result1 = check(test_data, "*.duration <= 30")
        print(f"*.duration <= 30: {'✓ 通过' if result1 else '✗ 失败'}")
    except Exception as e:
        print(f"*.duration <= 30: ❌ 异常 - {e}")
    
    # 测试2: 各种数值比较
    print("\n测试2: 各种数值比较操作")
    test_cases = [
        ("*.duration > 10", "所有duration大于10"),
        ("*.price >= 50", "所有price大于等于50"),
        ("*.count < 25", "所有count小于25"),
        ("*.duration <= 40", "所有duration小于等于40"),
    ]
    
    for rule, desc in test_cases:
        try:
            result = check(test_data, rule)
            print(f"{rule}: {'✓ 通过' if result else '✗ 失败'} ({desc})")
        except Exception as e:
            print(f"{rule}: ❌ 异常 - {e}")
    
    # 测试3: 混合类型数据
    print("\n测试3: 混合类型数据")
    mixed_data = {
        "int_str": "123",      # 字符串整数
        "float_str": "45.67",  # 字符串浮点数
        "int_val": 89,         # 整数
        "float_val": 12.34,    # 浮点数
        "text": "hello"        # 纯文本
    }
    
    mixed_test_cases = [
        ("int_str > 100", "字符串整数比较"),
        ("float_str <= 50", "字符串浮点数比较"),
        ("int_val >= 80", "整数比较"),
        ("float_val < 15", "浮点数比较"),
    ]
    
    for rule, desc in mixed_test_cases:
        try:
            result = check(mixed_data, rule)
            print(f"{rule}: {'✓ 通过' if result else '✗ 失败'} ({desc})")
        except Exception as e:
            print(f"{rule}: ❌ 异常 - {e}")
    
    # 测试4: 无法转换的情况（应该回退到原始比较）
    print("\n测试4: 无法转换的情况")
    try:
        # 这应该失败但不会抛异常，因为会回退到原始字符串比较
        result = check(mixed_data, "text > 'a'")
        print(f"text > 'a': {'✓ 通过' if result else '✗ 失败'} (字符串比较)")
    except Exception as e:
        print(f"text > 'a': ❌ 异常 - {e}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_string_numeric_comparison()
