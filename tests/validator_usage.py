#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
General-Validator 使用示例
展示新的validator风格和向后兼容的checker风格
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from general_validator.logger import setup_logger

from general_validator import (
    # 新风格API（推荐使用）
    validate, validate_when, validate_list, DataValidator, validator,
    
    # 旧风格API（向后兼容）
    check, check_when, check_list, DataChecker, checker
)

def main():
    print("🚀 General-Validator API 使用示例")
    print("=" * 50)
    
    # 测试数据
    response_data = {
        "status_code": 200,
        "data": {
            "user": {
                "id": 12345,
                "name": "张三",
                "email": "zhangsan@example.com",
                "age": 28
            },
            "products": [
                {"id": 1, "name": "商品A", "price": 99.9, "status": "active"},
                {"id": 2, "name": "商品B", "price": 199.8, "status": "active"}
            ]
        }
    }
    
    print("\n📋 测试数据:")
    print(f"  用户: {response_data['data']['user']['name']}")
    print(f"  商品数量: {len(response_data['data']['products'])}")
    
    # ==============================
    # 新风格API使用示例
    # ==============================
    print("\n🆕 新风格 API 示例 (推荐使用)")
    print("-" * 30)
    
    # 1. 函数式调用 - validate()
    print("1️⃣ 函数式调用 - validate():")
    result = validate(response_data,
                     "status_code == 200",
                     "data.user.id > 0",
                     "data.user.name",
                     "data.user.email",
                     "data.products.*.id > 0",
                     "data.products.*.price > 0")
    print(f"   结果: {'✅ 通过' if result else '❌ 失败'}")
    
    # 2. 条件校验 - validate_when()
    print("\n2️⃣ 条件校验 - validate_when():")
    result = validate_when(response_data, 
                          "status_code == 200", 
                          "data.user.id > 0")
    print(f"   结果: {'✅ 通过' if result else '❌ 失败'}")
    
    # 3. 列表批量校验 - validate_list()
    print("\n3️⃣ 列表批量校验 - validate_list():")
    result = validate_list(response_data['data']['products'],
                          "name", "status",
                          id="> 0",
                          price=">= 50")
    print(f"   结果: {'✅ 通过' if result else '❌ 失败'}")
    
    # 4. 链式调用 - DataValidator
    print("\n4️⃣ 链式调用 - DataValidator:")
    result = (DataValidator(response_data)
              .equals("status_code", 200)
              .not_empty("data.user.name", "data.user.email")
              .greater_than("data.user.age", 18)
              .is_positive("data.user.id")
              .when("status_code == 200", "data.user.id > 0")
              .validate())
    print(f"   结果: {'✅ 通过' if result else '❌ 失败'}")
    
    # 5. 工厂函数 - validator()
    print("\n5️⃣ 工厂函数 - validator():")
    result = (validator(response_data)
              .not_empty("data.user.name")
              .is_email("data.user.email")
              .between("data.user.age", 18, 65)
              .validate())
    print(f"   结果: {'✅ 通过' if result else '❌ 失败'}")
    
    # ==============================
    # 旧风格API使用示例（向后兼容）
    # ==============================
    print("\n🔄 旧风格 API 示例 (向后兼容)")
    print("-" * 30)
    
    # 1. 函数式调用 - check()
    print("1️⃣ 函数式调用 - check():")
    result = check(response_data,
                  "status_code == 200",
                  "data.user.id > 0",
                  "data.user.name",
                  "data.products.*.price > 0")
    print(f"   结果: {'✅ 通过' if result else '❌ 失败'}")
    
    # 2. 条件校验 - check_when()
    print("\n2️⃣ 条件校验 - check_when():")
    result = check_when(response_data, 
                       "status_code == 200", 
                       "data.user.name")
    print(f"   结果: {'✅ 通过' if result else '❌ 失败'}")
    
    # 3. 列表批量校验 - check_list()
    print("\n3️⃣ 列表批量校验 - check_list():")
    result = check_list(response_data['data']['products'],
                       "name",
                       id="> 0",
                       price="> 0")
    print(f"   结果: {'✅ 通过' if result else '❌ 失败'}")
    
    # 4. 链式调用 - DataChecker (旧名称)
    print("\n4️⃣ 链式调用 - DataChecker (旧名称):")
    result = (DataChecker(response_data)
              .equals("status_code", 200)
              .not_empty("data.user.name")
              .greater_than("data.user.id", 0)
              .validate())
    print(f"   结果: {'✅ 通过' if result else '❌ 失败'}")
    
    # 5. 工厂函数 - checker() (旧名称)
    print("\n5️⃣ 工厂函数 - checker() (旧名称):")
    result = (checker(response_data)
              .not_empty("data.user.name")
              .greater_than("data.user.age", 0)
              .validate())
    print(f"   结果: {'✅ 通过' if result else '❌ 失败'}")
    
    # ==============================
    # 总结
    # ==============================
    print("\n📝 总结")
    print("-" * 30)
    print("✅ 新风格API（推荐）:")
    print("   - validate(), validate_when(), validate_list(), validate_nested()")
    print("   - DataValidator, validator()")
    print("")
    print("🔄 旧风格API（向后兼容）:")
    print("   - check(), check_when(), check_list(), check_nested()")
    print("   - DataChecker, checker()")
    print("")
    print("💡 两种风格的API功能完全相同，可以自由选择使用！")
    print("   建议新项目使用validator风格，老项目可以继续使用checker风格。")

if __name__ == "__main__":
    setup_logger('INFO')
    main() 