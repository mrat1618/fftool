#!/usr/bin/env python

import sys, operator

class Atom:
    def __init__(self, name, x, y, z):
        self.name = name
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    def __repr__(self):
        return repr((self.x, self.y, self.z))
    def __str__(self):
        return "%-4s %11.6f %11.6f %11.6f" % \
          (self.name, self.x, self.y, self.z)

def main():
    if len(sys.argv) < 2:
        print 'Manipulate xyz file'
        print 'usage: xyztool.py command file.xyz'
        print 'commands:'
        print '  sort {xyz|zxy|...}'
        print '  swap {xy|xz|yz}'
        print '  move {x|y|z} {all|n1:n2} dist/A'
        sys.exit(1)
    cmd = sys.argv[1]
    file = sys.argv[-1]

    atom = []
    with open(file, 'r') as f:
        tok = f.readline().strip().split()
        natom = int(tok[0])
        title = f.readline().strip()
        for i in range(natom):
            tok = f.readline().strip().split()
            atom.append(Atom(tok[0], tok[1], tok[2], tok[3]))
            
    if cmd.startswith('so'):
        key1, key2, key3 = sys.argv[2]
        atom.sort(key = operator.attrgetter(key1, key2, key3))

    elif cmd.startswith('sw'):
        key1, key2 = sys.argv[2]
        for at in atom:
            val1 = getattr(at, key1)
            val2 = getattr(at, key2)
            setattr(at, key1, val2)
            setattr(at, key2, val1)

    elif cmd.startswith('m'):
        key = sys.argv[2]
        index = sys.argv[3]
        if index.startswith('a'):
            start = 0
            stop = len(atom) - 1
        else:
            tok = index.split(':')
            start, stop = [ int(t) - 1 for t in tok ]
        d = float(sys.argv[4])
        for index, at in enumerate(atom):
            if index >= start and index <= stop:
                val = getattr(at, key)
                setattr(at, key, val + d)

    else:
        print 'bad command'
        sys.exit(1)

    print natom
    print title
    for at in atom:
        print at
            
if __name__ == "__main__":
    main()
