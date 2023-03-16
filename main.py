from app_modules import *
from app_functions import *
from app_define import *

if __name__ == '__main__':
    print('[INFO] Start recording...')
    
    # 影像輸入參數
    """
    input_params = [
        {'type': 'camera', 'id': 0},
        {'type': 'rtsp', 'url': 'rtsp://xxx.xxx.xxx.xxx:554/xxx'},
        {'type': 'file', 'path': 'xxx.mp4'},
        #...
    ]
    """
    input_params = [
        {'type': 'file', 'path': 'data/2022-08-17_15raw.mp4'},
        {'type': 'file', 'path': 'data/PerspectiveTransform.mp4'},
        {'type': 'file', 'path': 'data/TestDrown.mp4'},
    ]
    processes = []
    
    for i, param in enumerate(input_params):
        # 生成檔案名稱
        now = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = f'{OUTPUT_DIR}/cam{i+1}'
        filename = f'raw_{now}.mp4'

        # 輸出路徑
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_path = os.path.join(output_dir, filename)

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