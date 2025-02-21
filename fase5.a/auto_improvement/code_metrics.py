def calculate_complexity(code: str) -> int:
    tree = ast.parse(code)
    return McCabeChecker(tree).complexity()

def measure_performance(code: str) -> dict:
    return {
        "time": timeit.timeit(lambda: exec(code, {}), number=1000),
        "memory": psutil.Process().memory_info().rss / 1024**2
    }