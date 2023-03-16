from app_modules import *
from app_define import *

#####################################################
###             Video Input - start               ###
#####################################################
class VideoInput:
    def __init__(self, input_src):
        self.input_src = input_src

    def read(self):
        raise NotImplementedError()

    def isOpened(self):
        raise NotImplementedError()

class CameraInput(VideoInput):
    def __init__(self, cam_id):
        super().__init__(cam_id)
        self.cap = cv2.VideoCapture(cam_id)

    def read(self):
        return self.cap.read()

    def isOpened(self):
        return self.cap.isOpened()

class RTSPInput(VideoInput):
    def __init__(self, rtsp_url):
        super().__init__(rtsp_url)
        self.cap = cv2.VideoCapture(rtsp_url)

    def read(self):
        return self.cap.read()

    def isOpened(self):
        return self.cap.isOpened()

class FileInput(VideoInput):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.cap = cv2.VideoCapture(file_path)

    def read(self):
        return self.cap.read()

    def isOpened(self):
        return self.cap.isOpened()

###################################################
###             Video Input - end               ###
################## ---/--/--- #####################

###################################################
###         Video Recording - start             ###
###################################################
class VideoRecorder(threading.Thread):
    def __init__(self, cam_index, video_input, output_path):
        super().__init__()
        self.cam_id = cam_index
        self.obj_name = f'Camera {cam_index}'
        self.video_input = video_input
        self.output_path = output_path
        self.fps = None
        self.is_create_window = False
    
        self.start_time = time.time()
        self.current_time = time.time()
        self.record_time = 0
        self.video_writer = None
                
        self.is_stop = False
    
    def create_file(self, frame):
        now = datetime.now()
        date_str = now.strftime('%Y-%m-%d')
        datetime_str = now.strftime('%Y%m%d_%H%M%S')
        file_name = f'raw_{datetime_str}.mp4'
        
        # 輸出路徑
        output_path = os.path.join(self.output_path, date_str)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        file_path = os.path.join(output_path, file_name)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        if self.fps is None: 
            self.fps = self.video_input.cap.get(cv2.CAP_PROP_FPS)
        print(f'[DEBUG] Write path: {file_path}')
        self.video_writer = cv2.VideoWriter(file_path, fourcc, self.fps, (frame.shape[1], frame.shape[0]))
        self.start_time = self.current_time = time.time()
        self.record_time = 0

    def run(self):
        self.start_time = time.time()

        while not self.is_stop:
            # 讀取影像
            ret, frame = self.video_input.read()
            
            if not ret:
                break

            # 初始化 video writer
            self.current_time = time.time()
            if self.video_writer is None: 
                self.printMsg_info(f'[INFO] Create new file')
                self.create_file(frame)

            elif self.video_writer is not None and (self.current_time - self.start_time) >= RECORD_TIME:
                # 關閉之前的檔案
                self.printMsg_info(f'[INFO] RECORD_TIME reach, Creating new file')
                if self.video_writer is not None:
                    self.video_writer.release()

                # 開啟新的檔案
                self.create_file(frame)
                

            # 寫入影像
            self.video_writer.write(frame)
            self.record_time = self.current_time - self.start_time

            # 顯示圖像
            if not self.is_create_window: 
                # 創建一個命名視窗 & 調整視窗大小
                cv2.namedWindow(self.obj_name, cv2.WINDOW_NORMAL)
                cv2.resizeWindow(self.obj_name, int(frame.shape[1]/3), int(frame.shape[0]/3))
                self.is_create_window = True
                
            cv2.imshow(self.obj_name, frame)
            if cv2.waitKey(1) == ord('q'):
                break

        # 釋放資源
        if self.video_writer is not None:
            self.video_writer.release()
        self.video_input.cap.release()
        
    def printMsg_info(self, msg):
        print(f'[INFO ] {self.obj_name} : {msg}') 

    def printMsg_debug(self, msg):
        print(f'[DEBUG] {self.obj_name} : {msg}') 
 
    def printMsg_warn(self, msg):
        print(f'[WARN ] {self.obj_name} : {msg}') 


    def printMsg_error(self, msg):
        print(f'[ERROR] {self.obj_name} : {msg}') 

###################################################
###             Video Input - end               ###
################## ---/--/--- #####################
