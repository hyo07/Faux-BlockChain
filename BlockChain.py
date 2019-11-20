import hashlib
import json
from datetime import datetime, timedelta, timezone

DIFFICULTY = 1
JST = timezone(timedelta(hours=+9), 'JST')


class BlockChain:
    def __init__(self, user_name: str, message: str, nonce: int):
        self.genesis_block = self.make_genesis()
        self.block_chain = [self.genesis_block]

        self.user_name = user_name
        self.message = message
        self.nonce = nonce

    def make_genesis(self):
        gene_nonce = 0
        while True:
            gene_j = {
                # "time_stamp": datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S.%f"),
                "time_stamp": "なうw",
                "genesis_block": True,
                "nonce": gene_nonce,
            }
            gene_hash = self.get_hash(json.dumps(gene_j))
            if self.judge_hash(gene_hash):
                return gene_j
            else:
                gene_nonce += 1

    def get_new_block(self):
        new_bc = {
            "prev_hash": self.get_hash(json.dumps(self.block_chain[-1])),
            # "time_stamp": datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S.%f"),
            "time_stamp": "なうw",
            "user_name": self.user_name,
            "message": self.message,
            "nonce": self.nonce
        }
        new_hash = self.get_hash(json.dumps(new_bc))
        if self.judge_hash(new_hash):
            self.block_chain.append(new_bc)
            print(self.block_chain)
            return True
        else:
            return False

    def get_hash(self, new_data: str):
        return hashlib.sha256(new_data.encode()).hexdigest()

    def judge_hash(self, digest, difficulty=DIFFICULTY):
        top = digest[:difficulty]
        if top == "0" * difficulty:
            return True
        else:
            return False


if __name__ == "__main__":
    pass

    USER_NAME = "yutaka"
    MESSAGE = "てすと〜"
    NONCE = 16

    # bc = BlockChain(USER_NAME, MESSAGE, NONCE)
    # print(bc.get_new_block())

    count = 1
    while True:
        print(count)
        bc = BlockChain(USER_NAME, MESSAGE, count)
        new_bc = bc.get_new_block()
        if new_bc:
            break
        else:
            count += 1
