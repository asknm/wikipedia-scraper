class PageRanker:
    pages = []
    def start(self):
        file = open("completed_with_path.txt", "r")
        paths = []

        for line in file:
            path = line.split()[1:-1]
            for i in range(len(path)):
                path[i] = path[i].split("'")[1]
            if path not in paths:
                paths.append(path)
                for i in range(len(path)):
                    index = self.in_pages(path[i])
                    if index > -1:
                        self.add_points(index, i)
                    else:
                        self.pages.append((path[i], i, path))
        self.pages.sort(key=lambda tup: tup[1])
        file = open("top_pages2.txt", "w")
        for p in self.pages:
            file.write(p[0] + ' ' + str(p[1]) + '\n')

    def add_points(self, index, points):
        self.pages[index] = (self.pages[index][0], self.pages[index][1] + points, self.pages[index][2])
        i = 0
        for page in self.pages[index][2]:
            if page == self.pages[index][0] and i+1 < len(self.pages[index][2]):
                next_page = self.pages[index][2][i+1]
                print(next_page)
                next_page_index = self.in_pages(next_page)
                if not self.pages[next_page_index][0] == '/wiki/Philosophy':
                    if self.pages[next_page_index][0] == '/wiki/Province_of_Schleswig-Holstein':
                        print('PSH')
                    self.add_points(next_page_index, points)
                break
            i += 1

    def in_pages(self, page):
        i = 0
        for p in self.pages:
            if page == p[0]:
                return i
            i += 1
        return -1


def main():
    p = PageRanker()
    p.start()


if __name__ == '__main__':
    main()
