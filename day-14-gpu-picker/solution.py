def parse_gpu_line(line: str) -> dict:
    ...


def pick_gpus(
    smi_output: str,
    count: int,
    *,
    min_free_mib: int = 0,
    max_util: int = 10,
) -> str:
    ...
