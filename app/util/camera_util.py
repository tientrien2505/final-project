import subprocess as sp
import numpy as np
import cv2


def gen_frames(url, rtsp_transport='tcp'):
    # rtsp_transport = 'tcp+udp'
    command = ['ffmpeg',
               '-rtsp_transport', rtsp_transport,
               # '-i', '/dev/video0',
               '-i', url,
               '-f', 'image2pipe',
               '-r', '24',
               '-s', '640x480',
               '-pix_fmt', 'bgr24',
               '-vcodec', 'rawvideo', '-']

    pipe = sp.Popen(command, stdout=sp.PIPE)
    while True:
        raw_image = pipe.stdout.read(640*480*3)
        if raw_image is not None:
            if len(raw_image) > 0:
                frame = np.fromstring(raw_image, dtype='uint8')
                frame = frame.reshape((480, 640, 3))
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                break
        else:
            break


