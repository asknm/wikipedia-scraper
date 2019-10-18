class Distance:
    pages = []
    distances = []
    paths = []
    def start(self):
        file = open("completed_with_path.txt", "r")
        for line in file:
            if line.split()[-1] == 'True':
                path = line.split()[1:-1]
                for i in range(len(path)):
                    path[i] = path[i].split("'")[1]
                if path not in self.paths:
                    if path[-1] == '/wiki/Philosophy':
                        while len(self.distances)+1 < len(path):
                            self.distances.append(0)
                        for i in range(len(path)-1):
                            self.distances[i] += 1
                    else:
                        distance = self.get_distance(path[-1])
                        while len(self.distances)+1 < len(path) + distance:
                            self.distances.append(0)
                        for i in range(distance, distance + len(path)-1):
                            self.distances[i] += 1
                    self.paths.append(path)

        file = open("distances.txt", "w")
        i = 1
        for distance in self.distances:
            file.write(str(i) + ':' + str(distance) + '\n')
            i += 1

    def get_distance(self, page):
        for path in self.paths:
            index = self.in_path(page, path)
            if index > -1:
                if path[-1] == '/wiki/Philosophy':
                    return len(path) - index - 1
                else:
                    return self.get_distance(path[-1]) + len(path) - index - 1

    def in_path(self, page, path):
        i = 0
        for word in path:
            if word.startswith(page):
                return i
            i += 1
        return -1

def main():
    d = Distance()
    d.start()


if __name__ == '__main__':
    main()
