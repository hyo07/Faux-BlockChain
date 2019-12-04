import hashlib
import json
from datetime import datetime, timedelta, timezone
from model import session, BlockChain

DIFFICULTY = 1
JST = timezone(timedelta(hours=+9), 'JST')


class BC:
    def __init__(self):
        self.block_chain = []
        if not self.get_full_chain():
            self.genesis_block = self.make_genesis()
            self.block_chain = [self.genesis_block]

    def make_genesis(self):
        gene_nonce = 0
        while True:
            gene_j = {
                "time_stamp": datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S.%f"),
                # "time_stamp": "なうw",
                "genesis_block": True,
                "nonce": gene_nonce,
            }
            gene_hash = self.get_hash(json.dumps(gene_j))
            if self.judge_hash(gene_hash):
                return gene_j
            else:
                gene_nonce += 1

    def get_new_block(self, user_name: str, message: str, nonce: int):
        if not self.block_chain:
            prev_hash = self.get_hash(json.dumps(self.get_full_chain()[-1]))
        else:
            prev_hash = self.get_hash(json.dumps(self.block_chain[-1]))
        new_bc = {
            "prev_hash": prev_hash,
            "time_stamp": datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S.%f"),
            # "time_stamp": "なうw",
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
        # if top == "0" * difficulty:
        if (top == "0") or (top == "1") or (top == "2") or (top == "3"):
            return True
        else:
            return False

    def save_block(self):
        if len(self.block_chain) > 2:
            self.save_to_db(self.block_chain[0])
            self.block_chain = self.block_chain[1:]
            print("セーブしました")

    def save_to_db(self, block):
        db = BlockChain()
        db.time_stamp = datetime.strptime(block["time_stamp"], "%Y-%m-%d %H:%M:%S.%f")
        db.nonce = int(block["nonce"])
        if "genesis_block" in block:
            db.genesis_block = block["genesis_block"]
        else:
            db.prev_hash = block["prev_hash"]
            db.user_name = block["user_name"]
            db.message = block["message"]
        session.add(db)
        session.commit()
        session.close()

    def get_full_chain(self):
        db_chain = session.query(BlockChain).order_by(BlockChain.index).all()

        if not db_chain:
            return self.block_chain

        genesis_dict = {
            "time_stamp": db_chain[0].time_stamp.strftime("%Y-%m-%d %H:%M:%S.%f"),
            "genesis_block": True,
            "nonce": db_chain[0].nonce,
        }
        full_chain = [genesis_dict]

        for db_block in db_chain[1:]:
            block_dict = {
                "prev_hash": db_block.prev_hash,
                "time_stamp": db_block.time_stamp.strftime("%Y-%m-%d %H:%M:%S.%f"),
                "user_name": db_block.user_name,
                "message": db_block.message,
                "nonce": db_block.nonce,
            }
            full_chain.append(block_dict)
        return full_chain + self.block_chain

    def valid_chain(self):
        full_chain = self.get_full_chain()
        valid_list = []
        index = 0
        hashed = ""
        for block in full_chain:
            if hashed:
                if not hashed == block["prev_hash"]:
                    return None

            hashed = self.get_hash(json.dumps(block))
            valid_dict = {
                "index": index,
                "block": block,
                "hash": hashed,
            }
            index += 1
            valid_list.append(valid_dict)

        return valid_list


if __name__ == "__main__":
    pass

    bc = BC()
    while True:
        print("↓↓↓↓↓ 現在のブロックチェーン ↓↓↓↓↓")
        print(json.dumps(bc.get_full_chain(), indent=2))
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
            bc.save_block()
        else:
            print("ブロックの生成に失敗しました")

        print("---------------------------------------")

    # print("full_chain:", bc.get_full_chain())
    # print("valid_chain:", bc.valid_chain())
