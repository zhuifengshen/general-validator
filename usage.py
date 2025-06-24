#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
新数据校验函数使用示例
"""

from src.general_validator.logger import setup_logger
from src.general_validator.checker import check, check_list, check_nested, checker

def example_api_response_validation():
    """API响应数据校验示例"""
    print("=== API响应数据校验示例 ===")
    
    # 模拟接口返回的数据
    api_response = {
        "status_code": 200,
        "message": "success",
        "timestamp": 1640995200,
        "data": {
            "user": {
                "id": 12345,
                "username": "test_user",
                "email": "test@example.com",
                "is_active": True,
                "balance": 99.99
            },
            "products": [
                {
                    "id": 1,
                    "name": "iPhone 14",
                    "price": 5999.0,
                    "category": "手机",
                    "stock": 100,
                    "tags": ["苹果", "智能手机"],
                    "reviews": [
                        {"id": 101, "rating": 5, "comment": "很好用"},
                        {"id": 102, "rating": 4, "comment": "不错"}
                    ]
                },
                {
                    "id": 2,
                    "name": "MacBook Pro",
                    "price": 12999.0,
                    "category": "电脑",
                    "stock": 50,
                    "tags": ["苹果", "笔记本"],
                    "reviews": [
                        {"id": 201, "rating": 5, "comment": "性能强劲"}
                    ]
                }
            ]
        }
    }
    
    print("1. 基础响应校验...")
    # 校验基础响应结构
    check(api_response,
          "status_code == 200",           # 状态码正确
          "message == 'success'",         # 消息正确
          "timestamp > 0",                # 时间戳有效
          "data.user.id > 0",             # 用户ID有效
          "data.user.username",           # 用户名非空
          "data.user.email *= '@'",       # 邮箱包含@
          "data.user.is_active == true",  # 用户状态激活
          "data.user.balance >= 0",       # 余额非负
          )
    print("✓ 基础响应校验通过")
    
    print("1.1 类型校验...")
    # 校验数据类型
    check(api_response,
          "status_code @= 'int'",         # 状态码是整数
          "message @= 'str'",             # 消息是字符串
          "timestamp @= 'int'",           # 时间戳是整数
          "data.user.id @= 'int'",        # 用户ID是整数
          "data.user.username @= 'str'",  # 用户名是字符串
          "data.user.is_active @= 'bool'", # 状态是布尔值
          "data.products @= 'list'",      # 商品列表是数组
          )
    print("✓ 类型校验通过")
    
    print("2. 商品列表批量校验...")
    # 校验商品列表
    check(api_response,
          "data.products.*.id > 0",           # 所有商品ID有效
          "data.products.*.name",             # 所有商品名称非空
          "data.products.*.price > 0",        # 所有商品价格大于0
          "data.products.*.category",         # 所有商品分类非空
          "data.products.*.stock >= 0",       # 所有商品库存非负
          )
    print("✓ 商品列表批量校验通过")
    
    print("3. 嵌套评论数据校验...")
    # 校验嵌套的评论数据
    check(api_response,
          "data.products.*.reviews.*.id > 0",        # 评论ID有效
          "data.products.*.reviews.*.rating >= 1",   # 评分至少1分
          "data.products.*.reviews.*.rating <= 5",   # 评分最多5分
          "data.products.*.reviews.*.comment",       # 评论内容非空
          )
    print("✓ 嵌套评论数据校验通过")


def example_list_validation():
    """列表数据专用校验示例"""
    print("\n=== 列表数据专用校验示例 ===")
    
    # 商品列表数据
    product_list = [
        {"id": 1, "name": "商品1", "price": 99.99, "status": "active"},
        {"id": 2, "name": "商品2", "price": 199.99, "status": "active"},
        {"id": 3, "name": "商品3", "price": 299.99, "status": "inactive"}
    ]
    
    print("使用check_list函数进行批量校验...")
    # 使用专用的列表校验函数
    check_list(product_list,
               "id", "name", "status",          # 默认非空校验
               id="> 0",                        # ID大于0
               price=">= 0",                    # 价格非负
               status="*= 'active'")            # 状态包含active (这个会部分失败，但演示用法)
    
    print("✓ 列表数据校验完成")


def example_nested_validation():
    """嵌套列表专用校验示例"""
    print("\n=== 嵌套列表专用校验示例 ===")
    
    # 包含嵌套结构的数据
    order_data = {
        "orders": [
            {
                "id": 1001,
                "customer": "张三",
                "items": [
                    {"product_id": 1, "name": "商品A", "quantity": 2, "price": 50.0},
                    {"product_id": 2, "name": "商品B", "quantity": 1, "price": 100.0}
                ]
            },
            {
                "id": 1002,
                "customer": "李四",
                "items": [
                    {"product_id": 3, "name": "商品C", "quantity": 3, "price": 30.0}
                ]
            }
        ]
    }
    
    print("使用check_nested函数校验嵌套数据...")
    # 使用专用的嵌套列表校验函数
    check_nested(order_data, "orders", "items",
                 "product_id > 0",      # 商品ID有效
                 "name",                # 商品名称非空
                 "quantity > 0",        # 数量大于0
                 "price > 0")           # 价格大于0
    
    print("✓ 嵌套列表校验完成")


def example_chain_validation():
    """链式调用校验示例"""
    print("\n=== 链式调用校验示例 ===")
    
    user_data = {
        "id": 12345,
        "username": "test_user",
        "email": "test@example.com",
        "age": 25,
        "score": 85.5,
        "is_vip": True
    }
    
    print("使用链式调用进行校验...")
    # 使用链式调用方式
    result = checker(user_data)\
        .not_empty("username", "email")\
        .equals("id", 12345)\
        .greater_than("age", 18)\
        .greater_than("score", 60.0)\
        .equals("is_vip", True)\
        .validate()
    
    print("✓ 链式调用校验完成")


def example_error_handling():
    """错误处理示例"""
    print("\n=== 错误处理示例 ===")
    
    # 包含错误的数据
    bad_data = {
        "status": "error",
        "user": {
            "id": 0,  # 无效ID
            "name": "",  # 空名称
            "age": -5  # 无效年龄
        }
    }
    
    print("1. 校验失败返回False...")
    result = check(bad_data,
                   "status == 'success'",  # 这会失败
                   "user.id > 0",          # 这会失败
                   "user.name",            # 这会失败
                   )
    
    if result == False:
        print("✓ 校验失败正确返回False")
    else:
        print("✗ 应该返回False")
    
    print("2. 数据结构异常抛出异常...")
    try:
        check(bad_data,
              "user.invalid_field",  # 字段不存在，应该抛出异常
              )
        print("✗ 应该抛出异常")
    except Exception:
        print("✓ 数据结构异常正确抛出异常")
    
    print("3. 部分成功部分失败的情况...")
    result = check(bad_data,
                   "status",               # 成功（非空）
                   "user.id > 0",          # 失败
                   "user.name",            # 失败
                   )
    
    if result == False:
        print("✓ 部分失败情况正确返回False")
    else:
        print("✗ 应该返回False")


def main():
    """主函数"""
    print("🚀 新数据校验函数使用示例")
    print("=" * 50)
    
    try:
        example_api_response_validation()
        example_list_validation()
        example_nested_validation()
        example_chain_validation()
        example_error_handling()
        
        print("\n" + "=" * 50)
        print("🎉 所有示例运行完成！")
        print("\n📖 更多用法请参考《数据校验使用文档.md》")
        
    except Exception as e:
        print(f"\n❌ 示例运行出错: {e}")


if __name__ == "__main__":
    setup_logger("DEBUG")
    main() 