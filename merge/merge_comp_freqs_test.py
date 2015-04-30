import unittest
import merge_comp_freqs

class MergeCompFreqsTest(unittest.TestCase):
	FAKED_COMLEXITY_METRIC = 42
	FAKED_MODULE = 'some/file/here.py'
	FAKED_WINDOWS_MODULE = 'some\\file\\here.py'
	FAKED_FREQS_METRIC = 26

	def setUp(self):
		self._merger = merge_comp_freqs.Merged()
		self._simulate_existing(self.FAKED_MODULE, self.FAKED_COMLEXITY_METRIC)

	def test_starts_empty(self):
		m = merge_comp_freqs.Merged()
		self.assertEqual(m.sorted_result(), [])

	def test_parses_freqs_row(self):
		a_row = [self.FAKED_MODULE, self.FAKED_FREQS_METRIC]
		merge_comp_freqs.parse_freqs(self._merger, a_row)
		updated = self._merger.sorted_result()
		self.assertEqual(updated, [(self.FAKED_MODULE, (self.FAKED_FREQS_METRIC, self.FAKED_COMLEXITY_METRIC))])

	def test_parses_freqs_row_windows(self):
		a_row = [self.FAKED_WINDOWS_MODULE, self.FAKED_FREQS_METRIC]
		merge_comp_freqs.parse_freqs(self._merger, a_row)
		updated = self._merger.sorted_result()
		self.assertEqual(updated, [(self.FAKED_MODULE, (self.FAKED_FREQS_METRIC, self.FAKED_COMLEXITY_METRIC))])

	def test_parses_complexity_row(self):
		fake_module = 'other/file/there.py'
		fake_complexity_metric = 53
		fake_freq_metric = 34
		merger = merge_comp_freqs.Merged()
		a_row = ['Python', "./" + fake_module, 0, 1, fake_complexity_metric]
		merge_comp_freqs.parse_complexity(merger, a_row)
		b_row = [fake_module, fake_freq_metric]
		merge_comp_freqs.parse_freqs(merger, b_row)
		updated = merger.sorted_result()
		self.assertEqual(updated, [(fake_module, (fake_freq_metric, fake_complexity_metric))])

	def test_parses_complexity_row_windows(self):
		fake_module_windows = '.\\other\\file\\there.py'
		fake_module = 'other/file/there.py'
		fake_complexity_metric = 53
		fake_freq_metric = 34
		merger = merge_comp_freqs.Merged()
		a_row = ['Python', fake_module_windows, 0, 1, fake_complexity_metric]
		merge_comp_freqs.parse_complexity(merger, a_row)
		b_row = [fake_module, fake_freq_metric]
		merge_comp_freqs.parse_freqs(merger, b_row)
		updated = merger.sorted_result()
		self.assertEqual(updated, [(fake_module, (fake_freq_metric, fake_complexity_metric))])

	def test_ignores_non_existent_change_records(self):
		""" Since we're using historic data, some modules may no longer exist.
			In that case we're just ignore them in the merge.
		"""
		row_with_nonexistent = ['another/module', self.FAKED_FREQS_METRIC]
		merge_comp_freqs.parse_freqs(self._merger, row_with_nonexistent)
		updated = self._merger.sorted_result()
		empty_merge_result = []
		self.assertEqual(updated, empty_merge_result)

	def test_sorts_output_on_freqs(self):
		a_new_module = 'hello'
		complexity_of_new_module = 120
		freqs_of_new_module = 2
		self._simulate_existing(a_new_module, complexity_of_new_module)
		rows = [[self.FAKED_MODULE, self.FAKED_FREQS_METRIC], [a_new_module, freqs_of_new_module]]
		for a_row in rows:
			merge_comp_freqs.parse_freqs(self._merger, a_row)
		updated = self._merger.sorted_result()
		self.assertEqual(updated, [(self.FAKED_MODULE, (self.FAKED_FREQS_METRIC, self.FAKED_COMLEXITY_METRIC)),
									(a_new_module, (freqs_of_new_module, complexity_of_new_module))])

	def _simulate_existing(self, module, complexity):
		self._merger.record_detected(module, complexity)