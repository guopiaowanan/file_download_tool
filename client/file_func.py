import hashlib
import os


def get_md5(f_abs_path):
    """
    获取单个接收文件的MD5值
    """
    with open(f_abs_path,"rb") as f:
        data = f.read()
    m = hashlib.md5()
    m.update(data)
    f_md5 = m.hexdigest()
    print(f_abs_path,"写入成功，MD5值为：",f_md5)
    return f_md5

def recv_file(sock,f_path,f_size):
    """
    单个文件写入
    """    
    try:
        os.makedirs(os.path.dirname(f_path),exist_ok=True)
        print("新建文件夹：",f_path)
    except:
        print("文件夹%s已存在,准备写入" % f_path)

    f = open(f_path,"ab")
    recv_size = 0
    print("正在写入文件：", f_path)
    while recv_size < int(f_size):        
        data = sock.recv(int(f_size) - recv_size)
        if len(data) == 0:
            print("写入成功",f_path)
            break
        f.write(data)
        print("已写入%s字节" % len(data), "文件总大小：",f_size,"还剩余",int(f_size) - recv_size)
        recv_size += len(data)
    f.close()
    get_md5(f_path)

def recv_func(sock):
    dest_d = r"D:\\"
    while True:
        f_path = sock.recv(300).decode().strip()
        if len(f_path) ==  0:
            break
        f_size = sock.recv(15).decode().strip()
        f_md5 = sock.recv(32).decode()   
        f_path = dest_d + f_path

        if int(f_size) == -1:   
            print("正在接收空文件夹：",f_path)
            os.makedirs(f_path,exist_ok=True)
            continue
        
        print("已接收包头文件","\n文件名%s" % f_path, "\n文件大小%s" % f_size,"\n文件MD5值：",f_md5)        
        
        recv_file(sock,f_path,f_size)
    sock.close()
    return