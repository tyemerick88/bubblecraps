from __future__ import annotations

from importlib import metadata
from typing import Literal, get_type_hints

from crapssim.rules import CraplessRules
from crapssim.table import TableSettings

EXPECTED_ENGINE_VERSION = "0.4.1"


def test_crapssim_is_exact_published_release() -> None:
    distribution = metadata.distribution("crapssim")

    assert distribution.version == EXPECTED_ENGINE_VERSION
    assert distribution.read_text("direct_url.json") is None, (
        "crapssim must be installed from the published package, not a local or VCS source"
    )


def test_crapless_rules_are_available_from_engine() -> None:
    rules = CraplessRules()

    assert rules.point_numbers() == [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]
    assert rules.come_out_winners() == [7]
    assert rules.come_out_losers() == []
    assert not rules.allow_dont_pass()
    assert not rules.allow_dont_come()


def test_table_settings_define_come_out_working_policy_options() -> None:
    annotations = get_type_hints(TableSettings)

    assert annotations["come_out_working_policy"] == Literal["legacy", "real_casino"]
