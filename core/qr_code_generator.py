import qrcode


def main():

    file = open("address.txt")

    while 1:
        line = file.readline()
        if not line:
            break
        else:
            config = {
                'data': line,
                'box_size': 20,
                'border': 8
            }
            img = qrcode.make(config)
            img.save(line + ".png")


if __name__ == '__main__':
    main()