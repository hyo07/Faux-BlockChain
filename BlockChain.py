import hashlib
import json
from datetime import datetime, timedelta, timezone

DIFFICULTY = 1
JST = timezone(timedelta(hours=+9), 'JST')


class BlockChain:
    def __init__(self):
        self.genesis_block = self.make_genesis()
        self.block_chain = [self.genesis_block]

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

    def get_new_block(self, user_name: str, message: str, nonce: int):
        new_bc = {
            "prev_hash": self.get_hash(json.dumps(self.block_chain[-1])),
            # "time_stamp": datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S.%f"),
            "time_stamp": "なうw",
            "user_name": user_name,
            "message": message,
            "nonce": nonce
        }
        new_hash = self.get_hash(json.dumps(new_bc))
        if self.judge_hash(new_hash):
            self.block_chain.append(new_bc)
            return True, new_hash
        else:
            return False, new_hash

    def get_current_block(self):
        return self.block_chain

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

    # USER_NAME = "わたしだ"
    # MESSAGE = "動く"
    # NONCE = 35

    # bc = BlockChain()
    # bc.get_new_block(USER_NAME, MESSAGE, NONCE)
    # print(bc.get_current_block())

    # count = 1
    # bc = BlockChain()
    # while True:
    #     print(count)
    #     new_bc, res_hash = bc.get_new_block(USER_NAME, MESSAGE, count)
    #     print(new_bc)
    #     if new_bc:
    #         print(bc.get_current_block())
    #         break
    #     else:
    #         count += 1

    bc = BlockChain()
    while True:
        print("↓↓↓↓↓ 現在のブロックチェーン ↓↓↓↓↓")
        print(json.dumps(bc.get_current_block(), indent=2))
        print()
        print("保存情報を入力してください")
        user_name = input("user_name: ")
        message = input("message: ")
        try:
            nonce = int(input("nonce: "))
        except ValueError:
            print()
            print("■■■■■■■■■■■■■■■■ ERROR ■■■■■■■■■■■■■■■■")
            print("nonce には整数値を入力してください")
            print("■■■■■■■■■■■■■■■■ ERROR ■■■■■■■■■■■■■■■■")
            print()
            continue
        new_bc, new_hash = bc.get_new_block(user_name, message, nonce)
        print("")
        print("生成ハッシュ値:", new_hash)
        if new_bc:
            print("ブロックの生成に成功しました")
        else:
            print("ブロックの生成に失敗しました")

        print("---------------------------------------")
