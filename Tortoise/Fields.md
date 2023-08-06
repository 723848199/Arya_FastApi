# Fields

## 使用

字段被定义为model类对象的属性

```python
from tortoise.models import Model
from tortoise import fields

class Tournament(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
```

## 参考

以下是这些字段的自定义选项可用的字段列表:

### 基本字段 Base Field

```python
class tortoise.fields.base.Field(
    source_field=None, 
    generated=False, 
    pk=False, 
    null=False, 
    default=None, 
    unique=False, 
    index=False, 
    description=None, 
    model=None, 
    validators=None, 
    **kwargs)
```

基本字段类型

**Parameters:**

* source_field=None   手动指定数据库对应的列名称
* generated=False     是否是数据库生成的字段
* pk=False            是否是主键
* null=False          是否允许为空
* default=None        设置默认值,可以为可调用对象
* unique=False        是否唯一
* index=False         是否自动建立索引
* description=None    字段描述。也会出现在tortoise . descripbe_model()中，并在生成的DDL中作为DB注释出现。
* validators=None     字段验证器

### Slass Attributers:

在定义实际字段类型时需要定义这些属性。

* field_type Type[Any]:  字段的类型。如果添加一个类型作为mixin， _FieldMeta会自动将this设置为that。
* indexable bool=True:   字段是否可索引?如果该字段不能可靠地索引，则设置为False。
* has_db_field bool=True: 这个字段有直接对应的DB列吗?或者该领域是虚拟化的?
* skip_to_python_if_native bool=False:如果DB驱动程序本身支持这种Python类型，我们是否应该跳过它?这只是为了优化目的，我们不需要在Python和DB之间强制进行类型转换。
* allows_generated bool = False: 这个字段能够被db生成吗?
* function_cast Optional[pypika.Term]=None: 在DB需要仿真帮助的情况下，我们需要应用一个强制转换术语。
* SQL_TYPE str:         SQL类型作为DB将使用的字符串。
* GENERATED_SQL str:    指示DB自动生成此字段的SQL。当allows_generated为True时必需。

#### Per-DB overrides:

可以指定每个数据库覆盖任何类属性，或者to_db_value或to_python_value方法。

为此，以class _db__SQL_DIALECT:的形式指定一个内部类，如下所示:

```python
class _db_sqlite:
    SQL_TYPE = "VARCHAR(40)"
    skip_to_python_if_native = False

    def function_cast(self, term: Term) -> Term:
        return functions.Cast(term, SqlTypes.NUMERIC)
```

然后，Tortoise将为该方言使用重写的属性/函数。如果需要动态属性，可以使用属性。

#### property constraints:dict

返回以Pydantic/JSONSchema格式定义的约束的字典。

**Return type:**  dict

```python
class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, index=True, unique=True, description='用户名')
    password = fields.CharField(max_length=100, index=True, description='密码')
User.username.constraints
```

#### describe(serializable)

描述字段

**Parameters**

* serializable   如果你想要原始的python对象为False，如果你想要json序列化的数据为True。(默认为True)

**Return type:**  dict

**Returns:**

包含字段描述的字典。(这假设serializable=True，这是默认值):

```python
{
    "name":         str     # 字段名称
    "field_type":   str     # 字段类型
    "db_column":    str     # 数据库对应列名称
                            #  可选: 仅适用 pk/data 字段
    "raw_field":    str     # 外键的原始字段名
                            #  可选: 仅适用外键
    "db_field_types": dict  # 默认和数据库覆盖的字段类型
    "python_type":  str     # Python type
    "generated":    bool    # 字段是否由数据库生成
    "nullable":     bool    # 字段是否允许为空
    "unique":       bool    # 字段是否唯一
    "indexed":      bool    # 字段是否被索引
    "default":      ...     # 默认值 (coerced to int/float/str/bool/null)
    "description":  str     # 字段描述 (nullable)
    "docstring":    str     # 字段文档 (nullable)
}
```

当serializable=False被指定时，一些字段不会被强制转换为有效的JSON类型。这些变化是:

```python
{
    "field_type":   Field   # 使用的字段类
    "python_type":  Type    # Python 类型
    "default":      ...     # 默认值为本机类型或可调用类型
}
```

#### get_db_field_types()

返回字段的数据库类型

**Return type:**  Optional[Dict[str,str]]

**Returns:** 以方言为键的字典。空白方言“”表示它是默认的DB字段类型。

#### get_for_dialect(dialect,key)

通过方言覆盖返回一个字段。

**Parameters:**

* dialect  使用的数据库方言
* key      属性/方法名

**return type:** Any

#### property required :bool

如果需要提供该字段，则返回True。它需要是非空的，并且没有默认值，也不需要由db生成。(字段是否必须传值,不能为空,没有默认值)

**Parameters:**

* value   model中的值
* instance  提供用于查找的模型类或模型实例。要确定这是否是一个可靠的实例，请执行: `if hasattr(instance, "_saved_in_db"):`

