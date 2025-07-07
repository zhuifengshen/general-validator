# General-Validator

## 概述

general-validator 是一款极简通用数据批量校验器，支持所有常用校验器，适用于数据接口测试中各种校验场景。

## 核心特性

- **极简调用**: 一个函数搞定所有场景
- **默认非空**: 无需记忆，符合最常见使用场景  
- **直观语法**: `"field > 0"` 比复杂配置更好理解
- **智能解析**: 自动推断数据类型
- **通配符支持**: `*.field` 实现批量校验
- **零学习成本**: 接近自然语言的表达式


## 主要函数

### 1. check() - 核心校验函数

最主要的校验函数，支持多种简洁的调用方式。

#### 基本语法
```python
check(data, *validations)
```

#### 参数说明
- `data`: 要校验的数据
- `validations`: 校验规则（支持字符串和字典格式）

#### 返回值说明
- `True`: 所有校验都通过
- `False`: 存在校验失败
- 抛出异常: 当参数错误或数据结构异常时

### 2. check_not_empty() - 专门非空校验

```python
check_not_empty(data, *field_paths)
```

### 3. check_when() - 条件校验
```python
check_when(data, condition, *then)
```

### 4. check_list() - 列表批量校验

```python
check_list(data_list, *validations)
```

### 5. check_array() - 列表批量校验（参数示意版）

```python
check_array(data_list, *field_names, **validators)
```

### 6. check_nested() - 嵌套列表校验

```python
check_nested(data, list_path, nested_field, *field_validations)
```

### 7. checker() - 链式调用

```python
checker(data).not_empty("field1").equals("field2", value).validate()
```

**支持的链式调用方法：**

#### 基础校验
- `not_empty(*paths)` - 批量非空校验
- `equals(path, value)` - 等于校验
- `not_equals(path, value)` - 不等于校验

#### 数值校验
- `greater_than(path, value)` - 大于校验
- `greater_equal(path, value)` - 大于等于校验
- `less_than(path, value)` - 小于校验
- `less_equal(path, value)` - 小于等于校验
- `between(path, min_value, max_value, inclusive=True)` - 范围校验
- `is_positive(path)` - 正数校验
- `is_negative(path)` - 负数校验
- `is_non_negative(path)` - 非负数校验

#### 字符串校验
- `starts_with(path, prefix)` - 以指定字符串开头
- `ends_with(path, suffix)` - 以指定字符串结尾
- `contains(path, substring)` - 包含指定字符串
- `contained_by(path, container)` - 被指定字符串包含
- `matches_regex(path, pattern)` - 正则表达式匹配
- `is_email(path)` - 邮箱格式校验
- `is_phone(path)` - 手机号格式校验
- `is_url(path)` - URL格式校验

#### 类型校验
- `is_type(path, expected_type)` - 通用类型校验
- `is_string(path)` - 字符串类型校验
- `is_number(path)` - 数字类型校验（int或float）
- `is_integer(path)` - 整数类型校验
- `is_float(path)` - 浮点数类型校验
- `is_boolean(path)` - 布尔类型校验
- `is_list(path)` - 列表类型校验
- `is_dict(path)` - 字典类型校验
- `is_none(path)` - None类型校验

#### 集合校验
- `in_values(path, values)` - 值在指定集合中
- `not_in_values(path, values)` - 值不在指定集合中

#### 长度校验
- `length_equals(path, length)` - 长度等于指定值
- `length_greater_than(path, length)` - 长度大于指定值
- `length_less_than(path, length)` - 长度小于指定值
- `length_greater_equal(path, length)` - 长度大于等于指定值
- `length_less_equal(path, length)` - 长度小于等于指定值
- `length_between(path, min_length, max_length)` - 长度在指定范围内

#### 批量校验
- `all_fields_not_empty(*paths)` - 批量非空校验
- `all_fields_positive(*paths)` - 批量正数校验
- `all_fields_type(field_type, *paths)` - 批量类型校验

#### 条件校验
- `when(condition, then)` - 条件校验：当条件满足时执行then校验

## 支持的校验器

