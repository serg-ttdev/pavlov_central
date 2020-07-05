import collections
from copy import deepcopy


def merge_dict(dict_src, dict_upd):
    result = deepcopy(dict_src)
    for key, value in dict_upd.items():
        src_sub_dict = result.get(key)
        if src_sub_dict is None:
            raise AttributeError('{} does not exist in src dict'.format(key))
        if isinstance(value, collections.Mapping):
            result[key] = merge_dict(src_sub_dict, value)
        else:
            result[key] = deepcopy(dict_upd[key])
    return result
