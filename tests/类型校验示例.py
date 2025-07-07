#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
类型校验功能示例
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from general_validator.logger import setup_logger
from general_validator.checker import check

def example_type_validation():
    """类型校验示例"""
    print("=== 类型校验功能示例 ===")
    
    # 示例数据
    api_response = {
        "user_id": 12345,                    # 整数
        "username": "test_user",             # 字符串
        "email": "test@example.com",         # 字符串
        "age": 25,                           # 整数
        "height": 175.5,                     # 浮点数
        "is_active": True,                   # 布尔值
        "is_premium": False,                 # 布尔值
        "tags": ["python", "testing"],      # 列表
        "profile": {                         # 字典
            "bio": "Software Developer",
            "location": "Beijing"
        },
        "scores": (95, 87, 92),             # 元组
        "skills": {"python", "java"},       # 集合
        "avatar": None                       # None值
    }
    
    print("1. 基础类型校验...")
    result = check(api_response,
                   "user_id @= 'int'",           # 整数类型
                   "username @= 'str'",          # 字符串类型
                   "email @= 'string'",          # 字符串类型（别名）
                   "age @= 'int'",               # 整数类型
                   "height @= 'float'",          # 浮点数类型
                   )
    print(f"✓ 基础类型校验结果: {result}")
    
    print("2. 布尔类型校验...")
    result = check(api_response,
                   "is_active @= 'bool'",        # 布尔类型
                   "is_premium @= 'boolean'",    # 布尔类型（别名）
                   )
    print(f"✓ 布尔类型校验结果: {result}")
    
    print("3. 容器类型校验...")
    result = check(api_response,
                   "tags @= 'list'",             # 列表类型
                   "profile @= 'dict'",          # 字典类型
                   "scores @= 'tuple'",          # 元组类型
                   "skills @= 'set'",            # 集合类型
                   )
    print(f"✓ 容器类型校验结果: {result}")
    
    print("4. None类型校验...")
    result = check(api_response,
                   "avatar @= 'none'",           # None类型
                   )
    print(f"✓ None类型校验结果: {result}")
    
    print("5. 类型不匹配测试...")
    # 故意使用错误的类型进行测试
    result = check(api_response,
                   "user_id @= 'str'",           # 错误：整数不是字符串
                   )
    print(f"✓ 类型不匹配测试结果: {result} (应该为False)")
    
    print("6. 组合校验（值校验 + 类型校验）...")
    result = check(api_response,
                   "user_id > 0",                # 值校验：大于0
                   "user_id @= 'int'",           # 类型校验：整数类型
                   "username",                   # 非空校验
                   "username @= 'str'",          # 类型校验：字符串类型
                   "email *= '@'",               # 值校验：包含@
                   "email @= 'str'",             # 类型校验：字符串类型
                   "is_active == true",          # 值校验：等于true
                   "is_active @= 'bool'",        # 类型校验：布尔类型
                   )
    print(f"✓ 组合校验结果: {result}")


def example_list_type_validation():
    """列表数据类型校验示例"""
    print("\n=== 列表数据类型校验示例 ===")
    
    # 用户列表数据
    users = [
        {
            "id": 1,
            "name": "Alice",
            "age": 25,
            "salary": 5000.0,
            "is_active": True,
            "tags": ["developer", "python"]
        },
        {
            "id": 2,
            "name": "Bob", 
            "age": 30,
            "salary": 6000.0,
            "is_active": False,
            "tags": ["manager", "java"]
        }
    ]
    
    print("批量类型校验...")
    result = check(users,
                   "*.id @= 'int'",              # 所有ID都是整数
                   "*.name @= 'str'",            # 所有姓名都是字符串
                   "*.age @= 'int'",             # 所有年龄都是整数
                   "*.salary @= 'float'",        # 所有薪资都是浮点数
                   "*.is_active @= 'bool'",      # 所有状态都是布尔值
                   "*.tags @= 'list'",           # 所有标签都是列表
                   )
    print(f"✓ 批量类型校验结果: {result}")


