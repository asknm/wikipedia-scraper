class Counter:
    def start(self):
        file = open("completed_with_path.txt", "r")
        pages = []
        for line in file:
            page = line.split()[0]
            index = self.in_pages(pages, page)
            if index > -1:
                #pages[index][1] += 1
                pages.append((page, pages[index][1] + 1))
                pages.pop(index)
            else:
                pages.append((page, 1))
        pages.sort(key=lambda tup: tup[1])
        file = open("top_pages.txt", "w")
        for p in pages:
            file.write(p[0] + ' ' + str(p[1]) + '\n')


    def in_pages(self, pages, page):
        i = 0
        for p in pages:
            if page == p[0]:
                return i
            i += 1
        return -1


def main():
    c = Counter()
    c.start()


if __name__ == '__main__':
    main()
