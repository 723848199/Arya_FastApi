# Schema Creation

在这里，我们创建与SQLite数据库客户端的连接，然后我们发现和初始化模型。

```python
async classmethod Tortoise.generate_schemas(safe=True)
```

根据提供给.init()方法的模型生成模式。如果模式已经存在，则会失败，因此不建议将其用作应用程序工作流程的一部分

**Parameters:**

* safe=True 当设置为true时，仅当表不存在时才创建表

**Raises:**

* ConfigurationError 当.init()未被调用时返回此异常

**Return type:** None

Generate_schema在空数据库上生成模式。生成模式时还有默认选项，将safe设置为True，仅当表不存在时才会插入表。

## Helper Functions

```pytnon
async tortoise.utils.generate_schema_for_client(client,safe)
```

直接生成SQL模式并将其应用于给定的客户端。

**Parameters:**

* client 生成Schema SQL的DB客户端
* safe 当设置为true时，仅当表不存在时才创建表。

**Return type:**  None

```python
tortoise.utils.get_schema_sql(client,safe)
```

为给定客户端生成SQL模式。

**Parameters:**

* client 生成Schema SQL的DB客户端
* safe 当设置为true时，仅当表不存在时才创建表。

**Return type:**  str