### 比较操作符
| 操作符 | 说明 | 示例 |
|--------|------|------|
| `==` | 等于 | `"status_code == 200"` |
| `!=` | 不等于 | `"status != 'error'"` |
| `>` | 大于 | `"price > 0"` |
| `>=` | 大于等于 | `"count >= 1"` |
| `<` | 小于 | `"age < 100"` |
| `<=` | 小于等于 | `"score <= 100"` |

### 字符串操作符
| 操作符 | 说明 | 示例 |
|--------|------|------|
| `^=` | 以...开头 | `"name ^= 'test'"` |
| `$=` | 以...结尾 | `"email $= '@qq.com'"` |
| `~=` | 正则匹配 | `"phone ~= '^1[3-9]\\d{9}$'"` |

### 列表、元组、字典、字符串等操作符
| 操作符 | 说明 | 示例 |
|--------|------|------|
| `*=` | 包含 | `"description *= '商品'"` |
| `=*` | 被包含 | `"'a' =* 'abc'"` |
| `#=` | 长度等于 | `"name #= 5"` |
| `#!=` | 长度不等于 | `"list #!= 0"` |
| `#>` | 长度大于 | `"content #> 10"` |
| `#>=` | 长度大于等于 | `"tags #>= 1"` |
| `#<` | 长度小于 | `"title #< 50"` |
| `#<=` | 长度小于等于 | `"items #<= 100"` |

### 类型操作符
| 操作符 | 说明 | 示例 |
|--------|------|------|
| `@=` | 类型匹配 | `"age @= 'int'"`，更多如下： |
|      |        | `int`/`integer`：整数类型 |
|      |        | `float`：浮点数类型 |
|      |        | `str`/`string`：字符串类型 |
|      |        | `bool`/`boolean`：布尔类型 |
|      |        | `list`：列表类型 |
|      |        | `dict`：字典类型 |
|      |        | `tuple`：元组类型 |
|      |        | `set`：集合类型 |
|      |        | `none`/`null`：None类型 |


### 默认校验器
- 无操作符时默认为非空校验
- 支持嵌套路径和通配符

## 使用示例

### 基础用法

```python
# 示例数据
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

# 1. 最简单的非空校验
check(response, "data.product.id", "data.product.name")

# 2. 带校验器的简洁语法  
check(response, 
      "status_code == 200",
      "data.product.id > 0", 
      "data.product.price >= 10")

# 3. 混合校验
check(response, 
      "data.product.id",           # 默认非空
      "data.product.price > 0",    # 大于0
      "status_code == 200",        # 等于200
      "message ^= 'suc'")          # 以'suc'开头

# 4. 通配符批量校验
check(response, 
      "data.productList.*.id",           # 所有商品ID非空
      "data.productList.*.name",         # 所有商品名称非空
      "data.productList.*.id > 0",       # 所有商品ID大于0
      "data.productList.*.price >= 0")   # 所有商品价格大于等于0

# 5. 嵌套列表校验
check(response, 
      "data.productList.*.purchasePlan.*.id > 0",
      "data.productList.*.purchasePlan.*.name",
      "data.productList.*.purchasePlan.*.amount >= 100")
```

### 专用函数用法

```python
# 1. 专门的非空校验
check_not_empty(response, "data.product.id", "data.product.name", "message")

# 2. 列表批量校验
check_list(response["data"]["productList"], 
           "id", "name",                    # 默认非空
           "price > 0", "id > 0")           # 带校验器

# 3. 嵌套列表校验
check_nested(response, "data.productList", "purchasePlan",
             "id > 0", "name", "amount >= 50")

# 4. 链式调用
checker(response)\
    .not_empty("data.product.id", "data.product.name")\
    .equals("status_code", 200)\
    .greater_than("data.product.id", 0)\
    .validate()
```

### 字典格式校验

```python
# 字典格式（兼容旧版本）
check(response, {
    "field": "data.product.id",
    "validator": "gt",
    "expect": 0
})

# 混合使用字符串和字典格式
check(response,
      "status_code == 200",              # 字符串格式
      {"field": "data.product.id", "validator": "gt", "expect": 0},  # 字典格式
      "data.product.name")               # 默认非空
```

