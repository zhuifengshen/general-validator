#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
新数据校验函数测试脚本
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from general_validator.checker import check, check_not_empty, check_list, check_nested, checker

def test_basic_validation():
    """测试基础校验功能"""
    print("=== 测试基础校验功能 ===")
    
    # 测试数据
    response = {
        "status_code": 200,
        "message": "success",
        "data": {
            "product": {
                "id": 7,
                "name": "商品A",
                "price": 99.99,
                "description": "这是一个测试商品"
            },
            "productList": [
                {
                    "id": 1,
                    "name": "商品1",
                    "price": 10.5,
                    "status": "active",
                    "purchasePlan": [
                        {"id": 101, "name": "计划1", "amount": 100},
                        {"id": 102, "name": "计划2", "amount": 200}
                    ]
                },
                {
                    "id": 2,
                    "name": "商品2", 
                    "price": 20.0,
                    "status": "active",
                    "purchasePlan": [
                        {"id": 201, "name": "计划3", "amount": 300}
                    ]
                }
            ]
        }
    }
    
    try:
        # 1. 最简单的非空校验
        print("1. 测试非空校验...")
        check(response, "data.product.id", "data.product.name")
        print("✓ 非空校验通过")
        
        # 2. 带校验器的简洁语法  
        print("2. 测试带校验器的语法...")
        check(response, 
              "status_code == 200",
              "data.product.id > 0", 
              "data.product.price >= 10")
        print("✓ 带校验器的语法通过")
        
        # 3. 混合校验
        print("3. 测试混合校验...")
        check(response, 
              "data.product.id",           # 默认非空
              "data.product.price > 0",    # 大于0
              "status_code == 200",        # 等于200
              "message ^= 'suc'")          # 以'suc'开头
        print("✓ 混合校验通过")
        
        # 4. 通配符批量校验
        print("4. 测试通配符批量校验...")
        check(response, 
              "data.productList.*.id",           # 所有商品ID非空
              "data.productList.*.name",         # 所有商品名称非空
              "data.productList.*.id > 0",       # 所有商品ID大于0
              "data.productList.*.price >= 0")   # 所有商品价格大于等于0
        print("✓ 通配符批量校验通过")
        
        # 5. 嵌套列表校验
        print("5. 测试嵌套列表校验...")
        check(response, 
              "data.productList.*.purchasePlan.*.id > 0",
              "data.productList.*.purchasePlan.*.name",
              "data.productList.*.purchasePlan.*.amount >= 100")
        print("✓ 嵌套列表校验通过")
        
    except Exception as e:
        print(f"✗ 基础校验测试失败: {e}")
        return False
    
    return True


def test_specialized_functions():
    """测试专用函数"""
    print("\n=== 测试专用函数 ===")
    
    response = {
        "data": {
            "product": {"id": 7, "name": "商品A"},
            "productList": [
                {"id": 1, "name": "商品1", "price": 10.5},
                {"id": 2, "name": "商品2", "price": 20.0}
            ]
        }
    }
    
    try:
        # 1. 专门的非空校验
        print("1. 测试专门非空校验...")
        check_not_empty(response, "data.product.id", "data.product.name")
        print("✓ 专门非空校验通过")
        
        # 2. 列表批量校验
        print("2. 测试列表批量校验...")
        check_list(response["data"]["productList"], 
                   "id", "name",                    # 默认非空
                   price="> 0", id="> 0")           # 带校验器
        print("✓ 列表批量校验通过")
        
        # 3. 链式调用
        print("3. 测试链式调用...")
        checker(response)\
            .not_empty("data.product.id", "data.product.name")\
            .equals("data.product.id", 7)\
            .greater_than("data.product.id", 0)\
            .validate()
        print("✓ 链式调用通过")
        
    except Exception as e:
        print(f"✗ 专用函数测试失败: {e}")
        return False
    
    return True


def test_error_handling():
    """测试错误处理"""
    print("\n=== 测试错误处理 ===")
    
    response = {
        "status_code": 200,
        "data": {"product": {"id": 0, "name": "商品A"}}
    }
    
    # 1. 测试校验失败返回False
    print("1. 测试校验失败返回False...")
    result = check(response, "data.product.id > 0")  # 这应该返回False
    if result == False:
        print("✓ 校验失败正确返回False")
    else:
        print("✗ 校验失败应该返回False")
        return False
    
    # 2. 测试混合校验结果
    print("2. 测试混合校验结果...")
    result = check(response, 
                   "status_code == 200",        # 这个会通过
                   "data.product.id > 0",       # 这个会失败
                   )
    
    if result == False:
        print("✓ 混合校验结果正确返回False（存在失败项）")
    else:
        print("✗ 混合校验应该返回False")
        return False
    
    # 3. 测试数据结构异常
    print("3. 测试数据结构异常...")
    try:
        check(response, "data.invalid_field")  # 这应该抛出异常
        print("✗ 数据结构异常应该抛出异常")
        return False
    except Exception:
        print("✓ 数据结构异常正确抛出异常")
    
    return True


def test_data_types():
    """测试各种数据类型"""
    print("\n=== 测试各种数据类型 ===")
    
    response = {
        "string_field": "test_string",
        "number_field": 42,
        "float_field": 3.14,
        "boolean_field": True,
        "null_field": None,
        "array_field": [1, 2, 3],
        "object_field": {"key": "value"}
    }
    
    try:
        # 测试各种数据类型的校验
        check(response,
              "string_field",                    # 字符串非空
              "number_field > 0",                # 数字大于0
              "float_field >= 3.0",              # 浮点数大于等于3.0
              "boolean_field == true",           # 布尔值为true
              "null_field == null",              # null值校验
              "string_field ^= 'test'",          # 字符串开头
              "string_field $= 'string'",        # 字符串结尾
              "string_field *= 'est'",           # 字符串包含
              )
        print("✓ 各种数据类型校验通过")
        
        # 测试类型匹配校验
        print("测试类型匹配校验...")
        check(response,
              "string_field @= 'str'",           # 字符串类型
              "number_field @= 'int'",           # 整数类型
              "float_field @= 'float'",          # 浮点数类型
              "boolean_field @= 'bool'",         # 布尔类型
              "null_field @= 'none'",            # None类型
              "array_field @= 'list'",           # 列表类型
              "object_field @= 'dict'",          # 字典类型
              )
        print("✓ 类型匹配校验通过")
        
    except Exception as e:
        print(f"✗ 数据类型测试失败: {e}")
        return False
    
    return True


def main():
    """主测试函数"""
    print("开始测试新的数据校验函数...")
    
    tests = [
        test_basic_validation,
        test_specialized_functions,
        test_error_handling,
        test_data_types
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        if test_func():
            passed += 1
    
    print(f"\n=== 测试结果 ===")
    print(f"总测试: {total}")
    print(f"通过: {passed}")
    print(f"失败: {total - passed}")
    
    if passed == total:
        print("🎉 所有测试都通过了！新的数据校验函数工作正常。")
        return True
    else:
        print("❌ 部分测试失败，请检查实现。")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 