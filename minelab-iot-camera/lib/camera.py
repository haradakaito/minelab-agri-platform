import os
import cv2

class Camera:
    def __init__(self):
        # self.cap   = cv2.VideoCapture(0, cv2.CAP_V4L2) # for Linux
        self.cap   = cv2.VideoCapture(0) # for Windows

    def capture(self):
        """カメラから画像を取得する関数"""
        # カメラがオープンされていない場合はNoneを返す
        if not self.cap.isOpened():
            raise ValidationError("カメラがオープンされていません")
        # カメラから画像を取得する
        ret, frame = self.cap.read()
        if not ret:
            self.cap.release()
            raise ValidationError("画像の取得に失敗しました")
        return frame

    def encode_frame(self, frame, ext='.jpg') -> bytes:
        """画像をエンコードする関数"""
        _, buffer = cv2.imencode(ext, frame)
        return buffer.tobytes()

# 使用例
if __name__ == "__main__":
    from custom_error import ValidationError, ErrorHandler, BaseCustomError

    try:
        # カメラから画像を取得
        camera = Camera()
        frame  = camera.capture()
        # 画像を表示
        if frame is not None:
            # 画像をエンコード
            encoded_frame = camera.encode_frame(frame)
            print("画像を取得しました")
        else:
            raise ValidationError("画像が取得できませんでした")
    except BaseCustomError as e:
        handler = ErrorHandler(log_file=f'../log/test-{os.path.splitext(__file__)[0]}.log')
        handler.handle_error(e)
else:
    from lib.custom_error import ValidationError