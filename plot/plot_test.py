import io
import unittest
from dataclasses import dataclass

import plot


class PlotterMock:
    def __init__(self):
        self.x = None
        self.y = None
        self.label = None

    def plot(self, x, y, label):
        self.x = x
        self.y = y
        self.label = label
        pass


@dataclass
class TestCase:
    column: int
    expected_y: list[float]
    expected_label: str

    def verify(self, t, actual_x, actual_y, actual_label):
        t.assertEqual(self.expected_y, actual_y, 'unexpected y coordinates')

        t.assertEqual(self.expected_label, actual_label, 'unexpected label')

        expected_x = range(1, len(self.expected_y) + 1)
        t.assertEqual(expected_x, actual_x, 'unexpected x coordinates')


class PlotTest(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.csv_data = "rev,n,total,mean,sd\n" \
                        "89272ea,1,10.0,20.1,30.0\n" \
                        "30b449a,2,11.0,20.2,30.0\n" \
                        "9caff67,3,12.0,20.3,30.0\n"

    def test_plot_file_plots_correct_column(self):
        cases = [
            TestCase(1, [1.0, 2.0, 3.0], "n"),
            TestCase(2, [10.0, 11.0, 12.0], "total"),
            TestCase(3, [20.1, 20.2, 20.3], "mean"),
            TestCase(4, [30.0, 30.0, 30.0], "sd")
        ]

        for case in cases:
            with self.subTest(column=case.column):
                input_file = io.StringIO(self.csv_data)
                plotter_mock = PlotterMock()

                plot.plot_file(input_file, case.column, plotter_mock)

                case.verify(self, plotter_mock.x, plotter_mock.y, plotter_mock.label)


if __name__ == '__main__':
    unittest.main()
