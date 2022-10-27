
from pyrsconf import WhoisProxy


def test_proxy():
    proxy = WhoisProxy()
    routes = proxy.expand_as(24796)
    for r in routes:
        print(f"[{r.route}] with origin AS{r.origin} ({r.source})")

    assert len(routes) > 0