**Return type:** Any

#### to_python_value(value)

将DB类型转换为Python类型。

**Parameters:**

* value  db的值

**Return type:** Any

#### validate(value)

验证给定的值是否有效

**Parameters:**

* value 需要验证的值

**Raises:**

ValidationError  --当验证不通过时返回此错误

---

#### class tortoise.fields.base.Ondelete(value)

枚举类

`CASCADE = 'CASCADE'`

`NO_ACTION = 'NO ACTION'`

`RESTRICT = 'RESTRICT'`

`SET_DEFAULT = 'SET DEFAULT'`

`SET_NULL = 'SET NULL'`

#### class tortoise.fields.base.StrEnum(value)

pass

---

### 数据字段

#### BigIntField(pk=False,**kwargs)

大整数字段(64bit)

pk(bool) 是否为主键

**property constraints : dict**

返回以Pydantic/JSONSchema格式定义的约束的字典。

**Return type:** dict

**field_type**  int的别名

#### BinaryField(...)

```python
class tortoise.fields.data.BinaryField(
    source_field=None, 
    generated=False, 
    pk=False, 
    null=False, 
    default=None, 
    unique=False, 
    index=False, 
    description=None, 
    model=None, 
    validators=None, 
    **kwargs)
```

二进制字段。这用于存储字节对象。注意，不支持筛选或查询集更新操作。

**Field_type** bytes的别名

#### BooleanField(...)

```python
class tortoise.fields.data.BooleanField(
    source_field=None, 
    generated=False, 
    pk=False, 
    null=False, 
    default=None, 
    unique=False, 
    index=False, 
    description=None, 
    model=None, 
    validators=None, 
    **kwargs)
```

布尔类型字段

**field_type**  bool的别名

#### CharEnumField(...)

```python
tortoise.fields.data.CharEnumField(
    enum_type, 
    description=None, 
    max_length=0, 
    **kwargs)
```

Char Enum字段表示字符枚举的字段。

警告:如果max_length未指定或等于零，则自动检测所表示的char字段的大小。因此，如果稍后更新枚举，也需要更新表模式。

备注:可接受enum_type的合法str值。

**Parameters**

* enum_type 枚举类
* description 字段的描述。如果没有指定多行"name: value"对列表，则自动设置。
* max_legnth 创建的CharField的长度。如果为零，则自动从enum_type中检测到它。

**Returntype:** Enum

#### CharField(max_length,**kwargs)

字符串字段。

你必须提供以下参数:max_length (int):字段的最大长度，以字符为单位。

#### DateField(...)

```python
class tortoise.fields.data.DateField(
    source_field=None, 
    generated=False, 
    pk=False, 
    null=False, 
    default=None, 
    unique=False, 
    index=False, 
    description=None, 
    model=None, 
    validators=None, 
    **kwargs)
```

日期类型字段

#### datetimeField(...)

```python
class tortoise.fields.data.DatetimeField(
    auto_now=False, 
    auto_now_add=False, **kwargs)
```

日期时间字段。

Auto_now和auto_now_add是互斥的。您可以选择不设置或只设置其中一个。

auto_now(bool):总是在保存时设置为datetime.utknow()--当前时间。

auto_now_add(bool):仅在第一次保存时设置为datetime.utknow()--当前时间。

#### DecimalField(max_digits,decimal_places,**kwargs)

精确的十进制字段。

你必须提供以下参数:

max_digits (int):十进制字段的最大有效位数。

decimal_places (int):小数点后有多少位有效数字

#### FloatField(...)

浮点数类型

#### IntEnumField(enum_type,description=None,**kwargs)

枚举字段表示整数枚举的字段。

如果不指定多行"name: value"对列表，则自动设置该字段的描述。

备注:可以接受enum_type的int值。

enum_type:枚举类描述:字段的描述。如果没有指定多行"name: value"对列表，则自动设置。

#### IntField(pk=False,**kwags)

int类型字段(32bit)

#### JSONFIELD(...)

```python
class tortoise.fields.data.JSONField(
    encoder=<function <lambda>>, 
    decoder=<built-in function loads>, 
    **kwargs)
```

JSON字段。这个字段可以存储任何json兼容结构的字典或列表。您可以指定自己的自定义JSON编码器/解码器，保留默认值应该可以很好地工作。如果你安装了或json，我们默认使用否则将使用默认的json模块。

编码器:自定义JSON编码器。

译码器:自定义JSON解码器。

#### SmallIntField(pk=False,**kwargs)

小整数字段(16bit)

#### TextField(pk=False,unique=False,index=False,**kwargs)

大文本类型字段

#### TimeDelteField(...)

存储时间差的字段。

#### UUIDField(**kwargs)

UUID字段可以存储uuid值。如果用作主键，它将在默认情况下自动生成uuid4。

### 关系字段

#### ForeignKeyField(...)

