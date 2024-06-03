import psutil
import math
import time
import os
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


def bytes_to_gb(nof_bytes: int) -> float:
    """Convert bytes to GB."""
    return round(nof_bytes / math.pow(2, 30), 4)


def get_ram_usage() -> float:
    """Return the current RAM usage of the system in GB."""
    ram_info = psutil.virtual_memory()
    return bytes_to_gb(ram_info.used)


def get_total_ram() -> float:
    """Return the amount of RAM available on the system in GB."""
    return bytes_to_gb(psutil.virtual_memory().total)


def get_rss() -> float:
    """Return the amount of RAM used by the running script in GB."""
    process = psutil.Process(os.getpid())
    return bytes_to_gb(process.memory_info().rss)


def get_available_ram(safety_margin_percent: int = 10) -> float:
    """Return the amount of RAM available in GB."""
    safety_margin = 1 - (safety_margin_percent / 100)
    return round((get_total_ram() - get_ram_usage()) * safety_margin, 4)


def main() -> None:
    ram_usage = list()
    rss = list()
    timestamps = list()
    dummy_data = list()
    ram_usage_lim = get_total_ram() * 0.95
    start_time = time.perf_counter()
    ram_usage_start = get_ram_usage()
    ram_remaining = True
    ram_available = get_available_ram()
    print(ram_available)

    while ram_remaining:
        ram_usage.append(get_ram_usage())
        rss.append(get_rss())
        timestamps.append(time.perf_counter() - start_time)
        dummy_data.append([x for x in range(10000)])
        if rss[-1] >= ram_available:
            ram_remaining = False

    fig, ax = plt.subplots()
    assert isinstance(fig, Figure)
    assert isinstance(ax, Axes)
    fig: Figure
    ax: Axes

    plt.axhline(ram_usage_lim, label=f"RAM limit: {round(ram_usage_lim, 2)} (GB)", color="r", linestyle="dashed")
    ax.plot(timestamps, ram_usage, label="Total RAM usage (GB)", color="k")
    ax.plot(timestamps, rss, label="Process RAM usage (GB)", color="y")
    ax.plot(timestamps[rss.index(max(rss))], max(rss), "yo", label=f"Max process RAM usage: {max(rss)} GB")
    ax.plot(timestamps[ram_usage.index(max(ram_usage))], max(ram_usage), "ro", label=f"Max total RAM usage: {max(ram_usage)} GB")
    ax.plot(timestamps[0], ram_usage_start, "go", label=f"RAM usage at start: {ram_usage_start} GB")
    ax.grid()
    ax.set_title("Resource utilization: RAM")
    ax.set_ylabel("RAM usage (GB)")
    ax.set_xlabel("Runtime (s)")
    ax.legend()
    plt.show()


if __name__ == "__main__":
    main()
