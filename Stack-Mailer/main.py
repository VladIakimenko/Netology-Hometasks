from stack import Stack
from code_samples import SAMPLE_CORRECT, SAMPLE_INCORRECT


def check_balanced(sequence):
    """
    Checks if the sequence of brackets is balanced.
    Ignores all other chars.
    """
    pairs = ['()', '{}', '[]']
    stack = Stack()
    for el in sequence:
        if el in [pair[0] for pair in pairs]:
            stack.push(el)
        elif el in [pair[1] for pair in pairs]:
            if stack.is_empty() or \
                    stack.pop() + el not in pairs:
                return False
    return True


if __name__ == '__main__':

    # Пример сбалансированных последовательностей скобок:
    for line in (
            '(((([{}]))))',
            '[([])((([[[]]])))]{()}',
            '{{[()]}}'
    ):
        assert check_balanced(line)

    # Несбалансированные последовательности:
    for line in (
            '}{}',
            '{{[(])]}}',
            '[[{())}]'
    ):
        assert not check_balanced(line)

    # Последовательности с кодом:
    assert check_balanced(SAMPLE_CORRECT)
    assert not check_balanced(SAMPLE_INCORRECT)
