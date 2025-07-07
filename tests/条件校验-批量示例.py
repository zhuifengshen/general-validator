#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试批量条件校验功能 - check_when 增强版
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from general_validator.checker import check_when, checker

# 测试数据
test_data = {
    "user": {
        "level": "vip",
        "status": "active",
        "last_login": "2024-01-15",
        "email": "user@example.com",
        "permissions": {
            "download": True,
            "upload": True
        },
        "quota": 5000
    },
    "products": [
        {
            "id": 1,
            "name": "Product A",
            "price": 100,
            "status": "active",
            "category": "electronics",
            "description": "高质量产品"
        },
        {
            "id": 2,
            "name": "Product B", 
            "price": 200,
            "status": "active",
            "category": "books",
            "description": "畅销书籍"
        }
    ],
    "order": {
        "type": "premium",
        "features": ["feature1", "feature2", "feature3"],
        "price": 150,
        "discount": 0.1
    }
}

def test_single_when():
    """测试单个条件校验（向后兼容）"""
    print("=== 测试单个条件校验 ===")
    
    # 单个then校验
    result = check_when(test_data, "user.level == 'vip'", "user.quota > 1000")
    print(f"单个then校验结果: {result}")
    
    # 条件不满足的情况
    result = check_when(test_data, "user.level == 'normal'", "user.quota > 1000")
    print(f"条件不满足时的结果: {result}")


def test_batch_when():
    """测试批量条件校验"""
    print("\n=== 测试批量条件校验 ===")
    
    # 多个then校验 - 当用户为VIP时，多个权限字段都必须校验
    result = check_when(test_data, "user.level == 'vip'", 
                       "user.permissions.download == true",
                       "user.permissions.upload == true", 
                       "user.quota > 1000",
                       "user.status == 'active'")
    print(f"批量校验结果: {result}")
    
    # 带通配符的批量校验 - 当所有产品状态为active时，多个字段都必须校验
    result = check_when(test_data, "products.*.status == 'active'", 
                       "products.*.price > 0", 
                       "products.*.name",
                       "products.*.id > 0")
    print(f"通配符批量校验结果: {result}")
    
    # 订单类型校验 - 当type为premium时，多个字段都必须校验
    result = check_when(test_data, "order.type == 'premium'", 
                       "order.features",
                       "order.price > 100",
                       "order.discount >= 0")
    print(f"订单批量校验结果: {result}")


def test_checker_batch_when():
    """测试链式调用的批量条件校验"""
    print("\n=== 测试链式调用的批量条件校验 ===")
    
    # 链式调用示例
    result = checker(test_data) \
        .when("user.level == 'vip'", 
              "user.permissions.download == true",
              "user.permissions.upload == true", 
              "user.quota > 1000") \
        .when("user.status == 'active'", 
              "user.last_login", 
              "user.email") \
        .when("products.*.status == 'active'", 
              "products.*.price > 0", 
              "products.*.name") \
        .validate()
    
    print(f"链式批量校验结果: {result}")


def test_failed_cases():
    """测试失败的情况"""
    print("\n=== 测试失败的情况 ===")
    
    # 修改测试数据，使某些校验失败
    failed_data = {
        "user": {
            "level": "vip",
            "status": "active",
            "permissions": {
                "download": True,
                "upload": False  # 这个会导致校验失败
            },
            "quota": 5000
        }
    }
    
    # 批量校验，其中一个失败
    result = check_when(failed_data, "user.level == 'vip'", 
                       "user.permissions.download == true",
                       "user.permissions.upload == true",  # 这个会失败
                       "user.quota > 1000")
    print(f"部分校验失败的结果: {result}")
    
    # 所有校验都通过的情况
    result = check_when(failed_data, "user.level == 'vip'", 
                       "user.permissions.download == true",
                       "user.quota > 1000")
    print(f"所有校验通过的结果: {result}")


if __name__ == "__main__":
    print("批量条件校验功能测试")
    print("=" * 50)
    
    test_single_when()
    test_batch_when()
    test_checker_batch_when()
    test_failed_cases()
    
    print("\n测试完成！") 