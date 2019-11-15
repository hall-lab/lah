"""
Add haplotig headers to chromosomes
"""

from yoyo import step

__depends__ = {'20191114_01_aWDaU-chromosomes-table'}

steps = [
    step("ALTER TABLE chromosomes ADD haplotig_hdrs VARCHAR(64)", "ALTER TABLE chromosomes DROP haplotig_hdrs"),
]
