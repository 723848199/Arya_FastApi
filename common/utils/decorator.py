def singleton(cls):
    """
    单例模式装饰器
    """
    instances = {}

    # @warps
    def __getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return __getinstance
