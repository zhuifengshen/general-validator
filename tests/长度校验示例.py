#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
长度校验示例 - 展示新增的长度校验操作符功能

新增的长度校验操作符：
- #= 长度等于
- #!= 长度不等于  
- #> 长度大于
- #>= 长度大于等于
- #< 长度小于
- #<= 长度小于等于

设计理念：使用 # 作为长度校验的前缀，简洁易记，减轻用户记忆负担
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from general_validator.logger import setup_logger
from general_validator.checker import check, checker, check_when

def test_length_validation_operators():
    """测试长度校验操作符"""
    print("🔍 长度校验操作符测试")
    print("=" * 50)
    
    # 设置INFO级别
    setup_logger("INFO")
    
    # 测试数据
    test_data = {
        "user": {
            "name": "张三",      # 长度为2
            "email": "test@example.com",  # 长度为16
            "tags": ["vip", "premium"],   # 长度为2
            "description": ""             # 长度为0
        },
        "products": [
            {"name": "商品A", "features": ["新品", "热销"]},  # name长度2, features长度2
            {"name": "商品B", "features": ["限时优惠"]},      # name长度2, features长度1
            {"name": "商品C", "features": []}               # name长度2, features长度0
        ]
    }
    
    print("\n1. 基础长度校验操作符测试")
    print("-" * 30)
    
    # 长度等于
    result = check(test_data, "user.name #= 2")
    print(f"user.name #= 2: {result}")  # True
    
    # 长度不等于
    result = check(test_data, "user.description #!= 0")
    print(f"user.description #!= 0: {result}")  # False
    
    # 长度大于
    result = check(test_data, "user.email #> 10")
    print(f"user.email #> 10: {result}")  # True
    
    # 长度大于等于
    result = check(test_data, "user.tags #>= 2")
    print(f"user.tags #>= 2: {result}")  # True
    
    # 长度小于
    result = check(test_data, "user.name #< 5")
    print(f"user.name #< 5: {result}")  # True
    
    # 长度小于等于
    result = check(test_data, "user.tags #<= 2")
    print(f"user.tags #<= 2: {result}")  # True
    
    print("\n2. 批量长度校验测试")
    print("-" * 30)
    
    # 同时校验多个字段的长度
    result = check(test_data, 
                   "user.name #>= 1",      # 姓名至少1个字符
                   "user.email #> 5",      # 邮箱长度大于5
                   "user.tags #<= 10")     # 标签数量不超过10个
    print(f"批量长度校验: {result}")
    
    print("\n3. 通配符长度校验测试")
    print("-" * 30)
    
    # 所有商品名称长度都大于0
    result = check(test_data, "products.*.name #> 0")
    print(f"products.*.name #> 0: {result}")  # True
    
    # 所有商品特性列表长度都大于等于0
    result = check(test_data, "products.*.features #>= 0")  
    print(f"products.*.features #>= 0: {result}")  # True
    
    # 所有商品特性列表长度都大于0（会失败，因为有空列表）
    result = check(test_data, "products.*.features #> 0")
    print(f"products.*.features #> 0: {result}")  # False

def test_length_validation_chain():
    """测试链式调用中的长度校验"""
    print("\n🔗 链式调用长度校验测试")
    print("=" * 50)
    
    test_data = {
        "form": {
            "username": "admin",      # 长度5
            "password": "123456789",  # 长度9
            "confirm": "123456789",   # 长度9
            "comments": "很好的产品！推荐使用"  # 长度10
        }
    }
    
    # 使用链式调用进行长度校验
    result = checker(test_data)\
        .length_greater_equal("form.username", 3)\
        .length_less_equal("form.username", 20)\
        .length_greater_equal("form.password", 8)\
        .length_less_equal("form.password", 50)\
        .length_equals("form.confirm", 9)\
        .length_greater_than("form.comments", 5)\
        .validate()
    
    print(f"表单长度校验结果: {result}")
    
    # 测试一些会失败的情况
    print("\n测试失败情况:")
    result = checker(test_data)\
        .length_greater_than("form.username", 10)\
        .validate()
    print(f"用户名长度 > 10: {result}")  # False

def test_length_validation_with_conditions():
    """测试长度校验与条件校验的结合"""
    print("\n🎯 长度校验与条件校验结合测试")
    print("=" * 50)
    
    test_data = {
        "article": {
            "type": "premium",
            "title": "高级文章标题",  # 长度6
            "content": "这是一篇很长的高级文章内容，包含了很多有价值的信息...",  # 长度较长
            "tags": ["技术", "深度", "原创"]  # 长度3
        }
    }
    
    # 当文章类型为premium时，标题长度必须大于5
    result = check_when(test_data, "article.type == 'premium'", "article.title #> 5")
    print(f"premium文章标题长度校验: {result}")  # True
    
    # 当文章有标签时，标签数量必须在1-5之间
    result = check_when(test_data, "article.tags #> 0", "article.tags #<= 5")
    print(f"标签数量范围校验: {result}")  # True
    
    # 当文章内容长度大于20时，必须有标签
    result = check_when(test_data, "article.content #> 20", "article.tags #> 0")
    print(f"长文章必须有标签: {result}")  # True

def test_length_validation_comparison():
    """对比传统方式和新操作符的使用体验"""
    print("\n📊 使用体验对比")
    print("=" * 50)
    
    test_data = {"text": "hello world"}  # 长度11
    
    print("传统方式 vs 新操作符:")
    print("1. 传统方式（字典格式）:")
    traditional_rule = {
        'field': 'text',
        'validator': 'length_gt',
        'expect': 5
    }
    result = check(test_data, traditional_rule)
    print(f"   字典格式校验: {result}")
    
    print("2. 新操作符（字符串格式）:")
    result = check(test_data, "text #> 5")
    print(f"   字符串格式校验: {result}")
    
    print("\n优势对比:")
    print("✅ 新操作符优势:")
    print("   - 更简洁：'text #> 5' vs 复杂的字典结构")
    print("   - 更直观：# 符号容易理解为长度/数量")
    print("   - 减少记忆负担：与现有比较操作符保持一致")
    print("   - 支持混合使用：可与其他校验器自由组合")

if __name__ == "__main__":
    # test_length_validation_operators()
    # test_length_validation_chain()
    test_length_validation_with_conditions()
    # test_length_validation_comparison()
    
    print("\n" + "=" * 50)
    print("✅ 长度校验操作符测试完成")
    print("\n💡 操作符总览:")
    print("   #=   长度等于")
    print("   #!=  长度不等于")
    print("   #>   长度大于")
    print("   #>=  长度大于等于")
    print("   #<   长度小于")
    print("   #<=  长度小于等于")
    print("\n🎯 设计理念:")
    print("   - 使用 # 作为长度校验前缀，简洁易记")
    print("   - 与现有比较操作符保持一致的逻辑")
    print("   - 减轻用户记忆负担，提升使用体验")
    print("   - 完美融入现有的极简数据校验体系") 