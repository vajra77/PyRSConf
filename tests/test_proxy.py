from pyrsconf import WhoisProxy


def test_proxy():
    routes = WhoisProxy.expand_as_and_macro(34428, 'AS-GLPR', 4)
    for r in routes:
        print(f"[{r.route}] with origin AS{r.origin} ({r.source})")

    assert len(routes) > 0
