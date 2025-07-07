#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
链式调用数据校验器功能测试
展示完善后的DataChecker类的各种校验能力
"""

import sys
import os

# 添加当前目录到系统路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from general_validator.logger import setup_logger
from general_validator.checker import checker

def test_basic_validations():
    """测试基础校验功能"""
    print("\n=== 基础校验功能测试 ===")
    
    data = {
        "user": {
            "id": 123,
            "name": "张三",
            "age": 25,
            "email": "zhangsan@example.com",
            "phone": "13812345678",
            "score": 85.5,
            "is_active": True,
            "profile": {
                "bio": "软件工程师"
            }
        },
        "products": [
            {"id": 1, "name": "产品A", "price": 100},
            {"id": 2, "name": "产品B", "price": 200}
        ]
    }
    
    # 基础校验
    result = checker(data)\
        .not_empty("user.id", "user.name", "user.email")\
        .equals("user.name", "张三")\
        .not_equals("user.age", 0)\
        .greater_than("products.*.price", 1)\
        .validate()
    
    print(f"基础校验结果: {result}")
    assert result == True


def test_numeric_validations():
    """测试数值校验功能"""
    print("\n=== 数值校验功能测试 ===")
    
    data = {
        "product": {
            "id": 123,
            "price": 99.99,
            "stock": 50,
            "discount": 0.1
        }
    }
    
    # 数值比较校验
    result = checker(data)\
        .greater_than("product.price", 50)\
        .greater_equal("product.stock", 50)\
        .less_than("product.discount", 1)\
        .less_equal("product.discount", 0.5)\
        .between("product.price", 50, 150)\
        .is_positive("product.id")\
        .is_non_negative("product.stock")\
        .validate()
    
    print(f"数值校验结果: {result}")
    assert result == True


def test_string_validations():
    """测试字符串校验功能"""
    print("\n=== 字符串校验功能测试 ===")
    
    data = {
        "user": {
            "name": "测试用户",
            "email": "test@example.com",
            "phone": "13812345678",
            "url": "https://www.example.com",
            "description": "这是一个测试用户"
        }
    }
    
    # 字符串校验
    result = checker(data)\
        .starts_with("user.name", "测试")\
        .ends_with("user.email", ".com")\
        .contains("user.description", "测试")\
        .is_email("user.email")\
        .is_phone("user.phone")\
        .is_url("user.url")\
        .validate()
    
    print(f"字符串校验结果: {result}")
    assert result == True


def test_type_validations():
    """测试类型校验功能"""
    print("\n=== 类型校验功能测试 ===")
    
    data = {
        "mixed": {
            "number": 123,
            "float_num": 45.67,
            "text": "hello",
            "flag": True,
            "items": [1, 2, 3],
            "info": {"key": "value"},
            "nothing": None
        }
    }
    
    # 类型校验
    result = checker(data)\
        .is_integer("mixed.number")\
        .is_float("mixed.float_num")\
        .is_string("mixed.text")\
        .is_boolean("mixed.flag")\
        .is_list("mixed.items")\
        .is_dict("mixed.info")\
        .is_none("mixed.nothing")\
        .is_number("mixed.number")\
        .is_number("mixed.float_num")\
        .validate()
    
    print(f"类型校验结果: {result}")
    assert result == True


def test_collection_validations():
    """测试集合校验功能"""
    print("\n=== 集合校验功能测试 ===")
    
    data = {
        "status": "active",
        "priority": "high",
        "category": "other"
    }
    
    # 集合校验
    result = checker(data)\
        .in_values("status", ["active", "inactive", "pending"])\
        .in_values("priority", ["low", "medium", "high"])\
        .not_in_values("category", ["forbidden", "blocked"])\
        .validate()
    
    print(f"集合校验结果: {result}")
    assert result == True


def test_length_validations():
    """测试长度校验功能"""
    print("\n=== 长度校验功能测试 ===")
    
    data = {
        "username": "testuser",
        "password": "password123",
        "tags": ["tag1", "tag2", "tag3"],
        "comment": "这是一个测试评论"
    }
    
    # 长度校验
    result = checker(data)\
        .length_greater_than("username", 5)\
        .length_less_than("password", 20)\
        .length_equals("tags", 3)\
        .length_between("comment", 5, 50)\
        .validate()
    
    print(f"长度校验结果: {result}")
    assert result == True


def test_batch_validations():
    """测试批量校验功能"""
    print("\n=== 批量校验功能测试 ===")
    
    data = {
        "product": {
            "id": 1,
            "price": 100,
            "stock": 50,
            "name": "产品A",
            "description": "这是产品A的描述",
            "category": "电子产品"
        }
    }
    
    # 批量校验
    result = checker(data)\
        .all_fields_not_empty("product.id", "product.name", "product.description")\
        .all_fields_positive("product.id", "product.price", "product.stock")\
        .all_fields_type("str", "product.name", "product.description", "product.category")\
        .validate()
    
    print(f"批量校验结果: {result}")
    assert result == True


def test_conditional_validations():
    """测试条件校验功能"""
    print("\n=== 条件校验功能测试 ===")
    
    data = {
        "order": {
            "type": "premium",
            "discount": 0.2,
            "min_amount": 1000
        }
    }
    
    # 条件校验：当订单类型为premium时，折扣必须大于0.1
    result = checker(data)\
        .when("order.type == 'premium'", "order.discount > 0.1")\
        .when("order.type == 'premium'", "order.min_amount >= 500")\
        .validate()
    
    print(f"条件校验结果: {result}")
    assert result == True


def test_failure_cases():
    """测试失败场景"""
    print("\n=== 失败场景测试 ===")
    
    data = {
        "user": {
            "age": -5,  # 负数
            "email": "invalid-email",  # 无效邮箱
            "phone": "123",  # 无效手机号
            "status": "unknown"  # 不在允许值中
        }
    }
    
    # 这些校验应该失败
    result = checker(data)\
        .is_positive("user.age")\
        .is_email("user.email")\
        .is_phone("user.phone")\
        .in_values("user.status", ["active", "inactive"])\
        .validate()
    
    print(f"失败场景校验结果: {result}")
    assert result == False


def main():
    """主测试函数"""
    print("🔗 链式调用数据校验器功能测试")
    print("=" * 60)
    
    # 设置DEBUG级别以查看详细日志
    setup_logger("DEBUG")  # 使用INFO级别，避免过多详细日志
    
    tests = [
        test_basic_validations,
        test_numeric_validations,
        test_string_validations,
        test_type_validations,
        test_collection_validations,
        test_length_validations,
        test_batch_validations,
        test_conditional_validations,
        test_failure_cases
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
            print("✓ 测试通过")
        except Exception as e:
            print(f"✗ 测试失败: {e}")
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试都通过了！链式调用数据校验器功能正常。")
    else:
        print("❌ 部分测试失败，请检查实现。")
    
    print("\n💡 链式调用数据校验器支持的功能：")
    print("- 基础校验：非空、等值比较")
    print("- 数值校验：大小比较、范围校验、正负数校验")
    print("- 字符串校验：前缀、后缀、包含、正则、格式校验")
    print("- 类型校验：各种数据类型检查")
    print("- 集合校验：值是否在指定集合中")
    print("- 长度校验：字符串、列表长度检查")
    print("- 批量校验：同时校验多个字段")
    print("- 条件校验：基于条件的动态校验")

if __name__ == "__main__":
    main() 