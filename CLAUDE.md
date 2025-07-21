# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

General-Validator 是一个极简通用数据批量校验器，专为接口测试中的数据校验场景设计。核心思想是通过极简的字符串表达式（如 `"field > 0"`）来完成复杂的数据校验任务。

## 核心架构

### 主要模块
- **src/general_validator/checker.py** - 核心校验引擎，包含所有校验逻辑
- **src/general_validator/logger.py** - 日志系统，支持彩色输出和级别控制
- **src/general_validator/__init__.py** - 版本信息和包导出

### 核心函数结构
```python
# 主要校验函数
check(data, *validations)           # 核心校验函数，支持多种格式
check_not_empty(data, *field_paths) # 专门非空校验
check_when(data, condition, *then)  # 条件校验
check_list(data_list, *field_names, **validators) # 列表批量校验
check_nested(data, list_path, nested_field, *field_validations) # 嵌套列表校验
checker(data)                       # 链式调用入口
```

### 校验器设计模式
1. **字符串表达式解析** - 通过 `_parse_string_rule()` 解析如 `"field > 0"` 的表达式
2. **通配符支持** - 使用 `*` 进行批量字段匹配，如 `"data.list.*.field"`
3. **操作符映射** - 将字符串操作符映射到内部校验函数
4. **链式调用** - 通过 `DataChecker` 类支持流式API

## 开发命令

### 依赖管理
```bash
# 安装依赖
make install
# 或者
poetry install
```

### 测试运行
```bash
# 运行测试
make test
# 或者
python -m unittest discover tests/
```

### 构建和发布
```bash
# 构建包
make build

# 发布 - 多种方式
make release                    # 交互式发布
make release VERSION=1.0.1     # 指定版本发布
make release-patch              # 补丁版本
make release-minor              # 次要版本
make release-major              # 主要版本
make release-test               # 发布到测试环境
```

### 版本管理
```bash
# 查看当前版本
make current-version

# 查看发布历史
make release-history

# 发布前检查
make pre-release-check
```

## 支持的校验操作符

### 比较操作符
- `==`, `!=`, `>`, `>=`, `<`, `<=` - 数值/字符串比较
- `^=` - 以...开头
- `$=` - 以...结尾
- `~=` - 正则匹配
- `*=` - 包含
- `=*` - 被包含

### 长度操作符
- `#=`, `#!=`, `#>`, `#>=`, `#<`, `#<=` - 长度校验

### 类型操作符
- `@=` - 类型匹配，支持 `int`, `float`, `str`, `bool`, `list`, `dict`, `none` 等

## 校验规则处理流程

1. **规则解析** - `_parse_and_validate()` 分发到字符串或字典解析
2. **字段路径解析** - `_get_values_by_path()` 处理通配符和嵌套路径
3. **校验器执行** - `_execute_validator()` 执行具体的校验逻辑
4. **结果汇总** - 返回布尔值，记录详细日志

## 常见使用模式

### 基础校验
```python
check(data, "field1", "field2 > 0", "field3 == 'value'")
```

### 列表批量校验
```python
check_list(data_list, "id", "name", "price > 0")
```

### 条件校验
```python
check_when(data, "status == 'active'", "price > 0", "name")
```

### 链式调用
```python
checker(data).not_empty("field1").greater_than("field2", 0).validate()
```

## 测试文件结构

测试文件位于 `tests/` 目录，包含多个演示和测试用例：
- `基础使用示例1.py`, `基础使用示例2.py` - 基本用法演示
- `条件校验示例.py` - 条件校验用法
- `列表批量校验示例.py` - 列表校验用法
- `链式调用测试.py` - 链式API用法
- `长度校验示例.py` - 长度校验用法

## 日志系统

日志系统支持四个级别：
- **DEBUG** - 详细的校验过程
- **INFO** - 校验开始和完成信息
- **WARNING** - 校验失败信息
- **ERROR** - 严重错误信息

通过 `setup_logger(log_level)` 控制日志级别。

## 扩展点

### 添加新的校验器
在 `_execute_validator()` 函数中添加新的 elif 分支，并在 `_parse_string_rule()` 中添加对应的操作符映射。

### 添加新的数据类型支持
在 `_check_type_match()` 函数中扩展 `type_mapping` 字典。

### 自定义校验逻辑
可以通过字典格式传入自定义的校验器名称和期望值。

## 注意事项

1. 校验失败时函数返回 `False`，数据结构异常时抛出 `Exception`
2. 通配符 `*` 用于批量字段匹配，支持列表和字典
3. 条件校验中，条件不满足时跳过校验（返回 `True`）
4. 链式调用必须以 `.validate()` 结束才执行校验
5. 日志级别会影响性能，生产环境建议使用 `INFO` 或更高级别