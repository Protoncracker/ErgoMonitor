from subprocess import run, DEVNULL
from time import perf_counter
from sys import argv

def run_script_and_measure_time(script_path):
    """
    Runs an external script and measures its execution time in milliseconds.

    :param script_path: Path to the script to be executed.
    :return: Execution time in milliseconds.
    """
    start_time = perf_counter()
    run(["python", script_path], stdout=DEVNULL, stderr=DEVNULL)
    end_time = perf_counter()
    elapsed_time_ms = (end_time - start_time) * 1000
    return elapsed_time_ms

def run_multiple_times(script_path, times=10):
    """
    Runs the given script multiple times and prints the execution time for each run.

    :param script_path: Path to the script to be executed.
    :param times: Number of times to run the script (default is 10).
    """
    for i in range(times):
        time_taken = run_script_and_measure_time(script_path)
        print(f"Run {i + 1}: {time_taken:.2f} ms")

if __name__ == "__main__":
    script_path = "path/to/your/script.py"  # Default script path
    times = 10  # Default number of times

    if len(argv) > 1:
        script_path = argv[1]
        if len(argv) > 2:
            try:
                times = int(argv[2])
            except ValueError:
                print("Invalid number for times, defaulting to 10.")

    run_multiple_times(script_path, times)
