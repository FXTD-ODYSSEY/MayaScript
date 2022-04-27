from typing import Type, TypeVar, ClassVar
T = TypeVar('T')

class M(type):
    count: ClassVar[int] = 0

    def make(cls: Type[T]) -> T:
        M.count += 1
        return cls()

class A(metaclass=M):
    pass

a = A.make()  # make() is looked up at M; the result is an object of type A
print(A.count)

class B(A):
    pass

b: B = B.make()  # metaclasses are inherited
# print(B.count + " objects were created")  # Error: Unsupported operand types for + ("int" and "str")