from pyrsconf import Router


def import_neighbors(filename):
    neighbors = []
    return neighbors

def main():
    router = Router(address='193.201.28.60',
                    asn=24796
                    )
    for n in import_neighbors('../assets/neighbors.json')
        router.add_neighbor(n)

    


if __name__ == '__main__':
    main()
