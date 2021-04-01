import random
from unittest import TestCase

################################################################################
# EXTENSIBLE xASxTABLE
################################################################################
class ExtensiblexasxTable:

    def __init__(self, n_buckets=1000, fillfactor=0.5):
        self.n_buckets = n_buckets
        self.fillfactor = fillfactor
        self.buckets = [None] * n_buckets
        self.nitems = 0

    def find_bucket(self, key):
        # BEGIN_SOLUTION
        x = hash(key) % self.n_buckets

        if self.buckets[x] and self.buckets[x][0] == key:
            return self.buckets[x]
        
        for x in range(self.n_buckets):
            if self.buckets[x] and self.buckets[x][0] == key:
                return self.buckets[x]
        # END_SOLUTION

    def __getitem__(self,  key):
        # BEGIN_SOLUTION
        x = hash(key) % self.n_buckets

        if self.buckets[x] and self.buckets[x][0] == key:
            return self.buckets[x][1]

        for x in range(self.n_buckets):
            if self.buckets[x] and self.buckets[x][0] == key:
                return self.buckets[x][1]
        raise KeyError
        # END_SOLUTION

    def __setitem__(self, key, value):
        # BEGIN_SOLUTION
        x = hash(key) % self.n_buckets

        while self.buckets[x] and self.buckets[x][0] != key:
            x += 1
            if x == self.n_buckets:
                x = 0
        self.buckets[x] = [key, value]
        self.nitems += 1

        if (self.nitems / self.n_buckets) >= self.fillfactor:
            self.n_buckets *= 2
            temp = self.buckets
            self.buckets = [None] * self.n_buckets
            self.nitems = 0
            for b in temp:
                if b:
                    self[b[0]] = b[1]
        # END_SOLUTION

    def __delitem__(self, key):
        # BEGIN SOLUTION
        x = hash(key) % self.n_buckets

        if self.buckets[x] == key:
            self.buckets[x] = None
            self.nitems -= 1
        else:
            for x in range(self.n_buckets):
                if self.buckets[x] and self.buckets[x][0] == key:
                    self.buckets[x] = None
                    self.nitems -= 1
                    break
        # END SOLUTION

    def __contains__(self, key):
        try:
            _ = self[key]
            return True
        except:
            return False

    def __len__(self):
        return self.nitems

    def __bool__(self):
        return self.__len__() != 0

    def __iter__(self):
        ### BEGIN SOLUTION
        for x in range(self.n_buckets):
            if self.buckets[x]:
                yield self.buckets[x][0]
        ### END SOLUTION

    def keys(self):
        return iter(self)

    def values(self):
        ### BEGIN SOLUTION
        for x in range(self.n_buckets):
            if self.buckets[x]:
                yield self.buckets[x][1]
        ### END SOLUTION

    def items(self):
        ### BEGIN SOLUTION
        for x in range(self.n_buckets):
            if self.buckets[x]:
                yield tuple(self.buckets[x])
        ### END SOLUTION

    def __str__(self):
        return '{ ' + ', '.join(str(k) + ': ' + str(v) for k, v in self.items()) + ' }'

    def __repr__(self):
        return str(self)

################################################################################
# TEST CASES
################################################################################
# points: 20
def test_insert():
    tc = TestCase()
    x = ExtensiblexasxTable(n_buckets=100000)

    for i in range(1,10000):
        x[i] = i
        tc.assertEqual(x[i], i)
        tc.assertEqual(len(x), i)

    random.seed(1234)
    for i in range(1000):
        k = random.randint(0,1000000)
        x[k] = k
        tc.assertEqual(x[k], k)

    for i in range(1000):
        k = random.randint(0,1000000)
        x[k] = "testing"
        tc.assertEqual(x[k], "testing")

# points: 10
def test_getitem():
    tc = TestCase()
    x = ExtensiblexasxTable()

    for i in range(0,100):
        x[i] = i * 2

    with tc.assertRaises(KeyError):
        x[200]


# points: 10
def test_iteration():
    tc = TestCase()
    x = ExtensiblexasxTable(n_buckets=100)
    entries = [ (random.randint(0,10000), i) for i in range(100) ]
    keys = [ k for k, v in entries ]
    values = [ v for k, v in entries ]

    for k, v in entries:
        x[k] = v

    for k, v in entries:
        tc.assertEqual(x[k], v)

    tc.assertEqual(set(keys), set(x.keys()))
    tc.assertEqual(set(values), set(x.values()))
    tc.assertEqual(set(entries), set(x.items()))

# points: 20
def test_modification():
    tc = TestCase()
    x = ExtensiblexasxTable()
    random.seed(1234)
    keys = [ random.randint(0,10000000) for i in range(100) ]

    for i in keys:
        x[i] = 0

    for i in range(10):
        for i in keys:
            x[i] = x[i] + 1

    for k in keys:
        tc.assertEqual(x[k], 10)

# points: 20
def test_extension():
    tc = TestCase()
    x = ExtensiblexasxTable(n_buckets=100,fillfactor=0.5)
    nitems = 10000
    for i in range(nitems):
        x[i] = i

    tc.assertEqual(len(x), nitems)
    tc.assertEqual(x.n_buckets, 25600)

    for i in range(nitems):
        tc.assertEqual(x[i], i)


# points: 20
def test_deletion():
    tc = TestCase()
    x = ExtensiblexasxTable(n_buckets=100000)
    random.seed(1234)
    keys = [ random.randint(0,1000000) for i in range(10) ]
    for k in keys:
        x[k] = 1

    for k in keys:
        del x[k]

    tc.assertEqual(len(x), 0)
    with tc.assertRaises(KeyError):
        x[keys[0]]

    with tc.assertRaises(KeyError):
        x[keys[3]]

    with tc.assertRaises(KeyError):
        x[keys[5]]

################################################################################
# TEST HELPERS
################################################################################
def say_test(f):
    print(80 * "*" + "\n" + f.__name__)

def say_success():
    print("SUCCESS")

################################################################################
# MAIN
################################################################################
def main():
    for t in [test_insert,
              test_iteration,
              test_getitem,
              test_modification,
              test_deletion,
              test_extension]:
        say_test(t)
        t()
        say_success()

if __name__ == '__main__':
    main()
