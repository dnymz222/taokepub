#coding=utf8
import time
import jwt
import os
from config import basedir
import sys



class HefengJWTConfig:
    def __init__(self):
        self.token = ""
        self.kid = "KCGX3DMADG"
        self.team_id = "4FKRT36W2R"
        path = os.path.join(basedir, "ed25519-private.pem")
        f = open(path, "r")
        self.private_key = f.read()
        self.cur_time = int(time.time())
        self.expiry = (int(time.time()) + 3600)
        self.algorithm = "EdDSA"
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
        return { "iat": self.cur_time, "exp": self.expiry, "sub": self.team_id}

    def __getHeaders(self) :
        return {"kid": self.kid, "alg": self.algorithm}