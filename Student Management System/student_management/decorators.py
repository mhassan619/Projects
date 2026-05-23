import time
def timer(func):
    def wrapper(*args,**kwargs):
        start = time.time()
        result = func(*args,**kwargs)
        end = time.time()
        print(f"⏰ {func.__name__} takes {end - start:.4f} seconds to execute.")
        return result
    return wrapper
def logger(func):
    def wrapper(*args,**kwargs):
        print(f" {func.__name__} is called - args: {args}")
        result = func(*args,**kwargs)
        print(f"{func.__name__} completed - result: {result}")
        return result
    return wrapper