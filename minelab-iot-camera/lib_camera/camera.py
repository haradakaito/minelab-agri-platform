import cv2

class Camera:
    def __init__(self):
        self.cap    = cv2.VideoCapture(0, cv2.CAP_V4L2) # for Linux
        # self.cap  = cv2.VideoCapture(0)               # for Windows
        self.frame  = None
        self.memory = []

    def _encode_frame(self, frame, ext='.jpg') -> bytes:
        """画像をエンコードする関数"""
        _, buffer = cv2.imencode(ext, frame)
        return buffer.tobytes()

    def capture(self) -> None:
        """カメラから画像を取得する関数"""
        # カメラがオープンされていない場合はNoneを返す
        if not self.cap.isOpened():
            raise Exception("カメラがオープンされていません")
        # カメラから画像を取得する
        ret, frame = self.cap.read()
        if not ret:
            self.cap.release()
            raise Exception("画像の取得に失敗しました")
        # 画像を一時的に保存する
        self.frame = frame

    def save(self) -> None:
        """一時的に保存してあるframeをメモリに保存"""
        self.memory.append(self.frame)

    def get(self, id: int=-1) -> bytes:
        """メモリから画像を取得する"""
        return self._encode_frame(frame=self.memory[id])

    def clear(self) -> None:
        """メモリをクリア"""
        self.frame  = None
        self.memory = []

# 使用例
if __name__ == "__main__":
    try:
        # カメラから画像を取得
        camera = Camera()
        camera.capture()
        camera.save()
        if camera.get():
            print("画像の取得に成功しました")
        else:
            print("画像の取得に失敗しました")
    except Exception as e:
        print(e)
    finally:
        camera.clear()