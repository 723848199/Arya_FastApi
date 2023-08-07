# Models

## 使用

要使用模型,首先需要导入他们

```python
from tortoise.models import Model
```

然后就可以描述你的模型了

```python
from tortoise.models import Model
from tortoise import fields


class Tournament(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    created = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Event(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    tournament = fields.ForeignKeyField('models.Tournament', related_name='events')
    participants = fields.ManyToManyField('models.Team', related_name='events', through='event_team')
    modified = fields.DatetimeField(auto_now=True)
    prize = fields.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return self.name


class Team(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()

    def __str__(self):
        return self.name
```

让我们看看我们做了什么

```python
class Tournament(Model):
```

每个模型都应该从基本模型导出。你也可以从你自己的模型子类中派生，你可以像这样创建抽象模型

```python
class AbstractTournament(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    created = fields.DatetimeField(auto_now_add=True)

    class Meta:
        # 定义抽象模型
        abstract = True

    def __str__(self):
        return self.name
```

抽象模型不会在模式生成中创建，也不会创建与其他模型的关系。

### 使用 \_\_models\_\_

如果你在你从中加载模型的模块中定义了变量`__models__`， `generate_schema`将使用该列表，而不是自动为你查找模型。

### 主键

在Tortoise ORM中，我们要求模型有一个主键。该主键将通过保留字段pk访问，该字段pk将是指定为主键的字段的别名。别名字段可以用作字段名进行过滤，例如。filter (pk=…)等…

> 可以使用任何类型作为主键,但只推荐下面四种类型
>
> * IntField
> * BigIntField
> * CharField
> * UUIDField

必须通过将pk参数设置为True来定义主键。如果您没有定义主键，我们将为您创建一个名称为`id`的`IntField`类型的主键。

> 如果在整数字段上使用此参数，则除非显式地传递`generate = False`，否则`generate`将被设置为`True`。

下面这些都是模型中有效的主键定义:

```python
id = fields.IntField(pk=True)

checksum = fields.CharField(pk=True)

guid = fields.UUIDField(pk=True)
```

### 继承

在Tortoise ORM中定义模型时，您可以通过利用继承来节省大量重复的工作。您可以在更泛型的类中定义字段，并且它们在派生类中自动可用。基类并不局限于模型类。任何课程都可以。这样，您就能够以一种自然且易于维护的方式定义您的模型。

让我们看一些例子。

```python
from tortoise import fields
from tortoise.models import Model

class TimestampMixin():
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)

class NameMixin():
    name = fields.CharField(40, unique=True)

class MyAbstractBaseModel(Model):
    id = fields.IntField(pk=True)

    class Meta:
        abstract = True

class UserModel(TimestampMixin, MyAbstractBaseModel):
    # Overriding the id definition
    # from MyAbstractBaseModel
    id = fields.UUIDField(pk=True)

    # Adding additional fields
    first_name = fields.CharField(20, null=True)

    class Meta:
        table = "user"


class RoleModel(TimestampMixin, NameMixin, MyAbstractBaseModel):

    class Meta:
        table = "role"
```

没有必要使用Meta类。但是给你的表一个明确的名字是个好习惯。这样，您就可以在不破坏模式的情况下更改模型名。所以下面的定义是有效的。

```python
class RoleModel(TimestampMixin, NameMixin, MyAbstractBaseModel):
    pass
```

### Meta 类

Meta类用于为模型配置元数据。

```python
class Foo(Model):
    ...

    class Meta:
        table="custom_table"
        unique_together=(("field_a", "field_b"), )
```

* abstract = False       设置为True表明这是一个抽象类
* schema = ''            设置它来配置一个模式名，其中table存在
* table = ''             设置此选项手动配置表名，而不是自动生成
* table_description = '' 将其设置为当前模型创建的表生成注释消息
* unique_together = None 为列集设置复合唯一索引。它应该是元组的元组(列表也可以)，格式为:

```python
  unique_together=("field_a", "field_b")
  unique_together=(("field_a", "field_b"), )
  unique_together=(("field_a", "field_b"), ("field_c", "field_d", "field_e"))
```

* indexes = None         列集设置复合非唯一索引。它应该是元组的元组(列表也可以)，格式为:

