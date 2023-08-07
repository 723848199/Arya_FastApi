# Indexes

tortoise默认使用BTree索引，当字段中定义index=True，或在Meta类中定义indexes.

如果你想使用其他索引类型，如Mysql的FullTextIndex,或Postgres的GinIndex,应该使用tortoise.indexes和它的子类。

## 用法

以下是使用MySQL的全文索引和空间索引的示例：

```python
from tortoise import Model, fields
from tortoise.contrib.mysql.fields import GeometryField
from tortoise.contrib.mysql.indexes import FullTextIndex, SpatialIndex


class Index(Model):
    full_text = fields.TextField()
    geometry = GeometryField()

    class Meta:
        indexes = [
            FullTextIndex(fields={"full_text"}, parser_name="ngram"),
            SpatialIndex(fields={"geometry"}),
        ]
```

> 一些内置索引可以在tortoise.contrib.mysql.indexes和tortoise.contrib.postgres.indexes中找到。

## 扩展索引

扩展索引很简单，你只需要继承tortoise.indexes.Index，以下是如何创建FullTextIndex的示例：

```python
from typing import Optional, Set
from pypika.terms import Term
from tortoise.indexes import Index

class FullTextIndex(Index):
    INDEX_TYPE = "FULLTEXT"

    def __init__(
        self,
        *expressions: Term,
        fields: Optional[Set[str]] = None,
        name: Optional[str] = None,
        parser_name: Optional[str] = None,
    ):
        super().__init__(*expressions, fields=fields, name=name)
        if parser_name:
            self.extra = f" WITH PARSER {parser_name}"
```

对于Postgres，您应该继承tortoise.contrib.postgres.indexes.PostgresIndex：

```python
class BloomIndex(PostgreSQLIndex):
    INDEX_TYPE = "BLOOM"
```
