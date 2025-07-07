#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
条件校验示例 - 展示完善后的条件校验功能

新的条件校验特性：
1. 支持所有校验器语法（不再局限于等值校验）
2. 支持通配符路径
3. 复用现有校验逻辑，保持极简风格
4. 提供多种调用方式
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from general_validator.logger import setup_logger
from general_validator.checker import check, check_when, checker

def test_basic_conditional_validation():
    """基础条件校验测试"""
    print("\n=== 基础条件校验测试 ===")
    
    # 测试数据
    user_data = {
        "user": {
            "type": "premium",
            "status": "active",
            "balance": 100,
            "features": ["feature1", "feature2"],
            "email": "user@example.com"
        }
    }
    
    # 1. 使用check函数 - 字典格式
    print("\n1. 字典格式条件校验1")
    conditional_rule = {
        'field': 'conditional',
        'validator': 'conditional_check',
        'expect': {
            'condition': "user.type == 'premium'",
            'then': "user.features"  # 当type为premium时，features不能为空
        }
    }
    result = check(user_data, conditional_rule)
    print(f"结果: {result}")

    # print("\n1. 字典格式条件校验2")
    # conditional_rule = {
    #     'field': 'conditional',
    #     'validator': 'conditional_validator',
    #     'expect': {
    #         'condition': "user.type == 'premium'",
    #         'then': "user.features"  # 当type为premium时，features不能为空
    #     }
    # }
    # result = check(user_data, conditional_rule)
    # print(f"结果: {result}")

    # print("\n1. 字典格式条件校验3")
    # conditional_rule = {
    #     'field': 'conditional',
    #     'validator': 'conditional_validate',
    #     'expect': {
    #         'condition': "user.type == 'premium'",
    #         'then': "user.features"  # 当type为premium时，features不能为空
    #     }
    # }
    # result = check(user_data, conditional_rule)
    # print(f"结果: {result}")

    # 2. 使用check_when函数
    print("\n2. check_when函数")
    result = check_when(user_data, "user.status == 'active'", "user.balance > 0")
    print(f"结果: {result}")
    
    # 3. 使用链式调用
    print("\n3. 链式调用")
    result = checker(user_data)\
        .when("user.type == 'premium'", "user.email")\
        .when("user.status == 'active'", "user.balance >= 50")\
        .validate()
    print(f"结果: {result}")


def test_advanced_conditional_validation():
    """高级条件校验测试"""
    print("\n=== 高级条件校验测试 ===")
    
    # 测试数据 - 商品列表
    products_data = {
        "products": [
            {
                "id": 1,
                "name": "商品A",
                "status": "active",
                "price": 99.9,
                "category": "electronics",
                "stock": 10
            },
            {
                "id": 2,
                "name": "商品B",
                "status": "inactive",
                "price": 0,
                "category": "books",
                "stock": 0
            },
            {
                "id": 3,
                "name": "商品C",
                "status": "active",
                "price": 199.5,
                "category": "electronics",
                "stock": 5
            }
        ]
    }
    
    # 1. 通配符条件校验 - 当商品状态为active时，价格必须大于0
    print("\n1. 通配符条件校验")
    result = check_when(
        products_data, 
        "products.*.status == 'active'", 
        "products.*.price > 0"
    )
    print(f"结果: {result}")
    
    # 2. 多种校验器组合
    print("\n2. 多种校验器组合")
    result = checker(products_data)\
        .when("products.*.category == 'electronics'", "products.*.price >= 50")\
        .when("products.*.status == 'active'", "products.*.stock > 0")\
        .validate()
    print(f"结果: {result}")
    
    # 3. 字符串匹配条件
    print("\n3. 字符串匹配条件")
    result = check_when(
        products_data,
        "products.*.name ^= '商品'",  # 名称以"商品"开头
        "products.*.id > 0"          # ID必须大于0
    )
    print(f"结果: {result}")


