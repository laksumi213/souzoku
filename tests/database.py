import sqlite3
from models import Customer, Bank
from config import DB_FILE


class DatabaseManager:
    """
    SQLiteデータベースを管理するクラス。
    顧客情報と銀行情報のテーブル作成、CRUD操作を提供します。
    """

    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        """データベースに接続します。"""
        try:
            self.conn = sqlite3.connect(DB_FILE)
            self.cursor = self.conn.cursor()
            print(f"データベース '{DB_FILE}' に接続しました。")
        except sqlite3.Error as e:
            print(f"データベース接続エラー: {e}")

    def create_tables(self):
        """
        顧客情報と銀行情報のテーブルを作成します。
        テーブルが存在しない場合にのみ作成されます。
        """
        if not self.conn:
            return

        # 顧客情報テーブル
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS customers (
                customer_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                address TEXT,
                phone TEXT
            )
        """
        )

        # 銀行情報テーブル
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS banks (
                bank_id TEXT PRIMARY KEY,
                bank_name TEXT NOT NULL,
                account_number TEXT,
                branch TEXT
            )
        """
        )
        self.conn.commit()
        print("テーブルが作成または既に存在します。")

    def insert_customer(self, customer: Customer) -> bool:
        """顧客情報を挿入します。"""
        try:
            self.cursor.execute(
                "INSERT INTO customers (customer_id, name, address, phone) VALUES (?, ?, ?, ?)",
                (customer.customer_id, customer.name, customer.address, customer.phone),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # customer_id が重複している場合
            return False
        except sqlite3.Error as e:
            print(f"顧客情報挿入エラー: {e}")
            return False

    def update_customer(self, customer: Customer) -> bool:
        """顧客情報を更新します。"""
        try:
            self.cursor.execute(
                "UPDATE customers SET name = ?, address = ?, phone = ? WHERE customer_id = ?",
                (customer.name, customer.address, customer.phone, customer.customer_id),
            )
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"顧客情報更新エラー: {e}")
            return False

    def delete_customer(self, customer_id: str) -> bool:
        """顧客情報を削除します。"""
        try:
            self.cursor.execute(
                "DELETE FROM customers WHERE customer_id = ?", (customer_id,)
            )
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"顧客情報削除エラー: {e}")
            return False

    def get_all_customers(self) -> list[Customer]:
        """全ての顧客情報を取得します。"""
        try:
            self.cursor.execute(
                "SELECT customer_id, name, address, phone FROM customers"
            )
            return [Customer(*row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"顧客情報取得エラー: {e}")
            return []

    def insert_bank(self, bank: Bank) -> bool:
        """銀行情報を挿入します。"""
        try:
            self.cursor.execute(
                "INSERT INTO banks (bank_id, bank_name, account_number, branch) VALUES (?, ?, ?, ?)",
                (bank.bank_id, bank.bank_name, bank.account_number, bank.branch),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # bank_id が重複している場合
            return False
        except sqlite3.Error as e:
            print(f"銀行情報挿入エラー: {e}")
            return False

    def update_bank(self, bank: Bank) -> bool:
        """銀行情報を更新します。"""
        try:
            self.cursor.execute(
                "UPDATE banks SET bank_name = ?, account_number = ?, branch = ? WHERE bank_id = ?",
                (bank.bank_name, bank.account_number, bank.branch, bank.bank_id),
            )
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"銀行情報更新エラー: {e}")
            return False

    def delete_bank(self, bank_id: str) -> bool:
        """銀行情報を削除します。"""
        try:
            self.cursor.execute("DELETE FROM banks WHERE bank_id = ?", (bank_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"銀行情報削除エラー: {e}")
            return False

    def get_all_banks(self) -> list[Bank]:
        """全ての銀行情報を取得します。"""
        try:
            self.cursor.execute(
                "SELECT bank_id, bank_name, account_number, branch FROM banks"
            )
            return [Bank(*row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"銀行情報取得エラー: {e}")
            return []

    def close(self):
        """データベース接続を閉じます。"""
        if self.conn:
            self.conn.close()
            print("データベース接続を閉じました。")
