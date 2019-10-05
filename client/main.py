#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import sys
import os
import hashlib
import re
import json
from normal_func import check_phone, check_password 
from file_func import get_md5,recv_func


def check_user_name(user_name):
    """"
    功能：客户端校验用户名是否存在请求
    参数：user_name 用户名
    返回值（"error_code"）： 0表示不存在，1表示存在,2为用户名不合法

    """
    if not re.match("^[a-zA-Z0-9_]{6,15}$", user_name):
        return 2
    msg_send = {"op": 3,"args": {"uname":user_name}}
    msg_send = json.dumps(msg_send).encode()

    msg_len = "{:<15}".format(len(msg_send)).encode()

    sock.send(msg_len)
    sock.send(msg_send)

    recv_len = int(sock.recv(15).decode().strip())

    dest_recv = 0
    recv_data = b""
    while True:
        tmp = sock.recv(recv_len-dest_recv)
        dest_recv += len(tmp)
        if len(tmp) == 0 :
            break
        recv_data += tmp

    recv_msg = json.loads(recv_data) 
    error_code = recv_msg["error_code"]
    if error_code == 0:
        print("用户名未被占用")
    elif error_code == 1:
        print("用户名已存在，请重新输入！")
    elif error_code == 2:
        print("用户名不合法！")
  


def reg_rsp(uname,passwd,phone,email):
    """
    功能：向服务器端发送用户注册请
    参数：uname,passwd,phone,email
    返回值："error_code": 0  # 0表示注册成功，1表示注册失败
    """
    reg_msg = {"op": 2,"args": {"uname": uname, "passwd": passwd,"phone": phone, "email":email  }} 
    
    msg = json.dumps(reg_msg).encode()
    print(msg)

    msg_len = "{:<15}".format(len(msg)).encode()
    
    sock.send(msg_len)
    print(len(msg_len))
    sock.send(msg)

    recv_len = int(sock.recv(15).decode().strip())
    dest_recv = 0
    recv_data = b""
    while True:
        tmp = sock.recv(recv_len-dest_recv)
        dest_recv += len(tmp)
        if len(tmp) == 0 :
            break
        recv_data += tmp
    
    
    recv_msg = json.loads(recv_data) 
    error_code = recv_msg["error_code"]
    return error_code



def reg_main():
    """
    功能：用户注册主程序
    参数：无
    返回值无
    """
    user_name = input("请输入用户名（只能包含英文字母、数字或下划线，最短6位，最长15位）：")
       
    while True:
        while True:
            password = input("请输入密码：")
            ret = check_password(password)

            if ret == 0:
                break
            elif ret == 1:
                print("密码不符合长度要求，请重新输入！")
            elif ret == 2:
                print("密码太简单，请重新输入！")

        confirm_pass = input("请再次输入密码：")

        if password == confirm_pass:
            confirm_pass = confirm_pass.encode(encoding="utf8")
            m = hashlib.md5()
            m.update(confirm_pass)
            passwd = m.hexdigest().upper()
            break
        else:
            print("两次输入的密码不一致，请重新输入！")

    while True:
        phone = int(input("请输入手机号："))
        ret = check_phone(phone)
        if ret == 1:
            print("手机号输入错误，请重新输入！")
        else:
            break
    email = input("请输入邮箱：")
    ret_reg = reg_rsp(user_name,passwd,phone,email)   
    if ret_reg == 1:
        print("注册失败")
    else :
        print("恭喜！注册成功\\nuser_name,passwd,phone,email分别为：",user_name,passwd,phone,email)

def login_main():
    """
    功能：向服务器端发送用户登录请求
    参数：无
    函数返回值：无
    服务器响应值"error_code"：0表示注册成功，1表示注册失败
    """

    user_name = input("请输入登录用户名：")
    password = input("请输入登录用密码：").encode()
    m = hashlib.md5()
    m.update(password)
    passwd = m.hexdigest().upper()
    msg = {"op": 1,"args":{"uname": user_name,"passwd": passwd}}
    msg_send = json.dumps(msg).encode()
    msg_len = "{:<15}".format(len(msg_send)).encode()
    sock.send(msg_len)
    sock.send(msg_send)

    recv_len = int(sock.recv(15).decode().strip())
    print(recv_len)
    dest_recv = 0
    recv_data = b""
    while True:
        tmp = sock.recv(recv_len-dest_recv)
        dest_recv += len(tmp)
        if len(tmp) == 0 :
            break
        recv_data += tmp

    recv_data = recv_data.decode(errors="ignore")   
    recv_msg = json.loads(recv_data)
    error_code = recv_msg["error_code"]
    if error_code ==0:
        print("登录成功")
        recv_func(sock)        
    elif error_code ==1:
        print("登录失败")


conf = json.load(open("conf.json"))
sock = socket.socket()
sock.connect((conf["server_ip"],conf["server_port"]))
print("连接成功！")
try:

    print("\n您可以输入1登录用户，2注册用户，3查询用户名是否合法,4退出向导")
    i = int(input(">>>>>"))
    if i == 1:
        login_main()
    elif i == 2:
        reg_main()
    elif i == 3:
        user_name = input("请输入您想查询的用户名")
        check_user_name(user_name)
    elif i == 4:
        print("再见")

    else:
        print("你输的啥")
finally:
    sock.close()
    




