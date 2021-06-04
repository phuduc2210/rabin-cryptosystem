from math import sqrt

# Hệ thống mật mã của Rabin

#const
buff_size = 0x4000

def fast_pow(num, power, mod):
    '''
    Luỹ thừa
    Kết quả bởi mod
    '''
    #result
    res = 1 
    # (b ^ k) * p = num ^ power
    while power > 0:
        while power % 2 == 0:
            power /= 2
            num = (num * num) % mod
        power -= 1
        res = (res * num) % mod
    return res      


def is_prime(num):
    '''
    Chức năng kiểm tra tính nguyên tố tiêu chuẩn
    '''
    if(num == 2):
        return True
    for i in range(2, int(sqrt(num))):
        if num % i == 0:
            return False
    return True

def sieve(num):
    '''
    
    '''
    S = [1 for k in range(num+1)]
    S[1] = 0
    k = 2

    while (k * k <= num):
        if S[k] == 1:
            l = k*k
            while (l <= num):
                S[l] = 0
                l += k
        k += 1

    return S

def chek_input(*, p, q, b, n):
    ''' 
    Kiểm tra đầu vào của các phím đã nhập
    '''
    if (p % 4 == 3 and q % 4 == 3 and 0 < b < n and is_prime(p) and is_prime(q) and n > 255):
        return True
    return False

def file_encrypt(filename, n, b):
    '''
    Mã hóa tệp bằng khóa công khai b và n
    Trả về danh sách với bản mã khi mã hóa thành công 

    '''
    
    f_out = open(filename + ".enc", "w")
    out_data = []
    with open(filename, "rb") as f:
        #Vòng lặp vô tận của việc đọc từ một tệp
        while True: 
            fdata = f.read(buff_size)
            if fdata: #mã hóa những gì được đọc: 
                for byte in fdata:
                    out_data.append((byte * (byte + b)) % n)
            else: #nếu không có gì được đọc, hãy thoát khỏi vòng lặp
                break
        for item in out_data:
            f_out.write(str(item) + " ")
        f.close()
        f_out.close()
    return out_data

def decrypt(c, p, q, b):
    '''
    Giải mã một phần tử của bản mã
    Trả về danh sách các mặt hàng ban đầu
    '''
    n = p * q #khóa công khai
    # D - phân biệt
    D = (b ** 2 + 4 * c) % n
    # Tìm căn bậc hai của D
    #mp_ = (D ** ((p + 1)//4)) % p 
    #mq_ = (D ** ((q + 1)//4)) % q
    mp = fast_pow(D, (p + 1) // 4, p)
    mq = fast_pow(D, (q + 1) // 4, q)

    #Thuật toán Euclid mở rộng
    yp, yq, _gcd = extended_euclid(p, q) #tham số trả về thứ ba không được sử dụng
    
    
    # di - gốc phân biệt
    d1 = (yp * p * mq + yq * q * mp) % n 
    d2 = n - d1
    d3 = (yp * p * mq - yq * q * mp) % n
    d4 = n - d3

    d = (d1, d2, d3, d4)
    m = [] #tin nhắn ban đầu
    for di in d:
        if (di - b) % 2 == 0:
            m.append(int(((-b + di) / 2) % n))
        else:
            m.append(int(((-b + di + n) / 2) % n))
    return m

def extended_euclid(a, b):
    '''
    Thuật toán Euclid mở rộng
    gcd(a, b) = x * a + y * b
    Trả về (x, y, gcd)
    '''

    #Chỉ mục 1 - mục hiện tại, 0 - trước đó
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    while b:
        # r2 = r0 - r1 * q
        # r - phần còn lại của bộ phận
        # q toàn bộ phần của a / b 
        q = a // b 

        a, b = b, a % b

        # để không tạo các biến trung gian, gán bởi bộ
        x0, x1 = x1, x0 - x1 * q
        y0, y1 = y1, y0 - y1 * q
    return (x0, y0, a)                

def file_decrypt(filename, p, q, b):
    '''
    Quy trình giải mã tệp
    '''
    #thay thế phần mở rộng tệp
    f_split = filename.split(".")
    f_expansion = f_split[len(f_split) - 1] # f_expansion = f_split[-1]
    if f_expansion == "enc":
        filename_out = filename.replace(f_expansion, "dec") 
    else:
        filename_out = filename + ".dec"
    
    f_out = open(filename_out, "wb")
    out_data = bytearray([])
    with open(filename, "r") as f:
        #vòng lặp vô tận của việc đọc từ một tệp
        while True:
            fdata_str = f.read(buff_size)
            fdata_str = fdata_str.strip()
            if fdata_str:
                fdata = fdata_str.split(" ") #nhận các giá trị bản mã từ một tệp
                for item in fdata:
                    if not is_number(item):
                        return []
                    m = decrypt(int(item), p, q, b)
                    for i in range(len(m)):
                        if m[i] <= 255:
                            out_data.append(m[i])
            else:
                break
        f.close()

    f_out.write(out_data)
    f_out.close()
    return out_data  

def get_byte_from_file(filename):

    with open(filename, "rb") as f:
        while True:
            fdata = f.read(buff_size)
            if fdata:
                for item in fdata:
                    yield item
            else:
                break
        f.close()

def get_num_from_file(filename):

    with open(filename, "r") as f:
        while True:
            fdata_str = f.read(buff_size)
            fdata_str = fdata_str.strip()
            if fdata_str:
                fdata = fdata_str.split(" ")
                for item in fdata:
                    yield item
            else:
                break
        f.close()   

def is_number(num):
    '''
    Kiểm tra xem một chuỗi có phải là một số không
    '''      
    #ký hiệu có sẵn
    symb = [str(i) for i in range(10)]
    if num.strip() == '':
        return False
    for dig in num:
        if dig not in symb:
            return False
    return True       