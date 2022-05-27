from toolz import compose
from toolz.curried import do
from toolz.dicttoolz import merge


def merge_dict(d1, d2):
    """Merge dict.
    https://stackoverflow.com/a/29847323/13452951

    Args:
        d1 (dict): Source Dict
        d2 (dict): Merge Dict
    """
    d1 = d1 if d1 else {}
    d2 = d2 if d2 else {}
    for k in d2:
        if k in d1 and isinstance(d1[k], dict) and isinstance(d2[k], dict):
            merge_dict(d1[k], d2[k])
        else:
            d1[k] = d2[k]


a = {
    "module_name": {
        "type": "string",
    }
}
b = {
    "module_name": {
        "type": "string",
        "coerce": str,
    },
    "file_path": {"type": "string", "check_with": "is_path_exists"},
}
res = merge(a, b)
print(res)

a = {
    "module_name": {
        "type": "string",
    }
}
b = {
    "module_name": {
        "type": "string",
        "coerce": str,
    },
    "file_path": {"type": "string", "check_with": "is_path_exists"},
}
merge_dict(a, b)
print(a)
