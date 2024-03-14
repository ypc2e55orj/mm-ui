import sys

sys.path.append("..")

import conn


def main():
    con = conn.SerialConnection()
    con.connect("COM6")

    while not con.is_abort():
        s = input()

        con.write_bytes(s.encode('utf-8'))
        b = con.read_bytes()

        if b is not None:
            print(b.decode('utf-8'))


if __name__ == "__main__":
    main()
