#coding=utf8
import time
import jwt
import os
from config import basedir
import sys



class JWTConfig:
    def __init__(self):
        self.token = ""
        self.key_id = "GQBTQVVQZT"
        self.team_id = "9295SUH62C"
        self.service_id = "com.xueping.weatherkitweb"
        path = os.path.join(basedir, "AuthKey_GQBTQVVQZT.p8")
        f = open(path, "r")
        self.private_key = f.read()
        self.cur_time = int(time.time())
        self.expiry = (int(time.time()) + 3600)
        self.algorithm = "ES256"
        f.close()


    def genToken(self):
        # 如果token没有初始化 or token过期了 => 生成新的token
        if self.token == "" or self.__tokenAlreadyExpired():
            self.cur_time = int(time.time())
            self.expiry = (int(time.time()) + 3600)
            payload = self.__getPayload()
            private_key = self.private_key
            algorithm = self.algorithm
            headers = self.__getHeaders()
            self.token = jwt.encode(payload=payload, key=private_key, algorithm=algorithm, headers=headers)
        return self.token

    def __tokenAlreadyExpired(self) :
        return int(time.time()) > self.expiry

    def __getPayload(self) :
        return {"iss": self.team_id, "iat": self.cur_time, "exp": self.expiry, "sub": self.service_id}

    def __getHeaders(self) :
        return {"kid": self.key_id, "id": (self.team_id + '.' + self.service_id), "alg": self.algorithm}