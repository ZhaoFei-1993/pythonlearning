def main():
    demo_dict = {
        "1": "abc",
        "2": "bcd",
        "3": "cde"
    }
    for key in demo_dict:
        print("key = %s, value = %s \n" % (key, demo_dict.get(key)))


if __name__ == '__main__':
    main()
