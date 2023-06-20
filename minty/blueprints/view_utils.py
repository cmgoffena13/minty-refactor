import cProfile
import functools
import os
import pstats


# Wrap any route after the decorator route to test.
def profile_view(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()

        if not os.path.exists("profile_logs"):
            os.mkdir("profile_logs")

        # Write profiling results to a file
        profile_filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "profile_logs",
            f"profile_{func.__name__}.log",
        )
        with open(profile_filename, "w") as f:
            stats = pstats.Stats(profiler, stream=f)
            stats.sort_stats("cumulative")
            stats.print_stats()

        return result

    return wrapper
