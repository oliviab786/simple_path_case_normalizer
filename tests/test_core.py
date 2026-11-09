import unittest

from simple_path_case_normalizer import normalize_path, find_duplicates


class NormalizePathTests(unittest.TestCase):
    def test_lowercases_ascii(self):
        self.assertEqual(normalize_path('/Home/User/File.TXT'), '/home/user/file.txt')

    def test_empty_string(self):
        self.assertEqual(normalize_path(''), '')

    def test_already_normalised(self):
        self.assertEqual(normalize_path('/a/b/c'), '/a/b/c')

    def test_preserves_separators_and_dots(self):
        # We deliberately do not resolve '..' or collapse slashes; the function
        # only changes case.
        self.assertEqual(normalize_path('A/../B//C'), 'a/../b//c')

    def test_non_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            normalize_path(b'/bytes')

    def test_unicode_case_folding(self):
        # German sharp s uppercases to 'SS' but lowercasing the uppercase form
        # gives 'ss'; the lowercase form is already 'ss'. Both normalise to the
        # same key, which is what we want for collision detection.
        self.assertEqual(normalize_path('STRASSE'), 'strasse')
        self.assertEqual(normalize_path('strasse'), 'strasse')


class FindDuplicatesTests(unittest.TestCase):
    def test_no_duplicates(self):
        self.assertEqual(find_duplicates(['/a/b', '/a/c', '/d/e']), [])

    def test_single_pair(self):
        self.assertEqual(
            find_duplicates(['/Home/User', '/home/user']),
            [('/Home/User', '/home/user')],
        )

    def test_three_way_collision_reports_against_first(self):
        self.assertEqual(
            find_duplicates(['/A/b', '/a/B', '/a/b']),
            [('/A/b', '/a/B'), ('/A/b', '/a/b')],
        )

    def test_exact_duplicate_is_also_a_collision(self):
        # An exact repeat is the degenerate case of a case collision and should
        # still be reported.
        self.assertEqual(
            find_duplicates(['/a/b', '/a/b']),
            [('/a/b', '/a/b')],
        )

    def test_empty_input(self):
        self.assertEqual(find_duplicates([]), [])

    def test_order_is_preserved(self):
        paths = ['/Z', '/z', '/Y', '/y']
        self.assertEqual(
            find_duplicates(paths),
            [('/Z', '/z'), ('/Y', '/y')],
        )

    def test_accepts_any_iterable(self):
        self.assertEqual(
            find_duplicates(iter(['/a', '/A'])),
            [('/a', '/A')],
        )


if __name__ == '__main__':
    unittest.main()
