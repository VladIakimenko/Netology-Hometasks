import types


class FlatIterator:
    def __init__(self, list_of_list):
        self.lol = list_of_list

    def __iter__(self):
        self.row = 0
        self.seat = 0
        return self

    def __next__(self):
        row_incremented = False
        while True:
            try:
                item = self.lol[self.row][self.seat]
                self.seat += 1
                break
            except IndexError:
                if row_incremented:
                    raise StopIteration
                self.row += 1
                self.seat = 0
                row_incremented = True
        return item


def test_1():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


def flat_generator(list_of_lists):
    row = 0
    seat = 0
    while True:
        try:
            yield list_of_lists[row][seat]
            if list_of_lists[row][seat] == list_of_lists[-1][-1]:
                break
            seat += 1
        except IndexError:
            row += 1
            seat = 0


def test_2():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_generator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_generator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)


class FlatIteratorMultiDepth:
    """
    An iterator that flattens a nested list with any level of depth.
    """
    def __init__(self, list_of_lists):
        self.lol = list_of_lists

    def __iter__(self):
        self.tail = self.lol.copy()
        return self

    def __next__(self):
        element = self.tail.pop(0)

        while True:
            if type(element) == list:
                if len(element) > 1:
                    element, remnant = element[0], element[1:]
                    self.tail.insert(0, remnant)
                elif len(element) == 1:
                    element = element[0]
                else:
                    break
            else:
                return element

        if not len(self.tail):
            raise StopIteration

    # def __init__(self, list_of_lists):       # THIS BLOCK PASSES BOTH TESTS BUT SEEMS TO LOSE THE IDEA OF USING AN ITERATOR,
    #     self.result = list_of_lists          # SINCE ALL CALCULATIONS ARE MADE AT ONCE WHEN THE __ITER__ METHOD IS CALLED
    #
    # def __iter__(self):
    #     while any([type(el) == list for el in self.result]):
    #         result = []
    #         for sublist in self.result:
    #             if type(sublist) == list:
    #                 for el in sublist:
    #                     result.append(el)
    #             else:
    #                 result.append(sublist)
    #         self.result = result
    #     self.counter = 0
    #     return self
    #
    # def __next__(self):
    #     if self.counter == len(self.result):
    #         raise StopIteration
    #     else:
    #         item = self.result[self.counter]
    #         self.counter += 1
    #         return item


def test_3():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIteratorMultiDepth(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIteratorMultiDepth(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']


def flat_generator_multi_depth(list_of_lists):
    """
    A generator that flattens a nested list with any level of depth.
    """
    lol = list_of_lists.copy()
    while len(lol):
        element = lol.pop(0)
        while True:
            if type(element) == list:
                if len(element) > 1:
                    element, remnant = element[0], element[1:]
                    lol.insert(0, remnant)
                elif len(element) == 1:
                    element = element[0]
                else:
                    break
            else:
                yield element
                break


def test_4():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for generator_item, check_item in zip(
            flat_generator_multi_depth(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert generator_item == check_item

    assert list(flat_generator_multi_depth(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    assert isinstance(flat_generator_multi_depth(list_of_lists_2), types.GeneratorType)


if __name__ == '__main__':
    test_1()
    test_2()
    test_3()
    test_4()
