from dependencies import Injector
from dependencies import operation



def view(user_word):
    points = calculate_points(user_word)
    return points


def calculate_points(word):
    guessed_letters_count = len([letter for letter in word if letter != "."])
    return Container._award_points_for_letters(guessed_letters_count)


class Container(Injector):
    threshold = 1
    view = view
    @operation
    def _award_points_for_letters(guessed,threshold=5):
        print(threshold)
        return 0 if guessed < threshold else guessed

res = view('asd')
print(res)

