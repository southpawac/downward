#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os

from lab.environments import LocalEnvironment, BaselSlurmEnvironment

import common_setup
from common_setup import IssueConfig, IssueExperiment
from relativescatter import RelativeScatterPlotReport

DIR = os.path.dirname(os.path.abspath(__file__))
BENCHMARKS_DIR = os.environ["DOWNWARD_BENCHMARKS"]
REVISIONS = ["issue781-v3", "issue781-v4-wss", "issue781-v4-varmark", "issue781-v4-opportunistic"]
CONFIGS = [
    IssueConfig(
        "{heuristic}-{pruning}".format(**locals()),
        ["--search", "astar({heuristic}(), pruning=stubborn_sets_{pruning}())".format(**locals())])
    for heuristic in ["blind", "lmcut"]
    for pruning in ["queue"]
]
SUITE = common_setup.DEFAULT_OPTIMAL_SUITE
ENVIRONMENT = BaselSlurmEnvironment(
    partition="infai_1",
    email="jendrik.seipp@unibas.ch",
    export=["PATH", "DOWNWARD_BENCHMARKS"])

if common_setup.is_test_run():
    SUITE = IssueExperiment.DEFAULT_TEST_SUITE
    ENVIRONMENT = LocalEnvironment(processes=1)

exp = IssueExperiment(
    revisions=REVISIONS,
    configs=CONFIGS,
    environment=ENVIRONMENT,
)
exp.add_suite(BENCHMARKS_DIR, SUITE)

exp.add_parser('lab_driver_parser', exp.LAB_DRIVER_PARSER)
exp.add_parser('exitcode_parser', exp.EXITCODE_PARSER)
#exp.add_parser('translator_parser', exp.TRANSLATOR_PARSER)
exp.add_parser('single_search_parser', exp.SINGLE_SEARCH_PARSER)
exp.add_parser('pruning_parser', os.path.join(common_setup.get_script_dir(), "parser.py"))

exp.add_absolute_report_step(
    attributes=IssueExperiment.DEFAULT_TABLE_ATTRIBUTES + ["time_for_pruning_operators"])
exp.add_report(common_setup.ComparativeReport([
        ("issue781-v3-{heuristic}-queue".format(**locals()),
         "issue781-v4-{extension}-{heuristic}-queue".format(**locals()))
        for heuristic in ["blind", "lmcut"]
        for extension in ["wss", "varmark", "opportunistic"]],
    attributes=IssueExperiment.DEFAULT_TABLE_ATTRIBUTES + ["time_for_pruning_operators"]))

exp.run_steps()
