# Timezone

**introduction**

时区的设计灵感来自Django，但也有差异。tortoise中有两个配置项use_tz和timezone影响时区，可以在调用Tortoise.init时进行设置。在不同的数据库管理系统中，也存在不同的行为。

* use_tz  当设置use_tz = True时，无论设置什么时区，乌龟都会将UTC时间存储在数据库中。MySQL使用字段类型DATETIME（6），PostgreSQL使用TIMESTAMPTZ，SQLite在生成模式时使用TIMESTAMP。对于TimeField，MySQL使用TIME（6），PostgreSQL使用TIMETZ，SQLite使用TIME。
* timezone 当您从数据库中选择DateTimeField和TimeField时，无论您的数据库是哪个时区，都应该使用 tortoise.timezone.now() 获取时间，而不是本机时间 datetime.datetime.now()。

## 参考

### get_default_timezone()

`tortoise.timezone.get_default_timezone()`

将默认时区作为tzinfo实例返回。

这是tortoise配置定义的时区。

**Return type**  tzinfo

### get_timezone()

从tortoise配置中设置的env获取时区。

**Return type** str

### get_use_tz()

从tortoise配置中的env设置中获取use_tz。

**Return type**  bool

### is_aware(value)

确定是否知道给定的datetime.datetime或datetime.time。

该概念在Python的文档中定义：https://docs.python.org/library/datetime.html#datetime.tzinfo

假设value.tzinfo为None或适当的datetime.tzinfo，value.utcoffset()实现适当的逻辑。

**Return type**  bool

### is_naive(value)

### localtime(value=None,timezone=None)

将感知的datetime.datetime转换为当地时间。

只允许日期时间格式的值。当值被省略时，它默认为now()。

本地时间由当前时区定义，除非指定了其他时区。

### make_aware(value,timezone=None,is_dst=None)

### now()

返回一个时间
