from collections import defaultdict
import math
import random
import unittest

import matplotlib.pyplot as plt

from funcs import (
    LinkedList, append_only, binary_search, linear_inserts, linked_list, native, quicksort
)

ORIGINAL_VALUES_LENGTH = 1_000_000
NEW_ARRAY_LENGTHS = [10, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]


class TestSortFuncs(unittest.TestCase):

    def test_funcs(self):
        for func_name, func in (
            ('simple', native), 
            ('inserts', linear_inserts), 
            ('create_new', append_only),
            ('quicksort', quicksort),
            ('binary-search', binary_search),
        ):
            with self.subTest(f'{func_name=}'):
                result, _ = func([1, 2, 3, 4], [0, 1, 3, 5, 5])
                self.assertListEqual(result, [0, 1, 1, 2, 3, 3, 4, 5, 5])

        # LinkedList gets its own code because the input is a different type
        with self.subTest(f'linked_list'):
            result, _ = linked_list(LinkedList.from_list([1, 2, 3, 4]), [0, 1, 3, 5, 5])
            self.assertListEqual(result.to_list(), [0, 1, 1, 2, 3, 3, 4, 5, 5])


class TestLinkedList(unittest.TestCase):

    def test_str(self):
        values = [2, 4, 5, 7, 7, 4, 3]
        ll = LinkedList.from_list(values)
        self.assertEqual(str(ll), '2 -> 4 -> 5 -> 7 -> 7 -> 4 -> 3')
        self.assertEqual(ll._len, 7)

    def test_from_list(self):
        values = [2, 5, 4]
        ll = LinkedList.from_list(values)
        self.assertEqual(ll.head.value, 2)
        self.assertEqual(ll.head.next.value, 5)
        self.assertEqual(ll.head.next.next.value, 4)

    def test_to_list(self):
        values = [2, 5, 4]
        ll = LinkedList.from_list(values)
        self.assertEqual(ll.head.value, 2)
        self.assertEqual(ll.head.next.value, 5)
        self.assertEqual(ll.head.next.next.value, 4)

        to_list = ll.to_list()
        self.assertListEqual(to_list, [2, 5, 4])


class TestPerformance(unittest.TestCase):
    
    @staticmethod
    def _get_random_list(n: int, seed: int=22):
        random.seed(seed)
        return [random.random() for _ in range(n)]

    def test_performance(self):
        results = defaultdict(list)
        for n in NEW_ARRAY_LENGTHS:
            for func_name, func in (
                ('native-sorted', native), 
                ('linear-inserts', linear_inserts), 
                ('append-only', append_only),
                # ('quicksort', quicksort),  # order of magnitude slower, skews charts
                ('binary-search-inserts', binary_search),
                ('linked-list', linked_list),
            ):
                original_values = self._get_random_list(ORIGINAL_VALUES_LENGTH, 13)
                new_values = self._get_random_list(n, 29)

                if func_name == 'linked-list':
                    # .from_list() runs before the function is called so is not part of its timing
                    _, time_taken = func(LinkedList.from_list(original_values), new_values)
                else:
                    _, time_taken = func(original_values, new_values)

                results[func_name].append((n, time_taken))

        # Plot all results together
        f = plt.figure()
        for method, values in results.items():
            x = [value[0] for value in values]
            y = [value[1] for value in values]
            plt.plot(x, y, label=method)
        plt.grid(True, linestyle='--')
        plt.legend()
        plt.title('Comparing performance of insertion methods')
        ymin, ymax = plt.ylim()
        plt.ylim([0, ymax])
        plt.ylabel('Average time taken (s)')
        plt.xlabel('# Inserted Elements')
        plt.savefig(f'./charts/all-methods.png')
        plt.close(f)

        # plot each method individually
        for method, values in results.items():
            f = plt.figure()
            x = [value[0] for value in values]
            y = [value[1] for value in values]
            plt.plot(x, y, label=method)
            plt.grid(True, linestyle='--')
            plt.title(method)
            ymin, ymax = plt.ylim()
            plt.ylim([0, ymax])
            plt.ylabel('Average time taken (s)')
            plt.xlabel('# Inserted Elements')
            plt.savefig(f'./charts/{method}.png')
            plt.close(f)


if __name__ == '__main__':
    unittest.main()
