import matplotlib.pyplot as plt


class DistancePlot:
    def start(self):
        x = []
        y = []
        file = open("distances.txt", "r")
        for line in file:
            if ':' in line:
                point = line.split(':')
                x.append(int(point[0]))
                y.append(int(point[1][:-1]))
        plt.plot(x, y)
        plt.show()


def main():
    p = DistancePlot()
    p.start()


if __name__ == '__main__':
    main()
