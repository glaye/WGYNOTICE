from rediscluster import StrictRedisCluster
from util import Readconf

cf = Readconf.Readconf().readConfigFile()
class Myrediscluster:
    def __init__(self):
        startup_nodes = [
            {"host": cf.get('Redis', 'h0'), "port": int(cf.get('Redis', 'p0'))},
            {"host": cf.get('Redis', 'h1'), "port": int(cf.get('Redis', 'p1'))},
            {"host": cf.get('Redis', 'h2'), "port": int(cf.get('Redis', 'p2'))},
            {"host": cf.get('Redis', 'h3'), "port": int(cf.get('Redis', 'p3'))},
            {"host": cf.get('Redis', 'h5'), "port": int(cf.get('Redis', 'p4'))},
            {"host": cf.get('Redis', 'h5'), "port": int(cf.get('Redis', 'p5'))},
        ]
#        print(startup_nodes)

        self.rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)
    def set(self, key, value, ex=None, px=None, nx=False, xx=False):
        self.rc.set(key, value, ex, px, nx,xx)

    def get(self, key):
        return self.rc.get(key)

    def incr(self, key, amount = 1):
        self.rc.incr(key,amount)

if (__name__ == '__main__'):

    rc = Myrediscluster()
#    print(rc.set('fds33a','world'))
#    print(rc.get('fds33a'))
#    print(rc.get('world'))
    '''
    startup_nodes = [
        {"host": "172.17.46.12", "port": 9100},
        {"host": "172.17.46.12", "port": 9101},
        {"host": "172.17.46.12", "port": 9102},
        {"host": "172.17.46.12", "port": 9103},
        {"host": "172.17.46.12", "port": 9104},
        {"host": "172.17.46.12", "port": 9105}
    ]
    rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)
    rc.set('name', 'admin')
    rc.set('age', 18)
    print("name is: ", rc.get('name'))
    print("age  is: ", rc.get('age'))
'''
