from copy import deepcopy


class Stack:
    def __init__(self):
        self.stack = []

    def is_empty(self):
        return len(self.stack) == 0

    def push(self, element):
        self.stack.append(deepcopy(element))

    def pop(self):
        return self.stack.pop() if not self.is_empty() else None

    def peek(self):
        return self.stack[-1]

    def size(self):
        return len(self.stack)