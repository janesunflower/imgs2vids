import os
import cv2
import glob
import numpy as np
import argparse
import yaml

def vids2imgs(config):  # 提取视频中图片 按照每帧提取
    videos = os.listdir(config['vids_root'])  # 返回指定路径下的文件和文件夹列表。
    for video_name in videos:  # 依次读取视频文件
        file_name = video_name.split('.')[0]  # 拆分视频文件名称 ，剔除后缀
        folder_name = config['imgs_root'] + file_name  # 保存图片的上级目录+对应每条视频名称 构成新的目录存放每个视频的
        os.makedirs(folder_name, exist_ok=True)  # 创建存放视频的对应目录

        c = 0  # 计数 统计对应帧号
        vc = cv2.VideoCapture(config['vids_root'] + file_name + config['vid_houzhui'])  # 读入视频文件, '.mp4'
        print(config['vids_root'] + file_name + config['vid_houzhui'])

        while vc.isOpened():  # 判断视频是否打开 返回True或Flase,循环读取视频帧
            rval, frame = vc.read()  # videoCapture.read() 函数，第一个返回值为是否成功获取视频帧，第二个返回值为返回的视频帧：
            pic_path = folder_name + '/'
            if rval:
                cv2.imwrite(pic_path + "%06d" % c + config['img_houzhui'], frame)  # '.png', 存储为图像,保存名为 文件夹名_数字（第几个文件）.jpg
                cv2.waitKey(1)  # waitKey()--这个函数是在一个给定的时间内(单位ms)等待用户按键触发;如果用户没有按下 键,则接续等待(循环)
                c = c + 1
            else:
                break
        vc.release()
        print('save_success' + folder_name)


def imgs2vids(config):
    img_root = config['imgs_root'] + config['vid_name'] + "/"
    vid_save_path = config['imgs_root']  + config['vid_name']  + config['vid_houzhui']
    print(vid_save_path)
    img_len = len(glob.glob(img_root + '*.jpg'))
    print("img_len:", img_len)

    params = config['img2vid']
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    videoWriter = cv2.VideoWriter(vid_save_path, fourcc, params['fps'], (params['w'], params['h']))
    for i in range(params['start_frame'], params['end_frame']):  # 有多少张图片，从编号1到编号2629
        print("frame： ", i)
        img = cv2.imread(img_root + "%06d"%i + config['img_houzhui']) # '.jpg'

        if config['isCrop']:
            cropParams = config['cropImg']
            img = img[cropParams['h1']:cropParams['h2'], cropParams['w1']:cropParams['w2']] # cropped_img = img[0:960, 0:1920]

        if config['isPutText']:
            img = put_text(img, config['putText']['text'])

        videoWriter.write(img)
    videoWriter.release()


def rename_imgs(img_path):
    img_list = os.listdir(img_path)
    img_list.sort()
    l = len(img_list)
    for i in range(l):
        old_name = img_list[i]
        new_name = "%03d" % i + config['img_houzhiu'] # ".png"
        os.rename(os.path.join(img_path, old_name), os.path.join(img_path, new_name))
        print(i)

def put_text(img, text):
    # 调用cv.putText()添加文字
    # text = "10m/s"
    imgcopy = img.copy()
    params = config['putText']
    cv2.putText(imgcopy, text, (params['orgx'], params['orgy']), cv2.FONT_HERSHEY_TRIPLEX, params['fontScale'], (255,0,0), params['thickness']) # 位置，字体，字号，颜色，粗细
    return imgcopy


# 图片裁剪
def crop_imgs(config, imgsave_name):
    img_root = config['imgs_root'] + config['vid_name'] + "/"
    save_img_root = config['imgs_root'] + imgsave_name + '/'

    files = os.listdir(img_root)
    files.sort()
    for file in files:
        print(file)
        img = cv2.imread(img_root + file)
        cropParams = config['cropImg']
        new_img = img[cropParams['h1']:cropParams['h2'], cropParams['w1']:cropParams['w2']] # H， W
        cv2.imwrite(save_img_root + file, new_img)



if __name__ == "__main__":
    # imgs2vids.yaml
    file = open("imgs2vids.yaml", encoding="UTF-8")
    config = yaml.load(file, Loader=yaml.FullLoader)

    # 视频转为图片
    # vids2imgs(config)
    # print("video转imgs完毕！")


    # # 图片转为视频
    imgs2vids(config)
    print("imgs转video成功！")


    # # 重命名图片名字
    # new_img_name = 'fly03'
    # img_path = config['imgs_root'] + new_img_name + '/' # 保存路径
    # rename_imgs(img_path)
    # print("重命名成功", len(os.listdir(img_path)))

    # 裁剪图片
    # img_root = f_save_path + "back02/"
    # save_img_root = f_save_path + "back02_640512/"
    # crop_imgs(img_root, save_img_root, 208, 720, 260, 900)
























