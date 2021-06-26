import cv2 as cv
import numpy as np

alpha = 1.0
alpha_max = 500
beta = 0
beta_max = 200
gamma = 1.0
gamma_max = 200
img_original = None
img_corrected = None
img_gamma_corrected = None

def basicLinearTransform():
    global img_original
    global img_corrected
    if img_original is not None:
        res = cv.convertScaleAbs(img_original, alpha=alpha, beta=beta)
        img_corrected = cv.hconcat([img_original, res])
        cv.imshow("Brightness and contrast adjustments", img_corrected)

def gammaCorrection():
    global img_original
    global img_gamma_corrected

    if img_original is not None:
        ## [changing-contrast-brightness-gamma-correction]
        lookUpTable = np.empty((1,256), np.uint8)
        for i in range(256):
            lookUpTable[0,i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)

        res = cv.LUT(img_original, lookUpTable)
        ## [changing-contrast-brightness-gamma-correction]

        img_gamma_corrected = cv.hconcat([img_original, res])
        cv.imshow("Gamma correction", img_gamma_corrected)

def on_linear_transform_alpha_trackbar(val):
    global alpha
    alpha = val / 100
    basicLinearTransform()

def on_linear_transform_beta_trackbar(val):
    global beta
    beta = val - 100
    basicLinearTransform()

def on_gamma_correction_trackbar(val):
    global gamma
    gamma = val / 100
    gammaCorrection()

def white_balance(img):
    lookupTable = np.empty((1,256), np.uint8)
    for i in range(256):
        lookupTable[0,i] = np.clip(pow(i / 255.0, gamma))

def main():
    global img_original
    global img_corrected
    global img_gamma_corrected
    video_capture = cv.VideoCapture("rtsp://control4:inner2sock@192.168.1.70/Streaming/Channels/101")

    # cv.namedWindow('Video', cv.WINDOW_AUTOSIZE)
    cv.namedWindow('Brightness and contrast adjustments', cv.WINDOW_AUTOSIZE)
    cv.namedWindow('Gamma correction', cv.WINDOW_AUTOSIZE)

    alpha_init = int(alpha * 100)
    cv.createTrackbar('Alpha gain (contrast)', 'Brightness and contrast adjustments', alpha_init, alpha_max,
                      on_linear_transform_alpha_trackbar)
    beta_init = beta + 100
    cv.createTrackbar('Beta bias (brightness)', 'Brightness and contrast adjustments', beta_init, beta_max,
                      on_linear_transform_beta_trackbar)
    gamma_init = int(gamma * 100)
    cv.createTrackbar('Gamma correction', 'Gamma correction', gamma_init, gamma_max,
                      on_gamma_correction_trackbar)

    on_linear_transform_alpha_trackbar(alpha_init)
    on_linear_transform_beta_trackbar(beta_init)
    on_gamma_correction_trackbar(gamma_init)

    while True:
        ret, frame = video_capture.read()
        # rgb_frame = frame[:, :, ::-1]
        if frame is not None:
            img_original = cv.resize(frame, (960, 540))
            img_corrected = np.empty((img_original.shape[0], img_original.shape[1] * 2, img_original.shape[2]),
                                     img_original.dtype)
            img_gamma_corrected = np.empty((img_original.shape[0], img_original.shape[1] * 2, img_original.shape[2]),
                                           img_original.dtype)

            img_corrected = cv.hconcat([img_original, img_original])
            img_gamma_corrected = cv.hconcat([img_original, img_original])

            # cv.rectangle(nframe, (100, 100), (300, 300), (0, 0, 255), 2)
            # cv.imshow('Video', nframe)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()

