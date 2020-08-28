def outer_fun(a, b, *args, d="d", e="e", **kwargs):
    def inner():
        yield a
        yield b
        yield args
        yield d
        yield e
        yield kwargs

    return inner  # returns a function handle
