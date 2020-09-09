from experiments.closures import outer_fun


def test_outer_fun():
    a = "a"
    b = "b"
    c = "c"
    d = "d"
    e = "e"
    f = "f"

    outfn = outer_fun(a, b, c, f=f)
    out = outfn()

    test_a, test_b, test_c, test_d, test_e, test_f = out
    assert a == test_a
    assert b == test_b
    assert c == test_c[0]
    assert d == test_d
    assert e == test_e
    assert {"f": f} == test_f
