from pydash import py_

value = 1


def on_true(*args):
    print("true")


def on_false(*args):
    value
    print("false")


py_().lte(2).tap(
    py_.cond(
        [
            (py_.stub_true, on_true),
            (py_.stub_false, on_false),
        ]
    )
)
