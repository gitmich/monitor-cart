import cv2
import time
import picamera
import picamera.array

# 創建一個 PiCamera 物件
with picamera.PiCamera() as camera:
    # 設置相機的解析度
    camera.resolution = (640, 480)
    # 創建一個 PiRGBArray 物件，用於存儲影像
    with picamera.array.PiRGBArray(camera) as stream:
        # 啟動預覽
        camera.start_preview()
        try:
            while True:
                # 捕捉影像
                camera.capture(stream, format='bgr', use_video_port=True)
                # 獲取 numpy 數組格式的影像
                image = stream.array
                # 顯示影像
                cv2.imshow('Pi Camera', image)
                # 清空流，準備下一次捕捉
                stream.truncate(0)
                # 如果按下 'q'，則退出
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            cv2.destroyAllWindows()
            camera.stop_preview()
