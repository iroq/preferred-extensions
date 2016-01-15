import unittest
from preferred_extensions import Vertex, Graph

class TestVertexMethods(unittest.TestCase):

    def test_create_new(self):
        v = Vertex('a')
        self.assertEqual(v.name, 'a')

    def test_copy(self):
        v1 = Vertex('a')
        v1.attacks.append('b')
        v2 = v1.copy()
        self.assertFalse(id(v1.attacks) == id(v2.attacks))
        self.assertEqual(len(v1.attacks), len(v2.attacks))


class TestPreferredExtensions(unittest.TestCase):

    def test_one_node(self):
        g = Graph(['a'])
        pref = g.find_pref()
        self.assertEqual(pref['val'][0][0], set(['a']))


if __name__ == '__main__':
    unittest.main()