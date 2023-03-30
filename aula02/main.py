#!/usr/bin/env python3
import random
import sys
import uuid

import etcd3

# Cada candidato a líder C possui um identificador único e
# ao ser executado, tenta tornar-se líder.
# Se já houver outro processo L líder, C aguarda que L termine (ou aborte) a sua execução para então novamente tentar se tornar o líder.
# Certifique-se de que apenas 1 único processo se torne líder em um dado momento!


class Etcd:
    def __init__(self, lease_connection=True):
        self.etcd = etcd3.client(host='localhost', port=2379)
        self.lease = None
        if lease_connection:
            self.acquire_lease()

    def get(self, key: str, prefix: bool = False, return_kv: bool = False):
        if prefix:
            value, metadata = self.etcd.get_prefix(key_prefix=key)
        else:
            value, metadata = self.etcd.get(key=key)

        value = value.decode('utf-8')
        metadata = metadata.key.decode('utf-8')

        if return_kv:
            return value, metadata
        return value

    def put(self, key: str, value: str):
        try:
            self.etcd.put(key=key, value=value, lease=self.lease)
        except:
            return False
        return True

    def delete(self, key: str, return_deleted: bool = False):
        try:
            self.etcd.delete(key=key, prev_kv=return_deleted)
        except:
            return False
        return True

    def lock(self, key: str):
        with self.etcd.lock(key) as lock:
            # do something that requires the lock
            print(lock.is_acquired())

            # refresh the timeout on the lease
            lock.refresh()

    def acquire_lease(self, ttl=60, lease_id=None):
        if not lease_id:
            lease_id = random.randint(100_000, 999_999)  # uuid.uuid4() would be better
        self.lease = self.etcd.lease(ttl=ttl, lease_id=lease_id)

    def refresh_lease(self):
        if not self.lease:
            return False
        self.etcd.refresh_lease(self.lease.id)
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

    def acquire(self, key: str):
        self.lock(key=key)


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
    cliente.put('teste2', 'asd')
    teste = cliente.get('teste')
    teste2 = cliente.get('teste2')

    print(teste, teste2)
