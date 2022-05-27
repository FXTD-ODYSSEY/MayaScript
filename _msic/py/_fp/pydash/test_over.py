from pydash import py_

value = "hello"

res = py_.over_every(
    [
        py_.partial_right(isinstance, str),
        py_.partial_right(py_.is_equal, "hello"),
    ]
)(value)
print(res)
