def main():
    file = open("completed_with_path.txt", "r")
    trues = 0
    falses = 0
    for line in file:
        if not line.split()[0] == line.split()[-2].split("'")[1]:
            value = line.split()[-1]
            if value == 'True':
                trues += 1
            elif value == 'False':
                falses += 1
            else:
                print("ERROR")
    print('Trues: ' + str(trues))
    print('Falses: ' + str(falses))
    print('Percentage: ' + str(trues/(trues+falses)))


if __name__ == '__main__':
    main()
