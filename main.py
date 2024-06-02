import psutil
import math
import time
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


def bytes_to_gb(nof_bytes: int) -> float:
    return round(nof_bytes / math.pow(2, 30), 4)


def get_ram_usage() -> float:
    ram_info = psutil.virtual_memory()
    return bytes_to_gb(ram_info.used)


def get_total_ram() -> float:
    return bytes_to_gb(psutil.virtual_memory().total)


def main() -> None:
    ram_usage = list()
    timestamps = list()
    dummy_data = list()
    ram_usage_lim = get_total_ram() * 0.95
    start_time = time.perf_counter()

    for _ in range(1024):
        ram_usage.append(get_ram_usage())
        timestamps.append(time.perf_counter() - start_time)
        dummy_data.append([x for x in range(10000)])

    fig, ax = plt.subplots()
    assert isinstance(fig, Figure)
    assert isinstance(ax, Axes)
    fig: Figure
    ax: Axes

    plt.axhline(ram_usage_lim, label="RAM limit (GB)", color="r", linestyle="dashed")
    ax.plot(timestamps, ram_usage, label="RAM usage (GB)", color="k")
    ax.grid()
    ax.set_title("Resource utilization: RAM")
    ax.set_ylabel("RAM usage (GB)")
    ax.set_xlabel("Runtime (s)")
    ax.legend()
    plt.show()


if __name__ == "__main__":
    main()