### 高级用法

```python
# 1. 校验结果处理
result = check(response, 
               "status_code == 200",
               "data.product.id > 0",
               "data.product.name")

if result:
    print("所有校验都通过")
else:
    print("存在校验失败")

# 2. 异常处理
try:
    result = check(response, "data.invalid_field")  # 字段不存在
except Exception as e:
    print(f"数据结构异常: {e}")

# 3. 复杂数据类型校验
result = check(response,
               "data.productList.*.status == 'active'",     # 字符串相等
               "data.product.price >= 10.5",                # 浮点数比较
               "data.product.description *= '测试'",         # 字符串包含
               "data.product.id @= 'int'",                  # 类型匹配
               "data.productList @= 'list'")                # 列表类型
```

## 在测试用例中的使用

### YAML测试文件中使用

```yaml
# testcase.yml
name: 商品接口测试
request:
  url: /api/products
  method: GET

validate:
  # 极简语法 - 默认非空
  - ${check(content, "content.data.product.id", "content.data.product.name")}
  - True
  
  # 带校验器的简洁语法
  - ${check(content, "status_code == 200", "content.data.product.id > 0")}
  - True
  
  # 通配符批量校验
  - check(content, "content.data.productList.*.id", "content.data.productList.*.name")
  - True

  # 列表专用
  - ${check_list("content.data.productList", "id", "name", "price = > 0")}
  - True
      
  # 嵌套列表专用
  - ${check_nested(content, "data.productList", "purchasePlan", "id > 0", "name", "amount >= 100")}
  - True
```

### Python测试文件中使用

```python
# test_products.py
import pytest
from debugtalk import check, check_list, check_nested

class TestProducts:
    
    def test_product_detail(self, response):
        """商品详情接口测试"""
        # 基础校验
        check(response, 
              "status_code == 200",
              "data.product.id > 0",
              "data.product.name",
              "data.product.price >= 0")
    
    def test_product_list(self, response):
        """商品列表接口测试"""
        # 列表批量校验
        check_list(response["data"]["productList"],
                   "id", "name", "price",           # 非空校验
                   "id > 0", "price >= 0")          # 数值校验
    
    def test_nested_purchase_plan(self, response):
        """嵌套购买计划测试"""
        # 嵌套列表校验
        check_nested(response, "data.productList", "purchasePlan",
                     "id > 0", "name", "amount >= 100")
    
    def test_comprehensive_validation(self, response):
        """综合校验测试"""
        # 一次性校验多个层级的数据
        check(response,
              # 基础响应校验
              "status_code == 200",
              "message == 'success'",
              
              # 商品基础信息校验
              "data.product.id > 0",
              "data.product.name",
              "data.product.price >= 0",
              
              # 商品列表批量校验
              "data.productList.*.id > 0",
              "data.productList.*.name",
              "data.productList.*.status == 'active'",
              
              # 嵌套购买计划校验
              "data.productList.*.purchasePlan.*.id > 0",
              "data.productList.*.purchasePlan.*.amount >= 100")
```

## 错误处理

### 常见错误类型

1. **字段不存在**: `KeyError: 字段不存在: data.invalid_field`
2. **类型错误**: `TypeError: 无法在str上访问字段: field`
3. **索引错误**: `IndexError: 索引超出范围: data.list.10`
4. **校验失败**: `AssertionError: 不大于: data.product.id = 0, 期望 > 0`

### 错误处理策略

```python
# 1. 校验结果处理
result = check(response, "data.product.id > 0", "data.product.name")
if not result:
    print("校验失败，请检查数据")

# 2. 异常处理
try:
    result = check(response, "data.invalid_field")
except Exception as e:
    print(f"数据结构异常: {e}")

# 3. 组合使用
try:
    result = check(response, 
                   "data.product.id > 0",
                   "data.product.name",
                   "data.product.price >= 0")
    if result:
        print("所有校验通过")
    else:
        print("存在校验失败")
except Exception as e:
    print(f"数据结构异常: {e}")
```


