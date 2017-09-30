# -*- coding: utf-8 -*-
# @Author t-liya
import base64
from urllib.parse import quote
from Crypto.Cipher import AES
import wget


class AESEncryption:
    PADDING = 16
    KEY = [222, 237, 16, 66, 28, 26, 85, 99, 114, 184, 88, 192, 37, 112, 222, 209, 241, 24, 175, 144, 173, 53, 105, 29,
           24, 26, 17, 218, 131, 236, 53, 209]
    VECTOR = [146, 44, 101, 111, 66, 32, 99, 119, 231, 121, 211, 88, 77, 32, 104, 156]
    key_bytes = bytes(bytearray(KEY))
    iv_bytes = bytes(bytearray(VECTOR))

    def __pad_it(self, source):
        return source + (16 - len(source) % 16) * chr(self.PADDING - len(source) % self.PADDING)

    def __unpad_it(self, source):
        return source.rstrip(chr(self.PADDING - len(source) % self.PADDING))

    def encrypt(self, plaintext):
        generator = AES.new(self.key_bytes, AES.MODE_CBC, self.iv_bytes)
        crypt = generator.encrypt(self.__pad_it(plaintext))
        return base64.b64encode(crypt)

    def decrypt(self, ciphertext):
        generator = AES.new(self.key_bytes, AES.MODE_CBC, self.iv_bytes)
        return self.__unpad_it(generator.decrypt(ciphertext))


class BingProxy(object):
    bing_proxy = 'http://www.bing.com/dict/proxy/proxy?k=%s'
    encryption = AESEncryption()

    def get_proxy_url(self, url):
        return self.bing_proxy % quote(self.encryption.encrypt(url))


# IP代理工具


f = open('record2.txt', 'r', encoding='utf-8')
fw = open('wr1.txt', 'w')
for line in f:
    l = line.strip().split(' ')
    print(l[0])
    s = BingProxy()
    url = s.get_proxy_url('http://www.midishow.com/midi/file/'+str(l[0])+'.mid')
    fw.write(str(url)+' '+str(l[0]))
    fw.write('\n')
    print(url)

#wget('url')


















