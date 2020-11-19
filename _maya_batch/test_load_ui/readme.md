Maya 使用 Qt.py loadUi 会出现 c++ 对象被删除的情况

使用老方法 mayaShow 或是 mayaMixin 都无法解决
唯一的方法就是将 parent 传递到 \__init__ 函数下
然而 Maya2018 下也不奏效

