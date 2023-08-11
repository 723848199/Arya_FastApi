## 实现功能

### 用户

注册,登录认证,查看信息

### 项目结构

* `app`  --项目源目录
    * `user` --用户模块
        * `api` --api接口
        * `auth.py` --认证相关
        * `models.py` --子模块模型
        * `routers` --子模块路由
        * `schemas.py` --子模块序列化模型
    * `...目录` --其他模块
    * `models.py` --公共模型
    * `routers.py` --总路由管理
    * `schemas.py` --总序列化模型
* `common` --公共函数目录
* `test` --单元测试目录
* `main.py` --项目入口
* `setting.py` --项目配置文件
* `.env` --环境变量(本地文件,不上传代码仓)
* `.gitginre` --git管理排除文件