## 日志控制
不同日志级别的输出内容：
- **DEBUG**: 显示每个字段的详细校验过程，包括：
  - 待校验数据类型
  - 校验规则列表
  - 每个字段的具体值、类型、校验器和期望值
  - 校验成功/失败的详细原因
- **INFO**: 显示校验开始和完成的汇总信息，包括：
  - 校验任务开始信息（规则数量）
  - 校验完成结果（成功率统计）
- **WARNING**: 显示校验失败的字段，如"[2/5] ✗ 校验失败: data.product.id > 0"
- **ERROR**: 显示数据结构异常等严重错误，如"❌ 数据结构异常: 字段不存在"


## 性能优化建议
1. **批量校验**: 尽量在一次`check()`调用中完成多个校验
2. **通配符使用**: 使用`*.field`比循环调用更高效
3. **日志控制**: 通过`--log-level`参数控制日志输出级别
4. **合理分组**: 将相关的校验规则分组，便于维护


## 最佳实践
1. **优先使用字符串格式**: 比字典格式更简洁直观
2. **善用默认非空**: 大部分场景无需显式指定校验器
3. **通配符批量处理**: 列表数据优先使用通配符
4. **错误信息友好**: 使用有意义的字段路径名称
5. **分层校验**: 按数据层级组织校验规则


## 常见问题
### Q: 如何校验字段值为null？
```python
check(response, "data.field == null")
```

### Q: 如何校验数组长度？
```python
# 需要先获取数组，然后校验长度
# 或者使用通配符确保数组非空
check(response, "data.list.*.id")  # 确保数组有元素且每个元素的id非空
```

### Q: 如何校验复杂的正则表达式？
```python
check(response, "data.phone ~= '^1[3-9]\\d{9}$'")  # 手机号正则
check(response, "data.email ~= '^[\\w.-]+@[\\w.-]+\\.[a-zA-Z]{2,}$'")  # 邮箱正则
```

### Q: 条件校验如何使用？
```python
# 当status为active时，price必须大于0
check_when(data, "status == 'active'", "price > 0")

# 使用链式调用
checker(data).when("type == 'premium'", "features").validate()
```

### Q: 长度校验如何使用？
```python
# 基础长度校验
check(data, "name #>= 2")         # 姓名至少2个字符
check(data, "email #> 5")         # 邮箱长度大于5
check(data, "tags #<= 10")        # 标签数量不超过10个
check(data, "description #!= 0")  # 描述不能为空

# 组合长度校验
check(data, 
      "password #>= 8",           # 密码至少8位
      "password #<= 50")          # 密码不超过50位

# 表单验证示例
check(form_data,
      "username #>= 3",           # 用户名至少3个字符
      "username #<= 20",          # 用户名不超过20个字符
      "password #>= 8",           # 密码至少8位
      "confirm #= 9")            # 确认码正好9位
```

## 条件校验

### 功能概述
条件校验允许根据某个字段的值来决定是否校验另一个字段，支持所有校验器语法和通配符路径。

### 基本用法
```python
# 1. 使用check_when函数（推荐）
check_when(data, "status == 'active'", "price > 0")

# 2. 使用链式调用
checker(data)\
    .when("status == 'active'", "price > 0")\
    .validate()

# 3. 使用check函数 - 字典格式
conditional_rule = {
    'field': 'conditional',
    'validator': 'conditional_check',
    'expect': {
        'condition': "status == 'active'",
        'then': "price > 0"
    }
}
check(data, conditional_rule)
```

### 支持的条件校验语法
条件校验支持所有校验器语法，不再局限于等值校验：

```python
# 等值校验
check_when(data, "status == 'active'", "price > 0")

# 数值比较
check_when(data, "level >= 5", "features")

# 字符串匹配
check_when(data, "name ^= 'VIP'", "discount > 0")

# 类型校验
check_when(data, "quantity @= 'int'", "quantity > 0")

# 正则匹配
check_when(data, "env == 'production'", "log_level ~= '^(ERROR|WARN)$'")
```

### 通配符支持
条件校验完全支持通配符路径：

