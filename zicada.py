#!-*-coding:utf-8-*-
from main.main import configSystem

if __name__=="__main__":
    try:
        configSystem()
    except Exception as e:
        print(e)
