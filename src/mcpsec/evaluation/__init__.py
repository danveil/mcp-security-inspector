"""Versioned corpus evaluation for deterministic detector research."""

from mcpsec.evaluation.comparison import compare_experiment_files, compare_experiments
from mcpsec.evaluation.evaluator import evaluate_corpus
from mcpsec.evaluation.integrity import compare_corpus_splits, corpus_sha256

__all__ = [
    "compare_corpus_splits",
    "compare_experiment_files",
    "compare_experiments",
    "corpus_sha256",
    "evaluate_corpus",
]
