import unittest
import loop

class TestLoop(unittest.TestCase):

    def test_dot_prod(self):

        list_1 = [1.0, 2.0]
        list_2 = [3.0, 4.0]
        expected = 11.0

        result = loop.dot_prod(list_1, list_2)

        self.assertEqual(result, expected)

    def test_matrix_vector_prod(self):

        list_1 = [[1.0, 2.0], [3.0, 4.0]]
        list_2 = [5.0, 6.0]
        expected = [17.0, 39.0]

        result = loop.matrix_vector_prod(list_1, list_2)

        self.assertEqual(result, expected)

    def test_pythagorean_triples(self):

        num = 10
        expected = [(3, 4, 5)]

        result = loop.pythagorean_triples(num)

        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main(exit=False)
