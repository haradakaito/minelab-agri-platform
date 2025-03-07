import hashlib
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class AESCodec:
    """AES暗号化・復号クラス"""
    def __init__(self, key: str) -> None:
        # keyをハッシュ化して鍵を生成
        self.key = self._hashed_key(key)

    def _hashed_key(self, key: str) -> bytes:
        """keyをハッシュ化して鍵を生成"""
        try:
            return hashlib.sha256(key.encode('utf-8')).digest()
        except Exception as e:
            raise e

    def encrypt(self, plaintext: str) -> str:
        """
        AES暗号化

        Parameters
        ----------
        plaintext : str
            平文

        Returns
        -------
        str
            IV + ciphertextの16進文字列

        Raises
        ------
        ValidationError
            AES暗号化に失敗した場合

        Notes
        -----
        - IV: 初期化ベクトル
        - ciphertext: 暗号文
        """
        try:
            # ランダムなIVを生成
            iv = os.urandom(16)
            # AES暗号器を生成
            cipher    = Cipher(algorithms.AES(self.key), modes.CFB(iv))
            encryptor = cipher.encryptor()
            # 暗号化
            ciphertext = encryptor.update(plaintext.encode('utf-8')) + encryptor.finalize()
            # IV + ciphertextを結合して返す
            encrypted_data = iv + ciphertext
            return encrypted_data.hex()
        except Exception as e:
            raise e

    def decrypt(self, encrypted_data: str) -> str:
        """
        AES復号

        Parameters
        ----------
        encrypted_data : str
            IV + ciphertextの16進文字列

        Returns
        -------
        str
            復号された平文

        Raises
        ------
        ValidationError
            AES復号に失敗した場合
        """
        try:
            # IVとciphertextに分割
            encrypted_data = bytes.fromhex(encrypted_data)
            iv         = encrypted_data[:16]
            ciphertext = encrypted_data[16:]
            # AES復号器を生成
            cipher    = Cipher(algorithms.AES(self.key), modes.CFB(iv))
            decryptor = cipher.decryptor()
            # 復号
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            return plaintext.decode('utf-8')
        except Exception as e:
            raise e

# 使用例
if __name__ == "__main__":
    try:
        mac_address = "00:00:00:00:00:00"
        codec = AESCodec(key=mac_address)

        original_text = "Hello, World!"
        print("Original Text:", original_text)

        encrypted_data = codec.encrypt(original_text)
        print("Encrypted Data:", encrypted_data)

        decrypted_text = codec.decrypt(encrypted_data)
        print("Decrypted Text:", decrypted_text)
    except Exception as e:
        print(e)