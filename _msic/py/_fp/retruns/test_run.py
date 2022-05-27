from returns.result import Result, safe

@safe
def divide(first: float, second: float) -> float:
     return first / second
 
result = divide(1, 0)
result += 1
print('x / y = ', result)
 