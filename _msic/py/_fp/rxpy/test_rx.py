from rx import Observable
from random import randint


three_emissions = Observable.range(1, 3)

(
    three_emissions.map(lambda i: randint(1, 100000))
    .subscribe(lambda i: print("Subscriber 1 Received: {0}".format(i)))
    .subscribe(lambda i: print("Subscriber 2 Received: {0}".format(i)))
)
