import json
from json import JSONDecodeError
from typing import Any

# def parse_string_list(raw_val: str) -> list[str]:
#     try:
#         retval = json.loads(raw_val)
#     except JSONDecodeError:  # as e:
#         retval = raw_val.split(',')
#
#     if not retval:
#         raise ValueError(raw_val)
#     return retval
#
#
# class ConfigBase:
#     @classmethod
#     def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
#         # print(f"cors: {raw_val}")
#         if field_name == 'BACKEND_CORS_ORIGINS':
#             retval = parse_string_list(raw_val)
#         else:
#             retval = cls.json_loads(raw_val)
#         return retval
