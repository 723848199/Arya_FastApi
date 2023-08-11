# User = pydantic_model_creator(Users, )
#
#
# UserIn = pydantic_model_creator(Users, exclude_readonly=True, include=('UserStatus',))
# UserSchema = pydantic_model_creator(Users)
#
# class UserStatusSchema(pydantic_model_creator(UserStatus, include=('name',))):
#     name: str
#     pass
# class UserSchema(pydantic_model_creator(Users)):
#     status: UserStatusSchema = None
