
import cloudpickle

squared = lambda x: x ** 2
pickled_lambda = cloudpickle.dumps(squared)

print(pickled_lambda)