def example_nested_type_validation():
    """嵌套数据类型校验示例"""
    print("\n=== 嵌套数据类型校验示例 ===")
    
    # 复杂嵌套数据
    company_data = {
        "company": {
            "id": 100,
            "name": "Tech Corp",
            "founded": 2010,
            "is_public": True,
            "departments": [
                {
                    "id": 1,
                    "name": "Engineering",
                    "budget": 1000000.0,
                    "employees": [
                        {"id": 101, "name": "Alice", "level": 5},
                        {"id": 102, "name": "Bob", "level": 3}
                    ]
                },
                {
                    "id": 2,
                    "name": "Marketing",
                    "budget": 500000.0,
                    "employees": [
                        {"id": 201, "name": "Carol", "level": 4}
                    ]
                }
            ]
        }
    }
    
    print("嵌套结构类型校验...")
    result = check(company_data,
                   # 公司基础信息类型校验
                   "company.id @= 'int'",
                   "company.name @= 'str'",
                   "company.founded @= 'int'",
                   "company.is_public @= 'bool'",
                   "company.departments @= 'list'",
                   
                   # 部门信息类型校验
                   "company.departments.*.id @= 'int'",
                   "company.departments.*.name @= 'str'",
                   "company.departments.*.budget @= 'float'",
                   "company.departments.*.employees @= 'list'",
                   
                   # 员工信息类型校验
                   "company.departments.*.employees.*.id @= 'int'",
                   "company.departments.*.employees.*.name @= 'str'",
                   "company.departments.*.employees.*.level @= 'int'",
                   )
    print(f"✓ 嵌套结构类型校验结果: {result}")


def example_type_validation_errors():
    """类型校验错误示例"""
    print("\n=== 类型校验错误处理示例 ===")
    
    # 包含类型错误的数据
    bad_data = {
        "id": "should_be_int",      # 应该是整数但是字符串
        "name": 12345,              # 应该是字符串但是整数
        "is_active": "true",        # 应该是布尔值但是字符串
        "tags": "should_be_list",   # 应该是列表但是字符串
        "profile": "should_be_dict" # 应该是字典但是字符串
    }
    
    print("1. 单个类型错误...")
    result = check(bad_data, "id @= 'int'")
    print(f"✓ 类型错误结果: {result} (应该为False)")
    
    print("2. 多个类型错误...")
    result = check(bad_data,
                   "id @= 'int'",
                   "name @= 'str'", 
                   "is_active @= 'bool'",
                   "tags @= 'list'",
                   "profile @= 'dict'",
                   )
    print(f"✓ 多个类型错误结果: {result} (应该为False)")
    
    print("3. 混合校验（部分成功部分失败）...")
    mixed_data = {
        "id": 123,                  # 正确：整数
        "name": "test",             # 正确：字符串
        "age": "should_be_int",     # 错误：应该是整数
        "is_active": True           # 正确：布尔值
    }
    
    result = check(mixed_data,
                   "id @= 'int'",           # 成功
                   "name @= 'str'",         # 成功
                   "age @= 'int'",          # 失败
                   "is_active @= 'bool'",   # 成功
                   )
    print(f"✓ 混合校验结果: {result} (应该为False，因为存在失败项)")


def main():
    """主函数"""
    print("🔍 类型校验功能完整示例")
    print("=" * 50)
    
    try:
        example_type_validation()
        example_list_type_validation()
        example_nested_type_validation()
        example_type_validation_errors()
        
        print("\n" + "=" * 50)
        print("🎉 类型校验示例运行完成！")
        print("\n📋 支持的类型名称:")
        print("  - 'int' / 'integer'     : 整数类型")
        print("  - 'float'               : 浮点数类型")
        print("  - 'str' / 'string'      : 字符串类型")
        print("  - 'bool' / 'boolean'    : 布尔类型")
        print("  - 'list'                : 列表类型")
        print("  - 'dict'                : 字典类型")
        print("  - 'tuple'               : 元组类型")
        print("  - 'set'                 : 集合类型")
        print("  - 'none' / 'null'       : None类型")
        
    except Exception as e:
        print(f"\n❌ 示例运行出错: {e}")


if __name__ == "__main__":
    main() 