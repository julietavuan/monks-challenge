"""Run monks API"""
from controller.monk import socket_, app

if __name__ == '__main__':
    socket_.run(app, debug=True)
