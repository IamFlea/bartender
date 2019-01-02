from collections import defaultdict


class keydefaultdict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret


if __name__ == '__main__':
    d = keydefaultdict(list)
    result = d["Hire"]
    print(d)
    print(list("Hi"))
