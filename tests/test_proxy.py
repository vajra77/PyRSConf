from pyrsconf import WhoisProxy


def test_proxy():
    routes = WhoisProxy.bulk_expand(34428, 'AS-GLPR', 4)
    for r in routes:
        print(f"[{r.route}] with origin AS{r.origin} ({r.source})")

    assert len(routes) > 0
