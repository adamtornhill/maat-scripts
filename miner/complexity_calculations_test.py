import unittest
import complexity_calculations
import language_preprocessors


class ComplexityCalculationsTest(unittest.TestCase):
    def test_cplusplus_code(self):
        file_contents = "        \n" \
                        "        return false;\n" \
                        "    }"
        # The first line is "no code" and thus, no complexity is calculated
        expected = [2.0, 1.0]

        preprocessor = language_preprocessors.create_for("somefile.cxx")
        actual = complexity_calculations.calculate_complexity_in(file_contents, preprocessor)

        self.assertEqual(actual, expected)

    def test_plain_ax_xpp_code(self):
        file_contents = "      SOURCE #functionName\n" \
                        "        #void functionName()\n" \
                        "        #{\n" \
                        "        #    return;\n" \
                        "        #}\n" \
                        "      ENDSOURCE\n"
        expected = [1.5, 2.0, 2.0, 3.0, 2.0, 1.5]

        preprocessor = language_preprocessors.create_for("somefile.xpo")
        actual = complexity_calculations.calculate_complexity_in(file_contents, preprocessor)

        self.assertEqual(actual, expected)

    def test_python_code_with_comments(self):
        file_contents = "class SomeClass(object):\n" \
                     "    def some_function(self):\n" \
                     "        # This is where we expect some fun\n" \
                     "        #    because python comments conflict with\n" \
                     "        #    X++ # characters at the beginning of\n" \
                     "        #    a line of code.\n" \
                     "        if something:\n" \
                     "            do_something()\n"
        expected = [0.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0]

        preprocessor = language_preprocessors.create_for("somefile.py")
        actual = complexity_calculations.calculate_complexity_in(file_contents, preprocessor)

        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
