import cv2
import os
import signal
import time
import _twilio
import sys
import led
from edge_impulse_linux.image import ImageImpulseRunner
led.setup()
sid = 'Enter the sid here'
token = 'Enter the token credential here'
runner, show_camera = None, None
count = 0
red,green = 14, 15
def now():
    return round(time.time() * 1000)
def sigint_handler(sig, frame):
    print('Interrupted')
    if (runner):runner.stop()
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)
def main():
    try:
        global count
        led.running()
        dir_path = 'Model directory here'
        model = 'modelfile.eim'
        modelfile = os.path.join(dir_path, model)
        print('MODEL: ' + modelfile)
        with ImageImpulseRunner(modelfile) as runner:
            try:
                model_info = runner.init()
                print('Loaded runner for "' + model_info['project']['owner'] + ' / ' + model_info['project']['name'] + '"')
                labels = model_info['model_parameters']['labels']
                camera = cv2.VideoCapture(0)
                ret = camera.read()[0]
                if ret:
                    backendName = camera.getBackendName()
                    w = camera.get(3)
                    h = camera.get(4)
                    print("Camera %s (%s x %s) in port %s selected." %(backendName,h,w, 0))
                    camera.release()
                else:raise Exception("Couldn't initialize selected camera.")
                next_frame = 0 # limit to ~10 fps here
                for res, img in runner.classifier(0):
                    if (next_frame > now()):
                        time.sleep((next_frame - now()) / 1000)
                    # print('classification runner response', res)
                    if "classification" in res["result"].keys():
                        print('Result (%d ms.) ' % (res['timing']['dsp'] + res['timing']['classification']), end='')
                        for label in labels:
                            score = res['result']['classification'][label]
                            print('%s: %.2f\t' % (label, score), end='')
                        print('', flush=True)
                    elif "bounding_boxes" in res["result"].keys():
                        print('Found %d bounding boxes (%d ms.)' % (len(res["result"]["bounding_boxes"]), res['timing']['dsp'] + res['timing']['classification']))
                        for bb in res["result"]["bounding_boxes"]:
                            print('\t%s (%.2f): x=%d y=%d w=%d h=%d' % (bb['label'], bb['value'], bb['x'], bb['y'], bb['width'], bb['height']))
                            #img = cv2.rectangle(img, (bb['x'], bb['y']), (bb['x'] + bb['width'], bb['y'] + bb['height']), (255, 0, 0), 1)
                            led.running()

                            mylist = list(bb.items())
                            name = mylist[1][1]
                            score = mylist[2][1]
                            if name == 'Monkey' and score > 0.6:
                                count = count + 1
                                print(count)
                                if count == 3:
                                    _twilio.notify(sid,token)
                                    led.detected()
                                    count = 0
                    if (show_camera):
                        #cv2.imshow('SPOTMONKEY', img)
                        if cv2.waitKey(1) == ord('q'):break
                    next_frame = now() + 100
            finally:
                if (runner):runner.stop()
    except Exception as e:
        print(e)
if __name__ == "__main__":
   main()