```python
# 当所有商品状态为active时，价格都必须大于0
check_when(data, "products.*.status == 'active'", "products.*.price > 0")

# 当商品类别为electronics时，价格必须>=50
check_when(data, "products.*.category == 'electronics'", "products.*.price >= 50")

# 嵌套条件校验
check_when(data, "order.items.*.discount_type == 'percentage'", "order.items.*.discount_value <= 100")
```

### 复杂场景示例
```python
# 订单数据
order_data = {
    "order": {
        "status": "confirmed",
        "payment_method": "credit_card",
        "items": [
            {"discount_type": "percentage", "discount_value": 10},
            {"discount_type": "fixed", "discount_value": 20}
        ]
    }
}

# 多个条件校验
checker(order_data)\
    .when("order.status == 'confirmed'", "order.total > 0")\
    .when("order.payment_method == 'credit_card'", "order.id")\
    .when("order.items.*.discount_type == 'percentage'", "order.items.*.discount_value <= 100")\
    .when("order.items.*.discount_type == 'fixed'", "order.items.*.discount_value > 0")\
    .validate()
```

### 条件校验逻辑
- **条件满足**: 执行then校验，返回then校验的结果
- **条件不满足**: 跳过校验，返回True（校验通过）
- **条件异常**: 如字段不存在等，校验失败返回False
- **then异常**: 如字段不存在等，校验失败返回False

### 与传统if-else的区别
```python
# 传统写法
if data.get("status") == "active":
    assert data.get("price", 0) > 0

# 条件校验写法
check_when(data, "status == 'active'", "price > 0")
```

条件校验的优势：
- 统一的错误处理和日志输出
- 支持通配符和复杂路径
- 与其他校验规则无缝集成
- 简洁的表达式语法

### Q: 如何校验字段的数据类型？
```python
check(response,
      "data.user_id @= 'int'",       # 校验是整数类型
      "data.username @= 'str'",      # 校验是字符串类型
      "data.is_active @= 'bool'",    # 校验是布尔类型
      "data.tags @= 'list'",         # 校验是列表类型
      "data.profile @= 'dict'")      # 校验是字典类型
```

### Q: 如何在一个校验中处理多种数据类型？
```python
check(response,
      "data.string_field",           # 字符串非空
      "data.string_field @= 'str'",  # 确认是字符串类型
      "data.number_field > 0",       # 数字大于0
      "data.number_field @= 'int'",  # 确认是整数类型
      "data.boolean_field == true",  # 布尔值为true
      "data.array_field.*.id")       # 数组元素非空
```

## 长度校验

### 功能概述
长度校验专门用于校验字符串、列表、字典等可测量长度的数据类型。使用 `#` 作为长度校验的前缀，设计简洁易记，减轻用户记忆负担。

### 支持的长度校验操作符
| 操作符 | 说明 | 示例 |
|--------|------|------|
| `#=` | 长度等于 | `"name #= 5"` |
| `#!=` | 长度不等于 | `"list #!= 0"` |
| `#>` | 长度大于 | `"content #> 10"` |
| `#>=` | 长度大于等于 | `"tags #>= 1"` |
| `#<` | 长度小于 | `"title #< 50"` |
| `#<=` | 长度小于等于 | `"items #<= 100"` |

### 基本用法
```python
# 基础长度校验
check(data, "name #>= 2")         # 姓名至少2个字符
check(data, "email #> 5")         # 邮箱长度大于5
check(data, "tags #<= 10")        # 标签数量不超过10个
check(data, "description #!= 0")  # 描述不能为空

# 组合长度校验
check(data, 
      "password #>= 8",           # 密码至少8位
      "password #<= 50")          # 密码不超过50位

# 表单验证示例
check(form_data,
      "username #>= 3",           # 用户名至少3个字符
      "username #<= 20",          # 用户名不超过20个字符
      "password #>= 8",           # 密码至少8位
      "confirm #= 9")            # 确认码正好9位
```

### 通配符长度校验
```python
# 所有商品名称都不为空
check(data, "products.*.name #> 0")

# 所有评论长度都在合理范围内
check(data, 
      "reviews.*.content #>= 10",    # 评论至少10个字符
      "reviews.*.content #<= 500")   # 评论不超过500个字符

# 所有标签列表都有内容
check(data, "articles.*.tags #>= 1")
```

