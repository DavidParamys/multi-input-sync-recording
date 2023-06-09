from app_modules import *
from app_functions import *
from app_define import *

if __name__ == '__main__':
    print('[INFO] Start recording...')
    
    # 影像輸入參數
    """
    使用範例
    input_params = [
        {'type': 'camera', 'id': 0},
        {'type': 'rtsp', 'url': 'rtsp://xxx.xxx.xxx.xxx:554/xxx'},
        {'type': 'file', 'path': 'xxx.mp4'},
        #...
    ]
    """
    """
    # 測試用 - 檔案
    input_params = [
        {'type': 'file', 'path': 'data/2022-08-17_15raw.mp4'},
        {'type': 'file', 'path': 'data/PerspectiveTransform.mp4'},
        {'type': 'file', 'path': 'data/TestDrown.mp4'},
    ]
    """
    # 實際執行 - RTSP
    
    input_params = [
        {'type': 'rtsp', 'url': 'rtsp://admin:Admin123!@192.168.0.99/stream1'},
        {'type': 'rtsp', 'url': 'rtsp://admin:Admin123!@192.168.0.98/stream1'},
        {'type': 'rtsp', 'url': 'rtsp://admin:Admin123!@192.168.0.97/stream1'},
    ]
    
    processes = []
    for i, param in enumerate(input_params):
        # 生成檔案名稱
        output_dir = f'{OUTPUT_DIR}/cam{i+1}'

        # 輸出路徑
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_path = os.path.join(output_dir)

        # 創建影像輸入物件
        if param['type'] == 'camera':
            video_input = CameraInput(param['id'])
        elif param['type'] == 'rtsp':
            video_input = RTSPInput(param['url'])
        elif param['type'] == 'file':
            video_input = FileInput(param['path'])
        else:
            raise ValueError('Invalid video input type')

        # 創建進程並開始錄影
        video_recorder = VideoRecorder(i, video_input, output_path)
        video_recorder.start()
        processes.append(video_recorder)
        
    # 等待所有進程結束
    for process in processes:
        process.join()
    
    cv2.destroyAllWindows()
    print('[INFO] All processes stopped.')