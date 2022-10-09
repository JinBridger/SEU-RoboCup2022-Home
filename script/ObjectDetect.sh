#! /bin/bash
read_dir(){
    for file in `ls ./images/imageAfterRoI`       #注意此处这是两个反引号，表示运行系统命令
    do
        if [ -d ./images/imageAfterRoI"/"$file ]  #注意此处之间一定要加上空格，否则会报错
        then
            read_dir ./images/imageAfterRoI"/"$file
        else
        	python /home/user_name/nanodet/tools/demo.py image --config ./object_detection/RoboCup416.yml --model model_best.ckpt --path ./images/imageAfterRoI"/"$file --save_result
            echo Processing ./images/imageAfterRoI"/"$file   #在此处处理文件即可
        fi
    done
}

source /home/user_name/anaconda3/bin/activate nanodet
python ./roi_crop/roi_crop.py
read_dir
python ./face_recognition/main.py
echo finish!