```python
tortoise.fields.relational.ForeignKeyField(
    model_name: str, 
    related_name: str | None | False = None, 
    on_delete: OnDelete = CASCADE, 
    db_constraint: bool = True, 
    null: False = False, 
    **kwargs: Any) → ForeignKeyFieldInstance[MODEL]
```

ForeignKey关系字段。该字段表示与另一个模型的外键关系。

有关使用信息，请参阅外键。

你必须提供以下资料:

* model_name:相关模型的名称，格式为“app.model”。

以下选项可选:

* related_name:相关模型上用于反向解析外键的属性名。
* on_delete:
  * field.CASCADE:  如果相关模型被删除，则指示该模型应该被级联删除。
  * field.RESTRICT: 表明只要外键指向它，就限制相关的模型删除。
  * field.SET_NULL: 在相关模型被删除的情况下，将字段重置为NULL。只有当字段设置为null=True时才能设置。
  * field.SET_DEFAULT: 在相关模型被删除的情况下，将字段重置为默认值。只有当字段有默认设置时才能设置。
  * field.No_ACTION: 不要采取任何行动。
* to_field: 用于建立外键关系的相关模型上的属性名。如果未设置，则使用pk
* db_constraint:控制是否应该在数据库中为此外键创建约束。默认值是True，这几乎肯定是你想要的;将其设置为False可能对数据完整性非常不利。

#### ManyToManyField(...)

```python
tortoise.fields.relational.ManyToManyField(
    model_name, 
    through=None, 
    forward_key=None, 
    backward_key='', 
    related_name='', 
    on_delete=OnDelete.CASCADE, 
    db_constraint=True, 
    **kwargs)
```

多对多关系字段。

这个字段表示这个模型和另一个模型之间的多对多。

有关使用信息，请参见多对多。

你必须提供以下资料:

* model_name:相关模型的名称，格式为“app.model”。
  以下选项可选:通过:表示through表的DB表。默认值通常是安全的。
* forward_key:through表上的正向查找键。默认值通常是安全的。
* backward_key:through表上的向后查找键。默认值通常是安全的。
* related_name:对相关模型的属性名进行多对多的反向解析。
* db_constraint:控制是否应该在数据库中为此外键创建约束。默认值是True，这几乎肯定是你想要的;将其设置为False可能对数据完整性非常不利。
* on_delete:
  * field.CASCADE:  如果相关模型被删除，则指示该模型应该被级联删除。
  * field.RESTRICT: 表明只要外键指向它，就限制相关的模型删除。
  * field.SET_NULL: 在相关模型被删除的情况下，将字段重置为NULL。只有当字段设置为null=True时才能设置。
  * field.SET_DEFAULT: 在相关模型被删除的情况下，将字段重置为默认值。只有当字段有默认设置时才能设置。
  * field.No_ACTION: 不要采取任何行动。

#### OneToOneField(...)

```python
tortoise.fields.relational.OneToOneField(
    model_name: str, 
    related_name: str | None | False = None, 
    on_delete: OnDelete = CASCADE, 
    db_constraint: bool = True, 
    null: False = False, 
    **kwargs: Any) → OneToOneFieldInstance[MODEL]
```

一对一关系字段

### 数据库特有字段

#### MySQL

##### GeometryField(...)

```python
class tortoise.contrib.mysql.fields.GeometryField(
    source_field=None, 
    generated=False, 
    pk=False, 
    null=False, 
    default=None, 
    unique=False, 
    index=False, 
    description=None, 
    model=None, 
    validators=None, 
    **kwargs)
```

#### Postgres

##### TSVectorField(...)

```python
class tortoise.contrib.postgres.fields.TSVectorField(
    source_field=None, 
    generated=False, 
    pk=False, 
    null=False, 
    default=None, 
    unique=False, 
    index=False, 
    description=None, 
    model=None, 
    validators=None, 
    **kwargs)
```

### 扩展字段

只要能够以数据库兼容的格式表示，就可以对允许使用任意类型的字段进行子类化。这方面的一个例子是一个围绕CharField的简单包装器，用于存储和查询Enum类型。

```python
from enum import Enum
from typing import Type

from tortoise import ConfigurationError
from tortoise.fields import CharField


class EnumField(CharField):
    """
    An example extension to CharField that serializes Enums
    to and from a str representation in the DB.
    """

    def __init__(self, enum_type: Type[Enum], **kwargs):
        super().__init__(128, **kwargs)
        if not issubclass(enum_type, Enum):
            raise ConfigurationError("{} is not a subclass of Enum!".format(enum_type))
        self._enum_type = enum_type

    def to_db_value(self, value: Enum, instance) -> str:
        return value.value

    def to_python_value(self, value: str) -> Enum:
        try:
            return self._enum_type(value)
        except Exception:
            raise ValueError(
                "Database value {} does not exist on Enum {}.".format(value, self._enum_type)
            )
```

当子类化时，确保to_db_value返回与父类相同的类型(在CharField的情况下，这是一个str)，并且to_python_value在value形参(也是str)中自然接受相同的类型。
