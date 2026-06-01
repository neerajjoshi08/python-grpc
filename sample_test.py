import collections

Person = collections.namedtuple("Person", ["name", "age"])


class Family:
    def __init__(self):
        self._persons = [
            Person("Alice:" + str(name), age)
            for name, age in zip(range(10), range(10))
        ]

    def __len__(self):
        return len(self._persons)

    def __getitem__(self, position):
        return self._persons[position]

    def __add__(self, person: Person):
        print("Adding the person")
        name = person.name
        age = person.age

        for _person in self._persons:
            name += _person.name
            age += _person.age
        return Person(name=name, age=age)


family = Family()
print(f"Length of family is: {len(family)}")
print(f"Third Family person is: {family[2]}")

new_person = family + Person(name="Hello", age=0)
print(new_person)


from math import hypot


class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Vector(%r, %r)" % (self.x, self.y)

    def __abs__(self):
        return hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)


v = Vector("1", "2")
print(v)
