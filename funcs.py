import bisect
from datetime import datetime
from typing import Any, List, Tuple


# Note: in-place memory issue for LinkedList - tests will fail if REPEATS > 1
# Note also that quicksort is recursive, so REPEATS > 1 will exponentially affect its performance
REPEATS = 1


def time_me(repeats: int=1) -> Tuple[Any, float]:
    def outer(func):
        def inner(*args, **kwargs):
            dt0 = datetime.utcnow()
            for _ in range(repeats):
                result = func(*args, **kwargs)
            dt1 = datetime.utcnow()
            return result, (dt1 - dt0).total_seconds() / repeats
        return inner
    return outer


@time_me(REPEATS)
def native(original_values: List[float], new_values: List[float]) -> List[float]:
    new_list = [*original_values]
    new_list.extend(new_values)
    return sorted(new_list)


@time_me(REPEATS)
def binary_search(original_values: List[float], new_values: List[float]) -> List[float]:
    new_list = [*original_values]
    for value in new_values:
        position = bisect.bisect_left(new_list, value)
        new_list.insert(position, value)
    return new_list


@time_me(REPEATS)
def quicksort(values: List[float], new_values: List[float]=None) -> List[float]:
    # quicksort algorithm taken from: https://stackoverflow.com/questions/18262306/quicksort-with-python
    if new_values is not None:
        values.extend(new_values)

    less, equal, greater = [], [], []
    if len(values) > 1:
        pivot = values[len(values) // 2]
        for value in values:
            if value < pivot:
                less.append(value)
            elif value == pivot:
                equal.append(value)
            elif value > pivot:
                greater.append(value)

        # because of decorator, actual result is first output (second is time taken)
        return quicksort(less)[0] + equal + quicksort(greater)[0]
    else:
        return values


@time_me(REPEATS)
def append_only(original_values: List[float], new_values: List[float]) -> List[float]:
    new_values = sorted(new_values)
    new_list = []

    len_original = len(original_values)
    len_new = len(new_values)
    
    i, j = 0, 0
    while i < len_original and j < len_new:
        if original_values[i] <= new_values[j]:
            new_list.append(original_values[i])
            i += 1
        else:
            new_list.append(new_values[j])
            j += 1
    
    # Append any remaining elements from either lists
    # note: only one of the below conditions can be True
    if i < len_original:
        new_list.extend(original_values[i:])
    elif j < len_new:
        new_list.extend(new_values[j:])

    return new_list


@time_me(REPEATS)
def linear_inserts(original_values: List[float], new_values: List[float]) -> List[float]:
    new_list = [*original_values]
    new_values = sorted(new_values)

    len_original = len(original_values)
    len_new = len(new_values)

    i, j = 0, 0
    while i < len_original + j and j < len_new:
        if new_values[j] <= new_list[i]:
            new_list.insert(i, new_values[j])
            j += 1
        else:
            i += 1
    
    if j < len_new:
        new_list.extend(new_values[j:])

    return new_list


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class LinkedList:
    def __init__(self, head: Node=None):
        self.head = head
        self._len = 1
    
    @classmethod
    def from_list(cls, values: list):
        if len(values) <= 1:
            raise Exception('Not enough values')

        node = Node(values[0])
        ll = cls(head=node)
        for value in values[1:]:
            new_node = Node(value)
            node.next = new_node
            ll._len += 1

            node = new_node
        return ll
    
    def to_list(self):
        output = []
        node = self.head
        while node.next is not None:
            output.append(node.value)
            node = node.next
        output.append(node.value)
        return output
    
    def __str__(self):
        output = ''
        node = self.head
        while node.next is not None:
            output += str(node.value) + ' -> '
            node = node.next
        output += str(node.value)
        return output
    
    def deep_copy(self):
        values_list = self.to_list()
        return self.from_list(values_list)


# there is an in-place memory problem with this code - if REPEATS is > 1, we get duplicated inserts
# running a deep-copy of the input variable decimates its performance. So keep this as 
# single, non-repeating
@time_me(REPEATS)
def linked_list(original_values: LinkedList, new_values: List[float]) -> LinkedList:
    ll = original_values
    new_values = sorted(new_values)

    len_new = len(new_values)

    node = ll.head
    prev_node = None
    i = 0
    while node.next is not None and i < len_new:
        if node.value >= new_values[i]:
            new_node = Node(new_values[i], next=node)
            if i == 0:
                ll.head = new_node
            else:
                prev_node.next = new_node
            i += 1

        prev_node = node
        node = node.next

    # any values left over to tag onto the end?
    if i < len(new_values):
        for value in new_values[i:]:
            node.next = Node(value)
            node = node.next

    return ll