```python
  indexes=("field_a", "field_b")
  indexes=(("field_a", "field_b"), )
  indexes=(("field_a", "field_b"), ("field_c", "field_d", "field_e"))
```

* ordering = None        指定排序以设置给定模型的默认排序。它应该是可迭代的字符串格式与.order_by(…)接收的方式相同。如果查询是使用.annotate(…)使用GROUP_BY子句构建的，则不应用默认排序。

```python
ordering = ["name", "-score"]
```

* manager = tortoise.manager.Manager 指定manager以覆盖默认管理器

```python
manager = CustomManager()
```

### 一对多外键 ForeignKeyField

```python
tournament = fields.ForeignKeyField('models.Tournament', related_name='events')
participants = fields.ManyToManyField('models.Team', related_name='events')
modified = fields.DatetimeField(auto_now=True)
prize = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
```

在事件模型中，我们有更多的字段，这对我们来说可能很有趣。

```python
fields.ForeignKeyField('models.Tournament',related_name='events')`
```

这里我们为tournament创建外键引用。我们通过引用model来创建它，由app名和model名组成。models是默认的应用名，但你可以在Meta类中用app = 'other'修改它。

`related_name`

是关键字参数，它定义了参考模型上相关查询的字段，所以你可以像这样获取所有tournament的事件:

```python
await Tournament.first().prefetch_related("events")
```

#### DB_backing 字段

> ForeignKeyField是一个虚拟字段，这意味着它没有直接的DB支持。相反，它有一个字段(默认情况下称为FKNAME_id(也就是说，只是附加了一个_id)，这是实际的db支持字段。它将只包含相关表的Key值。这是一个重要的细节，因为它允许直接分配/读取实际值，如果不需要整个外部对象，这可以被认为是一种优化。
>
> (说人话,就是外键在数据库里只存储对应指向数据的id,不存储具体的数据)

指定FK可以通过传递对象来完成:

```python
await SomeModel.create(tournament=the_tournament)
# or
somemodel.tournament=the_tournament
```

或者直接访问 DB_backing 字段

```python
await SomeModel.create(tournament_id=the_tournament.pk)
# or
somemodel.tournament_id=the_tournament.pk
```

查询关系通常是通过附加双下划线，然后是外部对象的字段来完成的。然后可以追加一个普通的查询属性。如果下一个键也是一个外部对象，则可以链接:

`FKNAME\_\_FOREIGNFIELD\_\_gt=3`or `FKNAME\_\_FOREIGNFK\_\_VERYFOREIGNFIELD\_\_gt=3`

然而，有一个主要的限制。我们不想限制外部列名，或者有歧义(例如，外部对象可能有一个名为isnull的字段)。

那么这样会产生歧义:

`FKNAME__isnull`

为了防止这种情况，我们要求外键的db支持字段应用直接过滤器:

`FKNAME_id__isnull`

#### 获取外部对象

获取外键可以通过异步和同步接口来完成。

异步获取:

```python
events = await tournament.events.all()
```

也可以这样异步迭代:

```python
async for event in tournament.events:
    pass
```

同步使用需要你在时间之前调用fetch_related，然后你可以使用常见的函数，比如:

```python
await tournament.fetch_related('events')
events = list(tournament.events)
eventlen = len(tournament.events)
if SomeEvent in tournament.events:
    ...
if tournament.events:
    ...
firstevent = tournament.events[0]
```

要获得Reverse-FK，例如一个事件。tournament我们目前只支持同步接口。

```python
await event.fetch_related('tournament')
tournament = event.tournament
```

### 多对多外键 ManyToManyField

下一个字段是`fields。ManyToManyField('model.Team'， related_name= 'events')`它描述了与模型团队的多对多关系要添加到ManyToManyField，这两个模型都需要保存，否则将引发`OperationalError`错误。解析多对多字段可以通过异步和同步接口来完成。

异步获取:

```python
participants = await tournament.participants.all()
```

也可以迭代获取

```python
async for participant in tournament.participants:
    pass
```

同步使用需要你在时间之前调用fetch_related，然后你可以使用常见的函数，比如:

```python
await tournament.fetch_related('participants')
participants = list(tournament.participants)
participantlen = len(tournament.participants)
if SomeParticipant in tournament.participants:
    ...
