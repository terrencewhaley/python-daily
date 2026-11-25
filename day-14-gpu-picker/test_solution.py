import pytest

from solution import parse_gpu_line, pick_gpus

SMI = """
0, NVIDIA A100-SXM4-40GB, 38912 MiB, 40960 MiB, 97 %
1, NVIDIA A100-SXM4-40GB, 512 MiB, 40960 MiB, 0 %
2, NVIDIA A100-SXM4-40GB, 10240 MiB, 40960 MiB, 4 %
3, NVIDIA A100-SXM4-40GB, 0 MiB, 40960 MiB, 0 %
"""


def test_parse_sample_line():
    assert parse_gpu_line("  2, NVIDIA A100-SXM4-40GB, 10240 MiB, 40960 MiB, 4 %\n") == {
        "index": 2,
        "name": "NVIDIA A100-SXM4-40GB",
        "mem_used": 10240,
        "mem_total": 40960,
        "util": 4,
    }
    # space before the unit is optional
    assert parse_gpu_line("7,Tesla T4,100MiB,15360MiB,55%")["util"] == 55


@pytest.mark.parametrize(
    "line",
    [
        "",
        "0, NVIDIA A100, 512 MiB, 40960 MiB",  # 4 fields
        "0, NVIDIA A100, 512 MiB, 40960 MiB, 0 %, extra",  # 6 fields
        "0, , 512 MiB, 40960 MiB, 0 %",  # empty name
        "0, NVIDIA A100, 512 GiB, 40960 MiB, 0 %",  # wrong unit
        "0, NVIDIA A100, 512 MiB, 40960 MiB, 0",  # missing %
        "x, NVIDIA A100, 512 MiB, 40960 MiB, 0 %",  # bad index
        "0, NVIDIA A100, [N/A] MiB, 40960 MiB, 0 %",  # non-numeric memory
    ],
)
def test_parse_rejects_bad_lines(line):
    with pytest.raises(ValueError):
        parse_gpu_line(line)


def test_pick_sample():
    assert pick_gpus(SMI, 2) == "1,3"
    assert pick_gpus(SMI, 3, min_free_mib=20000) == "1,2,3"
    assert pick_gpus(SMI, 1) == "3"


def test_pick_ascending_and_tie_break():
    smi = (
        "3, A100, 0 MiB, 40960 MiB, 0 %\n"
        "1, A100, 0 MiB, 40960 MiB, 0 %\n"
        "2, A100, 0 MiB, 40960 MiB, 0 %\n"
        "0, A100, 100 MiB, 40960 MiB, 0 %\n"
    )
    # 1, 2, 3 tie on free memory; lower index wins, output is ascending
    assert pick_gpus(smi, 2) == "1,2"
    assert pick_gpus(smi, 4) == "0,1,2,3"


def test_pick_thresholds_and_errors():
    # max_util is inclusive; min_free_mib is inclusive
    assert pick_gpus(SMI, 3, max_util=97) == "1,2,3"
    assert pick_gpus(SMI, 4, max_util=97) == "0,1,2,3"
    assert pick_gpus(SMI, 1, min_free_mib=40960) == "3"
    with pytest.raises(RuntimeError):
        pick_gpus(SMI, 4)
    with pytest.raises(RuntimeError):
        pick_gpus(SMI, 3, min_free_mib=40000)
    with pytest.raises(ValueError):
        pick_gpus(SMI, 0)


def test_pick_skips_blank_lines_but_not_bad_ones():
    assert pick_gpus("\n\n  \n" + SMI + "\n\n", 1) == "3"
    with pytest.raises(RuntimeError):
        pick_gpus("", 1)
    with pytest.raises(ValueError):
        pick_gpus(SMI + "4, A100, ERR! MiB, 40960 MiB, 0 %\n", 1)
