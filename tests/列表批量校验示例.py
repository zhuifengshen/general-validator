#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试 check_list 函数 - 与其他函数风格一致的列表数据批量校验
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from general_validator.checker import check_list, check, checker

# 测试数据
test_products = [
    {
        "id": 1,
        "name": "Product A",
        "price": 100.5,
        "status": "active",
        "category": "electronics",
        "description": "高质量的电子产品",
        "tags": ["electronic", "popular"],
        "is_active": True,
        "url": "https://example.com/product-a",
        "created_at": "2024-01-15"
    },
    {
        "id": 2,
        "name": "Product B",
        "price": 200.0,
        "status": "active",
        "category": "books",
        "description": "畅销书籍",
        "tags": ["book", "bestseller"],
        "is_active": True,
        "url": "https://example.com/product-b",
        "created_at": "2024-01-16"
    },
    {
        "id": 3,
        "name": "Product C",
        "price": 50.0,
        "status": "inactive",
        "category": "clothing",
        "description": "时尚服装",
        "tags": ["clothing", "fashion"],
        "is_active": False,
        "url": "https://example.com/product-c",
        "created_at": "2024-01-17"
    }
]

def test_basic_usage():
    """测试基本使用方式"""
    print("=== 测试基本使用方式 ===")
    
    # 默认非空校验
    result = check_list(test_products, "id", "name", "price")
    print(f"默认非空校验结果: {result}")
    
    # 带校验器的校验
    result = check_list(test_products, "id > 0", "name", "price >= 0", "status")
    print(f"带校验器校验结果: {result}")


def test_various_validators():
    """测试各种校验器"""
    print("\n=== 测试各种校验器 ===")
    
    # 数值比较校验
    result = check_list(test_products, "id > 0", "price >= 50", "id != 999")
    print(f"数值比较校验结果: {result}")
    
    # 字符串校验
    result = check_list(test_products, "name ^= 'Product'", "category != 'test'")
    print(f"字符串校验结果: {result}")
    
    # 类型校验
    result = check_list(test_products, "id @= int", "name @= str", "price @= float", "is_active @= bool")
    print(f"类型校验结果: {result}")
    
    # 长度校验
    result = check_list(test_products, "name #>= 3", "description #<= 100", "tags #> 0")
    print(f"长度校验结果: {result}")


def test_complex_validations():
    """测试复杂组合校验"""
    print("\n=== 测试复杂组合校验 ===")
    
    # 复杂组合校验
    result = check_list(test_products, 
                        "id > 0", 
                        "name", 
                        "price >= 0", 
                        "status",
                        "category != 'test'",
                        "description #>= 5",
                        "tags #> 0",
                        "created_at")
    print(f"复杂组合校验结果: {result}")


def test_style_comparison():
    """测试与其他函数风格的对比"""
    print("\n=== 测试与其他函数风格的对比 ===")
    
    # check_list 风格 1
    result_array = check_list(test_products, "name", "id", price="> 0", status="!= 'disabled'")
    print(f"风格1结果: {result_array}")
    
    # check_list 风格 2
    result_list = check_list(test_products, "name", "id", "price > 0", "status != 'disabled'")
    print(f"风格2结果: {result_list}")
    
    # 验证结果一致性
    print(f"两种风格结果一致: {result_list == result_array}")


def test_consistency_with_check():
    """测试与check函数的一致性"""
    print("\n=== 测试与check函数的一致性 ===")
    
    # 使用 check 函数的通配符方式
    result_check = check(test_products, "*.id > 0", "*.name", "*.price >= 0")
    print(f"check 函数结果: {result_check}")
    
    # 使用 check_list 函数的简化方式
    result_array = check_list(test_products, "id > 0", "name", "price >= 0")
    print(f"check_list 函数结果: {result_array}")
    
    # 验证结果一致性
    print(f"两种方式结果一致: {result_check == result_array}")


def test_error_cases():
    """测试错误情况"""
    print("\n=== 测试错误情况 ===")
    
    # 某些校验失败的情况
    result = check_list(test_products, "id > 0", "name", "price > 1000")  # price > 1000 会失败
    print(f"部分校验失败的结果: {result}")
    
    # 校验完全通过的情况
    result = check_list(test_products, "id > 0", "name", "price >= 0")
    print(f"全部校验通过的结果: {result}")


def test_with_checker():
    """测试与checker的配合使用"""
    print("\n=== 测试与checker的配合使用 ===")
    
    # 使用checker处理数组数据
    result = checker(test_products) \
        .field("*.id", "> 0") \
        .field("*.name") \
        .field("*.price", ">= 0") \
        .field("*.status") \
        .validate()
    
    print(f"checker处理数组数据结果: {result}")
    
    # 对比 check_list 的结果
    result_array = check_list(test_products, "id > 0", "name", "price >= 0", "status")
    print(f"check_list 结果: {result_array}")
    
    # 验证结果一致性
    print(f"两种方式结果一致: {result == result_array}")


def demo_usage_examples():
    """演示使用示例"""
    print("\n=== 演示使用示例 ===")
    print("以下是 check_list 函数的各种使用示例：")
    
    examples = [
        ("默认非空校验", 'check_list(productList, "id", "name", "price")'),
        ("数值比较校验", 'check_list(productList, "id > 0", "price >= 0", "stock > 10")'),
        ("字符串校验", 'check_list(productList, "name", "status == \'active\'", "category != \'test\'")'),
        ("类型校验", 'check_list(productList, "id @= int", "name @= str", "price @= float")'),
        ("长度校验", 'check_list(productList, "name #>= 3", "description #<= 100", "tags #> 0")'),
        ("字符串匹配", 'check_list(productList, "name ^= \'Product\'", "url ~= \'^https://\'")'),
        ("复杂组合", 'check_list(productList, "id > 0", "name", "price >= 0", "status", "tags #> 0")'),
    ]
    
    for desc, example in examples:
        print(f"{desc}:")
        print(f"  {example}")
        print()


if __name__ == "__main__":
    print("check_list 函数功能测试")
    print("=" * 60)
    
    test_basic_usage()
    test_various_validators()
    test_complex_validations()
    test_wildcard_handling()
    test_style_comparison()
    test_consistency_with_check()
    test_error_cases()
    test_with_checker()
    demo_usage_examples()
    
    print("=" * 60)
    print("测试完成！")
    print("\ncheck_list 函数特点总结：")
    print("1. 与 check() 函数风格完全一致")
    print("2. 自动处理数组元素的通配符前缀")
    print("3. 支持所有校验器语法")
    print("4. 调用方式更加直观简洁")
    print("5. 与现有函数生态完美融合") 