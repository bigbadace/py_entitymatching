from functools import partial
import os
from nose.tools import *
import unittest
import pandas as pd
import six

from magellan.utils.generic_helper import get_install_path
import magellan.catalog.catalog_manager as cm
from magellan.io.parsers import read_csv_metadata

import magellan.feature.simfunctions as sim

@nottest
def test_null_cases(sim_measure, input1, input2):
    val = sim_measure(input1, input2)
    assert_equal(pd.isnull(val), True)


def test_invalid_input_cases():
    sim_measures = {'jaccard':sim.jaccard, 'cosine':sim.cosine, 'monge_elkan':sim.monge_elkan,
                    'lev':sim.lev, 'jaro':sim.jaro, 'jaro_winkler':sim.jaro_winkler,
                    'need_wunch':sim.needleman_wunsch, 'smith_water':sim.smith_waterman,
                    'exact_match':sim.exact_match, 'rel_diff':sim.rel_diff, 'abs_norm':sim.abs_norm}
    inputs = {'None':None, 'pd.np.NaN':pd.np.NaN}


    for name, measure in six.iteritems(sim_measures):
        for label1, input1 in six.iteritems(inputs):
            for label2, input2 in six.iteritems(inputs):

                test_function = partial(test_null_cases, measure, input1, input2)
                test_function.description = 'Test ' + name + ' with inputs : ' + label1 + ', ' + label2
                yield test_function,

    for name, measure in six.iteritems(sim_measures):
        for label1, input1 in six.iteritems(inputs):
                label2='valid'
                input2 ='valid'
                test_function = partial(test_null_cases, measure, input1, input2)
                test_function.description = 'Test ' + name + ' with inputs : ' + label1 + ', ' + label2
                yield test_function,


    for name, measure in six.iteritems(sim_measures):
        for label2, input2 in six.iteritems(inputs):
                label1='valid'
                input1 ='valid'
                test_function = partial(test_null_cases, measure, input1, input2)
                test_function.description = 'Test ' + name + ' with inputs : ' + label1 + ', ' + label2
                yield test_function,

class SimFunctionsTestCases(unittest.TestCase):
    def test_get_global_sim_funs(self):
        x = sim._global_sim_fns

    def test_get_sim_funs_for_matching(self):
        x = sim.get_sim_funs_for_matching()
        l1 = list(x.keys())
        self.assertEqual(len(l1), len(sim.sim_fn_names))
        self.assertEqual(sorted(l1), sorted(sim.sim_fn_names))

    def test_get_sim_funs_for_blocking(self):
        x = sim.get_sim_funs_for_matching()
        l1 = list(x.keys())
        self.assertEqual(len(l1), len(sim.sim_fn_names))
        self.assertEqual(sorted(l1), sorted(sim.sim_fn_names))


    def test_sim_jaccard_valid_1(self):
        a = ['data']
        b = ['data', 'science']
        val = sim.jaccard(a, b)
        self.assertEqual(val, 0.5)


    def test_sim_jaccard_valid_2(self):
        a = 'data'
        b = ['data', 'science']
        val = sim.jaccard(a, b)
        self.assertEqual(val, 0.5)

    def test_sim_jaccard_valid_3(self):
        a = 'data'
        b = ['data', 'science']
        val = sim.jaccard(b, a)
        self.assertEqual(val, 0.5)


    #0.7071067811865475
    def test_sim_cosine_valid_1(self):
        a = ['data']
        b = ['data', 'science']
        val = sim.cosine(a, b)
        self.assertAlmostEqual(val, 0.7071067811865475)


    def test_sim_cosine_valid_2(self):
        a = 'data'
        b = ['data', 'science']
        val = sim.cosine(a, b)
        self.assertAlmostEqual(val, 0.7071067811865475)

    def test_sim_cosine_valid_3(self):
        a = 'data'
        b = ['data', 'science']
        val = sim.cosine(b, a)
        self.assertAlmostEqual(val, 0.7071067811865475)


    # >>> monge_elkan(['Niall'], ['Neal'])
    #     0.8049999999999999
    def test_sim_monelk_valid_1(self):
        a = ['Niall']
        b = ['Neal']
        val = sim.monge_elkan(a, b)
        self.assertAlmostEqual(val, 0.8049999999999999)


    def test_sim_monelk_valid_2(self):
        a = 'Niall'
        b = ['Neal']
        val = sim.monge_elkan(a, b)
        self.assertAlmostEqual(val, 0.8049999999999999)

    def test_sim_monelk_valid_3(self):
        a = ['Niall']
        b = 'Neal'
        val = sim.monge_elkan(a, b)
        self.assertAlmostEqual(val, 0.8049999999999999)

        # levenshtein('levenshtein', 'frankenstein')
        #        6
    def test_sim_lev_valid_1(self):
        a = 'levenshtein'
        b = 'frankenstein'
        val = sim.lev(a, b)
        self.assertEqual(val, 6)

    def test_sim_jaro_valid_1(self):
        #         >>> jaro('MARTHA', 'MARHTA')
        # 0.9444444444444445
        a = 'MARTHA'
        b = 'MARHTA'
        val = sim.jaro(a, b)
        self.assertAlmostEqual(val, 0.9444444444444445)


    def test_sim_jaro_winkler_valid_1(self):
        a = 'MARTHA'
        b = 'MARHTA'
        val = sim.jaro_winkler(a, b)
        self.assertAlmostEqual(val, 0.9611111111111111)

    def test_needleman_wunch_valid(self):
        self.assertEqual(sim.needleman_wunsch('dva', 'deeva'), 1.0)

    def test_smith_waterman_valid(self):
        self.assertEqual(sim.smith_waterman('cat', 'hat'), 2.0)

    def test_rel_diff_valid_1(self):
        a, b = float(10.0), float(11.0)
        v = abs(a-b)/(a+b)
        v = 1.0 - v
        self.assertEqual(sim.rel_diff(a, b), v)

    def test_rel_diff_valid_2(self):
        a, b = float(0.00001), float(0.00000012)
        v = abs(a-b)/(a+b)
        v = 1.0 - v
        self.assertEqual(sim.rel_diff(a, b), v)

    def test_rel_diff_valid_3(self):
        a, b = float(0.0), float(0.0)
        # v = abs(a-b)/(a+b)
        # v = 1.0 - v
        self.assertEqual(sim.rel_diff(a, b), 0)

    def test_rel_diff_valid_4(self):
        a, b = float(10.0), float(10.0)
        # v = abs(a-b)/(a+b)
        # v = 1.0 - v
        self.assertEqual(sim.rel_diff(a, b), 1.0)

    def test_abs_diff_valid_1(self):
        a, b = float(10.0), float(11.0)
        v = abs(a-b)/max(a, b)
        v = 1.0 - v
        self.assertEqual(sim.abs_norm(a, b), v)

    def test_abs_diff_valid_2(self):
        a, b = float(0.00001), float(0.00000012)
        v = abs(a-b)/max(a, b)
        v = 1.0 - v
        self.assertEqual(sim.abs_norm(a, b), v)

    def test_abs_diff_valid_3(self):
        a, b = float(0.0), float(0.0)
        # v = abs(a-b)/(a+b)
        # v = 1.0 - v
        self.assertEqual(sim.abs_norm(a, b), 0)

    def test_abs_diff_valid_4(self):
        a, b = float(10.0), float(10.0)
        # v = abs(a-b)/(a+b)
        # v = 1.0 - v
        self.assertEqual(sim.abs_norm(a, b), 1.0)