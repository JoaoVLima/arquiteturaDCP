#!/usr/bin/env python3

import sys
import etcd3


class Etcd:
    def __init__(self):
        self.etcd = etcd3.client(host='localhost', port=2379)

    def get(self, key, prefix: bool = False):
        if prefix:
            value, metadata = self.etcd.get_prefix(key_prefix=str(key))
        else:
            value, metadata = self.etcd.get(key=str(key))

        value = value.decode('utf-8')
        metadata = metadata.key.decode('utf-8')

        return value

    def put(self, key, value):
        try:
            self.etcd.put(key=str(key), value=str(value))
        except:
            return False
        return True


class LeaderElection(Etcd):
    def __init__(self, election_name):
        super().__init__()
        self.election_name = election_name
        self.leader_key = f'/{self.election_name}/leader'
        self.candidates_key = f'/{self.election_name}/candidates/'

    def get_leader(self):
        leader_name = self.get(self.leader_key)
        return leader_name


class Candidate(LeaderElection):
    def __init__(self, election_name):
        super().__init__(election_name=election_name)




if __name__ == "__main__":
    election_name = 'election'
    candidate_name = 'A'
    if len(sys.argv) > 1:
        election_name = sys.argv[1]
        candidate_name = sys.argv[2]

    cliente = Candidate(election_name=election_name)
    cliente.put('teste', 'valor')
    cliente.put('teste2', {'lider': 'A'})
    teste = cliente.get('teste')
    teste2 = cliente.get('teste2', is_return_dict=True)

    print(teste, teste2)