if tournament.participants:
    ...
firstparticipant = tournament.participants[0]
```

#### 改进关系类型提示

由于Tortoise ORM仍然是一个年轻的项目，它没有得到各种编辑器的广泛支持，这些编辑器可以帮助您使用良好的模型自动补全功能和模型之间的不同关系来编写代码。但是，您可以通过自己做一点工作来获得这种自动完成功能。您所需要做的就是为负责关系的字段的模型添加一些注释。

下面是一个来自入门的更新示例，它将为所有模型添加自动完成，包括模型之间关系的字段。

```python
from tortoise.models import Model
from tortoise import fields


class Tournament(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)

    events: fields.ReverseRelation["Event"]

    def __str__(self):
        return self.name


class Event(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    tournament: fields.ForeignKeyRelation[Tournament] = fields.ForeignKeyField(
        "models.Tournament", related_name="events"
    )
    participants: fields.ManyToManyRelation["Team"] = fields.ManyToManyField(
        "models.Team", related_name="events", through="event_team"
    )

    def __str__(self):
        return self.name


class Team(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)

    events: fields.ManyToManyRelation[Event]

    def __str__(self):
        return self.name
```

## 参考

### class tortoise.models.Model(**kwargs)

所以模型的基类

#### class Meta

Meta类为模型配置元数据

```python
class Foo(Model):
    ...

    class Meta:
        table="custom_table"
        unique_together=(("field_a", "field_b"), )
```

#### classmethod all(using_db=None)

返回完整的QuerySet

**Return type:**

`QuerySet[typing_extension.Self]`

#### classmethod annotate(**kwargs)

用额外的函数/聚合/表达式注释结果集。

**Parameters:**

* **kwargs: 参数名称和要注释的函数/聚合。

**Return type:**

`QuerySet[typing_extensions.Self]`

#### classmethod bulk_create(...)

```python
classmethod bulk_create(
    objects, 
    batch_size=None, 
    ignore_conflicts=False, 
    update_fields=None, 
    on_conflict=None, 
    using_db=None)
```

大容量插入操作

> 大容量插入操作将尽可能确保在DB中创建的对象具有设置的所有默认值和生成的字段，但在Python中可能是不完整的引用。例如，IntField主键将不会被填充。

只有在您希望确保最佳插入性能的情况下，才建议使用这种方法。

```python
User.bulk_create([
    User(name="...", email="..."),
    User(name="...", email="...")
])
```

**Parameters:**

* on_conflict = None   冲突的索引名称
* update_fields = None 冲突时更新字段
* ignore_conflicts = False  插入时是否忽略冲突
* objects   要批量创建的对象列表
* batch_size = None 单个查询中创建多少个对象
* using_db = None 要使用的特定DB连接，而不是默认绑定的

**Return type:**

`BulkCreateQuery[Model]`

#### classmethod bulk_update(...)

```python
classmethod bulk_update(
    objects, 
    fields, 
    batch_size=None, 
    using_db=None)
```

更新数据库中每个给定对象中的给定字段。该方法通常通过一个查询有效地更新所提供模型实例上的给定字段。

```python
users = [
    await User.create(name="...", email="..."),
    await User.create(name="...", email="...")
]
users[0].name = 'name1'
users[1].name = 'name2'

await User.bulk_update(users, fields=['name'])
```

**Parameters:**

* objects   要批量创建的对象列表
* fields    要更新的字段
* batch_size = None 单个查询中创建多少个对象
* using_db = None 要使用的特定DB连接，而不是默认绑定的

**Return type:**

`BulkCreateQuery[Model]`

#### classmethod check()

调用各种检查来验证模型。

**Raises**

ConfigurationError 如果模型没有正确配置返回此错误

**Return type**

None

#### clone(pk=\<object object\>)

创建对象的新克隆。Save()将创建一条新记录。

**Parameters:**

* pk:Any  如果模型不生成自己的主键，则可选的必需值。您在这里指定的任何值都将始终被使用。

**Return type:**  Model

**Returns:**

没有主键信息的当前对象的副本。

**Raises:**

ParamsError  -如果需要pk主键，但没有提供。返回次错误

#### async classmethod create(using_db=None,**kwargs)

在DB数据库中创建一条记录并返回该对象。

```python
user = await User.create(name="...", email="...")
```

等价于

```python
user = User(name="...", email="...")
await user.save()
```

**Parameters:**

* using_db = None 要使用的特定DB连接，而不是默认绑定
* **kwargs  model参数

**Return type:**

Model

#### delete(using_db=None)

删除当前模型对象

**Parameters:**

* using_db = None 要使用的特定DB连接，而不是默认绑定

**Raises**

OperationalError 如果对象从未被持久化过抛出此异常

**Return type:** None

#### classmethod describe(serializable=True)

描述给定的模型列表或所有已注册的模型。

**Parameters:**

* serializable=True  如果你想要原始的python对象为False，如果你想要json序列化的数据为True。(默认为True)

**Return Tpye:**

dict

**Retuens:**

包含模型描述的字典。基本字典有一组固定的键，这些键引用一个字段列表(或者主键的情况下是单个字段):

```python
{
    "name":                 str     # Qualified model name
    "app":                  str     # 'App' namespace
    "table":                str     # DB table name
    "abstract":             bool    # Is the model Abstract?
    "description":          str     # Description of table (nullable)
    "docstring":            str     # Model docstring (nullable)
    "unique_together":      [...]   # List of List containing field names that
                                    #  are unique together
    "pk_field":             {...}   # Primary key field
    "data_fields":          [...]   # Data fields
    "fk_fields":            [...]   # Foreign Key fields FROM this model
    "backward_fk_fields":   [...]   # Foreign Key fields TO this model
    "o2o_fields":           [...]   # OneToOne fields FROM this model
    "backward_o2o_fields":  [...]   # OneToOne fields TO this model
    "m2m_fields":           [...]   # Many-to-Many fields
}
```

每个字段都按照`tortoise.fields.base.Field.describe()`描述

#### classmethod exclude(*args,**kwargs)

生成一个排除指定字段的QuerySet。

**Parameters:**

* *args Q个包含约束的函数。将是AND'ed。
* **kwargs  简单的过滤器约束。

**Return type:**

QuerySet[typing_extensions.Self]

#### classmethod exists(*args,using_db=None,**kwargs)

返回True/False是否存在提供的筛选参数的记录。

**Parameters:**

* using_db=None  指定使用的数据库
* *args Q个包含约束的函数。将是AND'ed。
* **kwargs  简单的过滤器约束

**Return type:**

ExistsQuery

#### async classmethod fetch_for_list(...)

```python
async classmethod fetch_for_list(
    instance_list,
    *args,
    using_db=None)
```

获取提供的Model对象列表的相关模型。

**Parameters:**

* instance_list  获取关系的Model对象列表。
* *args    要获取的关系名称
* using_db=None  DO NOT USE

**Return type:**

None

#### async fetch_related(*args,using_db=None)

获取相关字段

```python
User.fetch_related("emails", "manager")
```

**Parameters:**

* *args  应该提取的相关字段。
* using_db=None 要使用的特定DB连接，而不是默认绑定

**Return type:**

None

#### classmethod filter(*args,**kwargs)

生成应用筛选器的QuerySet。

**Parameters:**

* *args Q个包含约束的函数。将是AND'ed。
* **kwargs  简单的过滤器约束

**Return type:

QuerySet[typing_extensions.Self]

#### classmethod first(using_db=None)

生成返回第一条记录的QuerySet。

> filter查询到的是一个列表,指定主键,仅查询到一个值返回的也是一个列表,可以在后面跟上.first()取值

**Parameters:**

**Return type:**

QuerySetSingle[Optional[typing_extensions.Self]]

#### classmethod get(*args,using_db=None,**kwargs)

使用提供的过滤器参数为Model类型获取一条记录,找不到报错提示

**Parameters:**

* using_db=None 要使用的数据库
* *args Q个包含约束的函数。将是AND'ed。
* **kwargs  简单的过滤器约束

**Return type:

QuerySetSingle[typing_extensions.Self]

#### async classmethod get_or_create(defaults=None,using_db=None,**kwargs)

如果存在则获取对象(过滤提供的参数)，否则创建一个实例，其中任何未指定的参数作为默认值。

> 查不到就创建

**Parameters:**

* defaults=None  如果无法获取已创建的实例，则将默认值添加到该实例。
* using_db=None 要使用的特定DB连接，而不是默认绑定
* kwargs 查询参数

**Raises**

IntegrityError 如果创建失败

transactionManagementError 如果事物错误

Return type:

tuple[typing_extensions.Self,bool]

#### classmethod get_or_none(*args,using_db=None,**kwargs)

查不到就返回None

```python
user = await User.get_or_none(username="foo")
```

**Parameters:**

* using_db=None 需要使用的数据库
* *args Q个包含约束的函数。将是AND'ed。
* **kwargs  简单的过滤器约束

**Return type:**

QuerySetSingle[Optional[typing_extensions.Self]]

#### async classmethod in_bulk(id_list,field_name='pk',using_db=None)

返回一个字典，将每个给定的ID映射到具有该ID的对象。如果没有提供id_list，则计算整个QuerySet。

**Parameters:**

* id_list 字段值的列表
* ield_name='pk' 必须是唯一的字段
* using_db=None 要使用的特定DB连接，而不是默认绑定

**Return type:**

Dict[str,Model]

#### property pk:Any

**模型主键的别名。在进行过滤时可以用作字段名，例如。过滤器(pk=…)等等…**

**Return type**

Any

#### classmethod raw(sql,using_db=None)

执行raw sql 并返回结果

```python
result = await User.raw("select * from users where name like '%test%'")
```

**Parameters:**

* using_db=None 需要使用的数据库
* sql sql语句

**Return type:**

RawSqlQuery

#### async refresh_from_db(fields=None,using_db=None)

从db中刷新最新数据。当不带参数调用此方法时，模型的所有db字段都会更新为数据库中当前存在的值。

**Parameters:**

* fields = None 需要刷新的特殊字段。
* using_db=None 需要使用的数据库

**Raises**

* OperationalError  - 如果对象从未被持久化。

**Return type**

None

#### classmethod register_listener(singal,listener)

为特殊信号注册侦听器到当前模型类。

**Parameters:**

* signal  信号(不懂)
* listener  可调用的侦听器

**Raises**

ConfigurationError 侦听器不可调用时

#### async save(using_db=None,update_fields=None,force_create=Fale,force_update=False)

创建/更新当前模型对象。

**Parameters:**

* update_fields=None 如果提供，它应该是按名称的元组/字段列表。这是应该更新的字段子集。如果需要创建对象，update_fields将被忽略。
* using_db=None 要使用的特定DB连接，而不是默认绑定
* force_create=False 强制创建记录
* force_update=False 强制更新记录

**Raises:**

incompleteinstanceError —如果模型是局部的，并且字段不可用于持久化。

IntegrityError  -如果不能创建或更新模型(特别是如果已经设置了force_create或force_update)

**Return type:**

None

#### classmethod select_for_update(...)

```python
classmethod select_for_update(
    nowait=False,
    skip_locked=False,
    of=(),
    using_db=None)
```

使QuerySet选择更新。返回一个查询集，该查询集将锁定行，直到事务结束，生成一个SELECT…在支持的数据库上更新SQL语句

**Return type:**

QuerySet[typing_extensions.Self]

#### update_from_dict(data)

使用提供的字典更新当前模型。这允许从字典大量更新模型，同时确保数据类型转换的发生。这将忽略任何额外的字段，并且不会使用它们更新模型，但会在错误类型或更新多实例关系时引发错误。

**Parameters:**

data  要以字典格式更新的参数

**Return type**

Model

**Returns**

当前模型实例

**Raises:**

* ConfigurationError -当尝试更新远程实例时(例如反向外键或多对多关系)
* **ValueError** —当传递的参数类型不兼容时

#### async classmethod update_or_create(defaults=None,using_db=None,**kwargs)

一种方便的方法，用于使用给定的kwargs更新对象，并在必要时创建一个新对象。

**Parameters:**

* defaults=None 用于更新对象的默认值。
* using_db=None 要使用的特定DB连接，而不是默认绑定
* **kwargs 查询的参数

**Return type**

Tuple[Model,bool]
