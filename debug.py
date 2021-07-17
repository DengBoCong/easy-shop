if __name__ == '__main__':
    a = 0X01
    b = 0X02
    c = 0X03
    d = 0X04
    f = 0X05
    g = 0X06
    h = 0X07

    admin = a + b + d
    public = c + d
    print(admin & c == c)
    print(admin & d == d)