def test_complex_conditional_scenarios():
    """复杂条件校验场景"""
    print("\n=== 复杂条件校验场景 ===")
    
    # 订单数据
    order_data = {
        "order": {
            "id": "ORD001",
            "status": "confirmed",
            "total": 299.8,
            "payment_method": "credit_card",
            "items": [
                {
                    "product_id": 1,
                    "quantity": 2,
                    "price": 99.9,
                    "discount_type": "percentage",
                    "discount_value": 10
                },
                {
                    "product_id": 2,
                    "quantity": 1,
                    "price": 199.9,
                    "discount_type": "fixed",
                    "discount_value": 20
                }
            ]
        }
    }
    
    # 1. 嵌套条件校验
    print("\n1. 嵌套条件校验")
    result = checker(order_data)\
        .when("order.status == 'confirmed'", "order.total > 0")\
        .when("order.payment_method == 'credit_card'", "order.id")\
        .when("order.items.*.discount_type == 'percentage'", "order.items.*.discount_value <= 100")\
        .when("order.items.*.discount_type == 'fixed'", "order.items.*.discount_value > 0")\
        .validate()
    print(f"结果: {result}")
    
    # 2. 类型校验条件
    print("\n2. 类型校验条件")
    result = check_when(
        order_data,
        "order.items.*.quantity @= 'int'",  # 数量必须是整数
        "order.items.*.quantity > 0"        # 且大于0
    )
    print(f"结果: {result}")


def test_conditional_validation_edge_cases():
    """条件校验边界情况测试"""
    print("\n=== 条件校验边界情况测试 ===")
    
    # 1. 条件不满足的情况
    print("\n1. 条件不满足（应该跳过校验）")
    test_data = {"status": "inactive", "value": None}
    result = check_when(test_data, "status == 'active'", "value")  # 条件不满足，跳过校验
    print(f"结果: {result} (条件不满足，跳过校验)")
    
    # 2. 条件满足但then校验失败
    print("\n2. 条件满足但then校验失败")
    test_data = {"status": "active", "value": None}
    result = check_when(test_data, "status == 'active'", "value")  # 条件满足，但value为空
    print(f"结果: {result} (条件满足但then校验失败)")
    
    # 3. 条件和then都通过
    print("\n3. 条件和then都通过")
    test_data = {"status": "active", "value": "valid"}
    result = check_when(test_data, "status == 'active'", "value")
    print(f"结果: {result} (条件和then都通过)")
    
    # 4. 复杂条件表达式
    print("\n4. 复杂条件表达式")
    test_data = {"config": {"env": "production", "debug": False}, "logging": {"level": "ERROR"}}
    result = check_when(
        test_data,
        "config.env == 'production'",
        "logging.level ~= '^(ERROR|WARN)$'"  # 生产环境日志级别必须是ERROR或WARN
    )
    print(f"结果: {result}")


def test_conditional_validation_errors():
    """条件校验异常情况测试"""
    print("\n=== 条件校验异常情况测试 ===")
    
    test_data = {"user": {"name": "张三"}}
    
    # 1. 条件字段不存在 - 应该抛出异常
    print("\n1. 条件字段不存在（应该抛出异常）")
    try:
        result = check_when(test_data, "user.nonexistent == 'value'", "user.name")
        print(f"结果: {result} (未抛出异常，这是错误的)")
    except Exception as e:
        print(f"✓ 正确抛出异常: {type(e).__name__}")
    
    # 2. then字段不存在 - 应该抛出异常
    print("\n2. then字段不存在（应该抛出异常）")
    try:
        result = check_when(test_data, "user.name == '张三'", "user.nonexistent")
        print(f"结果: {result} (未抛出异常，这是错误的)")
    except Exception as e:
        print(f"✓ 正确抛出异常: {type(e).__name__}")
    
    # 3. 测试条件不满足但字段存在的情况
    print("\n3. 条件不满足但字段存在（应该跳过校验）")
    try:
        result = check_when(test_data, "user.name == '李四'", "user.name")
        print(f"结果: {result} (条件不满足，跳过校验)")
    except Exception as e:
        print(f"异常: {e}")


if __name__ == "__main__":
    # 设置日志级别
    setup_logger("DEBUG")
    
    print("🔍 条件校验功能完善示例")
    print("=" * 50)
    
    # 运行测试
    test_basic_conditional_validation()
    test_advanced_conditional_validation()
    test_complex_conditional_scenarios()
    test_conditional_validation_edge_cases()
    test_conditional_validation_errors()
    
    print("\n" + "=" * 50)
    print("✅ 条件校验功能测试完成")
    print("\n主要改进:")
    print("1. ✅ 支持所有校验器语法（不再局限于等值校验）")
    print("2. ✅ 支持通配符路径")
    print("3. ✅ 复用现有校验逻辑，保持极简风格")
    print("4. ✅ 提供多种调用方式")
    print("5. ✅ 完整的异常处理和日志输出") 