import os
import cv2
import time
import argparse
import math
import numpy
import torch
import model.detector
import utils.utils
import time
import socket


# from move import Mover

def getDirectionLetter(dirLeft,dirRight,dirForward, dirBack):
        if dirLeft:
            return 'l'
        if dirForward:
            return 'f'
        if dirRight:
            return 'r'
        if dirBack:
            return 'b'
        
        return 's'
                
    

if __name__ == '__main__':
    # Parse arguments
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='',
                        help='Specify training profile *.data')
    parser.add_argument('--weights', type=str, default='',
                        help='The path of the .pth model to be transformed')
    parser.add_argument('--img', type=str, default='',
                        help='The path of test image')

    opt = parser.parse_args()
    cfg = utils.utils.load_datafile(opt.data)
    
    host = '192.168.217.38'
    port = 5004  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind host address and port together
    server_socket.listen(2)
    conn=None
    conn, address = server_socket.accept()  # accept new connection

    assert os.path.exists(opt.weights), "Please specify the correct model path"
    assert os.path.exists(
        opt.img), "Please specify the correct test image path"

    # Load model
    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    device = torch.device("cpu")
    model = model.detector.Detector(
        cfg["classes"], cfg["anchor_num"], True).to(device)
    model.load_state_dict(torch.load(opt.weights, map_location=device))

    # sets the module in eval node
    model.eval()

    # Capture video through webcam
    cap = cv2.VideoCapture(2)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)
  
    dirLeft, dirRight, dirForward, dirBack=False, False, False, False
    directionLetter='s'
    
    
    start_time = time.time()
    x = 1 # displays the frame rate every 1 second
    counter = 0
    try:
        while True:
            # print('-----------------------------------------------------')
            counter+=1
            fps=0
            if (time.time() - start_time) > x :
                fps= counter / (time.time() - start_time)
                counter = 0
                start_time = time.time()
            
            ret, ori_img = cap.read()
            if ori_img is None:
                continue
            # time.sleep(0.1)
            #draw fps
            cv2.putText(ori_img, "FPS: " + str(fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            res_img = cv2.resize(
                ori_img, (cfg["width"], cfg["height"]), interpolation=cv2.INTER_LINEAR)
            img = res_img.reshape(1, cfg["height"], cfg["width"], 3)
            img = torch.from_numpy(img.transpose(0, 3, 1, 2))
            img = img.to(device).float() / 255.0
            preds = model(img)
            output = utils.utils.handel_preds(preds, cfg, device)
            output_boxes = utils.utils.non_max_suppression(
                output, conf_thres=0.3, iou_thres=0.4)
            LABEL_NAMES = []
            with open(cfg["names"], 'r') as f:
                for line in f.readlines():
                    LABEL_NAMES.append(line.strip())

            h, w, _ = ori_img.shape
            scale_h, scale_w = h / cfg["height"], w / cfg["width"]
            BAreas = []
            centerXpoints = []
            
            left = int(w/3) #427
            right = int((2*w)/3)#mid =853
            #right = 1280
            for box in output_boxes[0]:
                box = box.tolist()

                obj_score = box[4]
                category = LABEL_NAMES[int(box[5])]

                x1, y1 = int(box[0] * scale_w), int(box[1] * scale_h)
                x2, y2 = int(box[2] * scale_w), int(box[3] * scale_h)

                if(category == 'person'):
                    BHeight = math.sqrt((y2 - y1)**2)
                    BWidth = math.sqrt((x2 - x1)**2)

                    BArea = BHeight * BWidth
                    centerX = (BWidth/2) + x1
                    BAreas.append(BArea)
                    centerXpoints.append(centerX)

                #print("h,w:", h, w)
                #print("category ,x1, y1, x2, y2:", category, x1, y1, x2, y2)
                #print("BArea: ", BArea)

                    cv2.rectangle(ori_img, (x1, y1), (x2, y2), (255, 255, 0), 2)

                    cv2.putText(ori_img, '%.2f' % obj_score,
                                (x1, y1 - 5), 0, 0.7, (0, 255, 0), 2)
                    cv2.putText(ori_img, category, (x1, y1 - 25),
                                0, 0.7, (0, 255, 0), 2)
            #print("BAreas:", BAreas)
            

            if (not len(BAreas)): #rotate right
                dirForward=False
            else:   
                maxArea = max(BAreas)
                maxAreaindex = BAreas.index(maxArea)
                centerX = centerXpoints[maxAreaindex]
                print(f"maxArea: {maxArea}\n")                
                dirLeft = (centerX < left)
                dirForward =(centerX <= right and centerX >= left and maxArea < 100000)
                dirRight = (centerX > right )#and centerX < right)
                dirBack = (maxArea > 200000 and centerX <= right and centerX >= left)
            directionLetter=getDirectionLetter(dirLeft,dirRight,dirForward, dirBack)
            # mover.move(directionLetter)

            print("Sending letter: ",directionLetter)
            if(conn is not None):
                conn.send(directionLetter.encode())
                
            print(f"dirLeft: {dirLeft}\ndirRight: {dirRight}\ndirForward: {dirForward}\ndirBack: {dirBack}\n\n")        
           
            
          #  time.sleep(1)
            cv2.imshow("", ori_img)
            if (cv2.waitKey(1) & 0xFF == ord("q")) or (cv2.waitKey(1) == 27):
                break
        
    except KeyboardInterrupt:
            cap.release()
            cv2.destroyAllWindows()
            conn.close()
            # mover.destroyGPIOPins()