### 链式调用中的长度校验
```python
# 表单验证
result = checker(form_data)\
    .length_greater_equal("username", 3)\
    .length_less_equal("username", 20)\
    .length_greater_equal("password", 8)\
    .length_less_equal("password", 50)\
    .length_equals("verification_code", 6)\
    .validate()

# 内容审核
result = checker(content_data)\
    .length_greater_than("title", 5)\
    .length_less_than("title", 100)\
    .length_greater_equal("content", 50)\
    .length_not_equals("tags", 0)\
    .validate()
```

### 与条件校验结合使用
```python
# 当文章类型为premium时，标题长度必须大于5
check_when(data, "article.type == 'premium'", "article.title #> 5")

# 当文章有标签时，标签数量必须在1-5之间
check_when(data, "article.tags #> 0", "article.tags #<= 5")

# 当文章内容长度大于20时，必须有标签
check_when(data, "article.content #> 20", "article.tags #> 0")
```

### 适用的数据类型
长度校验适用于所有有 `len()` 方法的数据类型：

```python
# 字符串长度
check(data, "title #<= 100")

# 列表长度
check(data, "items #>= 1")

# 字典长度（键数量）
check(data, "config #> 0")

# 元组长度
check(data, "coordinates #= 2")
```

### 使用场景示例

#### 1. 用户注册验证
```python
registration_data = {
    "username": "john_doe",
    "password": "secure123",
    "email": "john@example.com",
    "bio": "Software developer"
}

check(registration_data,
      "username #>= 3",        # 用户名至少3位
      "username #<= 20",       # 用户名不超过20位
      "password #>= 8",        # 密码至少8位
      "email #> 5",            # 邮箱有基本长度
      "bio #<= 200")           # 个人简介不超过200字
```

#### 2. 商品信息验证
```python
product_data = {
    "name": "智能手机",
    "description": "一款功能强大的智能手机",
    "tags": ["电子产品", "通讯设备"],
    "features": ["拍照", "游戏", "办公"]
}

check(product_data,
      "name #>= 2",            # 商品名至少2个字符
      "name #<= 50",           # 商品名不超过50个字符
      "description #>= 10",    # 描述至少10个字符
      "tags #>= 1",            # 至少有一个标签
      "tags #<= 10",           # 标签不超过10个
      "features #> 0")         # 至少有一个特性
```

#### 3. 内容管理验证
```python
# 批量验证文章列表
articles_data = {
    "articles": [
        {"title": "技术分享", "content": "这是一篇技术文章...", "tags": ["技术", "分享"]},
        {"title": "生活随笔", "content": "记录生活点滴...", "tags": ["生活"]}
    ]
}

check(articles_data,
      "articles.*.title #>= 3",      # 所有标题至少3个字符
      "articles.*.title #<= 100",    # 所有标题不超过100个字符
      "articles.*.content #>= 20",   # 所有内容至少20个字符
      "articles.*.tags #>= 1")       # 所有文章至少有一个标签
```

### 设计理念
1. **简洁易记**: 使用 `#` 符号作为长度校验前缀，直观表示数量/长度概念
2. **一致性**: 与现有比较操作符保持相同的逻辑和语法
3. **减轻记忆负担**: 无需记忆复杂的函数名或参数，操作符即见即懂
4. **完美融合**: 与现有的极简数据校验体系无缝集成

### 与传统方式对比
```python
# 传统方式（字典格式）
traditional_rule = {
    'field': 'text',
    'validator': 'length_gt',
    'expect': 5
}
check(data, traditional_rule)

# 新操作符（字符串格式）
check(data, "text #> 5")
```

新操作符的优势：
- 更简洁：`"text #> 5"` vs 复杂的字典结构
- 更直观：`#` 符号容易理解为长度/数量
- 减少记忆负担：与现有比较操作符保持一致
- 支持混合使用：可与其他校验器自由组合

这个新的数据校验方案大大简化了接口测试中的数据校验工作，让测试人员能够用最少的代码完成最全面的数据校验。 