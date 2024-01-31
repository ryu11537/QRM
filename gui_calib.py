#!/usr/bin/env python3

import tkinter as tk
import tkinter.ttk as ttk

from tkinter import filedialog
from tkinter import messagebox
from tkinter import font

import rospy
import os
import time
import shutil
import subprocess
import psutil
import datetime

class CalibMsgBox(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        self.current_path = os.getcwd()

        master.geometry("995x970") # 画面サイズ変更
        master.title("QRM Robot Vision Calibration") # タイトルを指定
        
        self.frame1 = tk.Frame(master,height=300, width=1024, bg="cyan") # フレームの作成
        self.frame1.pack()
        self.frame2 = tk.Frame(master,height=300, width=1024, bg="pale green") # フレームの作成
        self.frame2.pack()
        self.frame3 = tk.Frame(master,height=300, width=1024, bg="orchid1") # フレームの作成
        self.frame3.pack()
        self.frame4 = tk.Frame(master,height=300, width=1024, bg="SteelBlue2") # フレームの作成
        self.frame4.pack()
        self.frame5 = tk.Frame(master,height=300, width=1024, bg="light salmon") # フレームの作成
        self.frame5.pack()

        self.fTyp = [("","*")] # ファイルタイプの指定無し
        
        # カメラソフト画面フレームの定義
        self.subtitle1= tk.Label(self.frame1, text="カメラソフト起動", bg="cyan", font=("MSゴシック", "24", "bold"), fg="black", width="52")
        self.subtitle1.grid(row=0, column=0, columnspan=2, padx=0, pady=0)
 
        self.basler_button = tk.Button(self.frame1, text="Basler製カメラ", bg="white", font=("MSゴシック", "24", "bold"), fg="black", width="24", command=self.select_basler_camera)
        self.basler_button.grid(row=1, column=0, padx=1, pady=10)

        self.omron_button = tk.Button(self.frame1, text="OmronSentech製カメラ", bg="white", font=("MSゴシック", "24", "bold"), fg="black", width="24", command=self.select_omron_camera)
        self.omron_button.grid(row=1, column=1, padx=1, pady=10)

        # キャリブレーション画面フレームの定義
        self.subtitle2= tk.Label(self.frame2, text="初期設定", bg="pale green", font=("MSゴシック", "24", "bold"), fg="black", width="52")
        self.subtitle2.grid(row=0, column=0, columnspan=2, padx=0, pady=0)

        self.create_dir_button = tk.Button(self.frame2, text="設定フォルダ作成", bg="white", font=("MSゴシック", "24", "bold"), fg="black", width="24", command=self.select_create_dir)
        self.create_dir_button.grid(row=1, column=0, padx=1, pady=10)

        self.del_dir_button = tk.Button(self.frame2, text="設定フォルダ削除", bg="white", font=("MSゴシック", "24", "bold"), fg="black", width="24", command=self.select_del_dir)
        self.del_dir_button.grid(row=1, column=1, padx=1, pady=10)

        self.set_dir_button = tk.Button(self.frame2, text="設定フォルダ選択", bg="white", font=("MSゴシック", "24", "bold"), fg="black", width="24", command=self.select_set_dir)
        self.set_dir_button.grid(row=2, column=0, padx=1, pady=10)

        self.chenge_dir_button = tk.Button(self.frame2, text="設定フォルダ修正", bg="white", font=("MSゴシック", "24", "bold"), fg="black", width="24", command=self.select_change_dir)
        self.chenge_dir_button.grid(row=2, column=1, padx=1, pady=10)

        self.subtitle3= tk.Label(self.frame2, text="選択中フォルダ", bg="pale green", font=("MSゴシック", "16", "bold"), fg="black")
        self.subtitle3.grid(row=3, column=0, sticky=tk.E, pady=0)

        self.show_dir = tk.StringVar()
        self.show_setdir = tk.Entry(self.frame2, bg="white", font=("MSゴシック", "10", "bold"), fg="black", width="58", textvariable= self.show_dir)
        self.show_setdir.grid(row=3, column=1, padx=1, pady=10)
        self.show_setdir.config(state='readonly')

        self.subtitle4= tk.Label(self.frame3, text="キャリブレーション", bg="orchid1", font=("MSゴシック", "24", "bold"), fg="black", width="52")
        self.subtitle4.grid(row=0, column=0, columnspan=2, padx=0, pady=0)

        self.camcalib_button = tk.Button(self.frame3, text="カメラキャリブレーション", bg="white", font=("MSゴシック", "24", "bold"), fg="black", width="24", command=self.select_camera_calib)
        self.camcalib_button.grid(row=1, column=0, padx=1, pady=10)

        self.rbcalib_button = tk.Button(self.frame3, text="ロボットキャリブレーション", bg="white", font=("MSゴシック", "24", "bold"), fg="black", width="24", command=self.select_robot_calib)
        self.rbcalib_button.grid(row=1, column=1, padx=1, pady=10)

        self.subtitle5= tk.Label(self.frame3, text="選択中カメラメーカー", bg="orchid1", font=("MSゴシック", "16", "bold"), fg="black")
        self.subtitle5.grid(row=2, column=0, sticky=tk.E, pady=0)

        self.show_cammaker = tk.StringVar()
        self.show_setcammaker = tk.Entry(self.frame3, bg="white", font=("MSゴシック", "10", "bold"), fg="black", width="58", textvariable= self.show_cammaker)
        self.show_setcammaker.grid(row=2, column=1, padx=1, pady=10)
        self.show_setcammaker.config(state='readonly')

        self.subtitle6= tk.Label(self.frame3, text="選択中画像トピック", bg="orchid1", font=("MSゴシック", "16", "bold"), fg="black")
        self.subtitle6.grid(row=4, column=0, sticky=tk.E, pady=0)

        self.show_img = tk.StringVar()
        self.show_setimg = tk.Entry(self.frame3, bg="white", font=("MSゴシック", "10", "bold"), fg="black", width="58", textvariable= self.show_img)
        self.show_setimg.grid(row=4, column=1, padx=1, pady=10)
        self.show_setimg.config(state='readonly')

        self.exposure_button = tk.Button(self.frame3, text="露光時間変更", bg="white", font=("MSゴシック", "24", "bold"), fg="black", width="24", command=self.select_ex_change)
        self.exposure_button.grid(row=5, column=0, padx=5, pady=10)     
    
        # マスター登録画面フレームの定義
        self.subtitle7= tk.Label(self.frame4, text="マスター登録", bg="SteelBlue2", font=("MSゴシック", "24", "bold"), fg="black", width="52")
        self.subtitle7.grid(row=0, column=0, columnspan=2, padx=0, pady=0)

        self.three_hole_button = tk.Button(self.frame4, text="3穴マスター登録", bg="white", font=("MSゴシック", "24", "bold"), fg="black", width="24", command=self.hole_master_reg)
        self.three_hole_button.grid(row=6, column=0, padx=5, pady=10)

        self.akaze_button = tk.Button(self.frame4, text="akazeマスター登録", bg="white", font=("MSゴシック", "24", "bold"), fg="black", width="24", command=None)
        self.akaze_button.grid(row=6, column=1, padx=5, pady=10)

        # データ移行画面フレームの定義
        self.subtitle8= tk.Label(self.frame5, text="PC交換時バックアップデータ移行", bg="light salmon", font=("MSゴシック", "24", "bold"), fg="black", width="52")
        self.subtitle8.grid(row=0, column=0, columnspan=2, padx=0, pady=0)

        self.three_hole_button = tk.Button(self.frame5, text="データ移行ソフト起動", bg="white", font=("MSゴシック", "24", "bold"), fg="black", width="24", command=self.pc_bkup)
        self.three_hole_button.grid(row=7, column=0, padx=(170,0), pady=10)

    # Baslerカメラソフトの起動
    def select_basler_camera(self):
        self.run_cmd('/opt/pylon5/bin/PylonViewerApp')
        self.basler_button["state"] = "normal"
        
    # OmronSentechカメラソフトの起動
    def select_omron_camera(self):
        self.run_cmd('/opt/sentech/bin/StViewer')
        self.omron_button["state"] = "normal"

    # 設定フォルダの作成
    def select_create_dir(self):
        try:
            ret = tk.messagebox.askyesno('確認', '設定フォルダを \n 作成しますか？')
            if ret == True:
                self.close_flg2 = False
                self.dirselect(os.path.expanduser('~')+'/ros_ws/src/tmej_robot_setting', '設定元になるフォルダ(RB名)を選択して下さい')
                source_dir = self.dirname
                idx = source_dir.find("/tmej_robot_setting/")
                source_pkgnm  = source_dir[idx+len("/tmej_robot_setting/"):]
                if len(source_dir) < 1:
                    return
                self.valueinput('設定フォルダ名を入力してください')
                new_dir = os.path.expanduser('~')+'/ros_ws/src/tmej_robot_setting/'+self.input_value
                if self.close_flg2:
                    return
                shutil.copytree(source_dir,new_dir)
                os.chmod(new_dir, 0o777)
                self.run_cmd('grep -rl \'' + source_pkgnm + '\' ' + new_dir + ' | xargs sed -i -e \'s/' + source_pkgnm + '/' + self.input_value+ '/g\'')
                make_dir = os.path.expanduser('~')+'/ros_ws'
                self.run_cmd('gnome-terminal -- bash -c \'cd  ' + make_dir + '; catkin_make; bash\'')
        except Exception as err:
            print(err)
            tk.messagebox.showerror('エラーが発生しました',err)

    # 設定フォルダの削除
    def select_del_dir(self):
        try:
            ret = tk.messagebox.askyesno('確認', '設定フォルダを \n 削除しますか？')
            if ret == True:
                self.dirselect(os.path.expanduser('~')+'/ros_ws/src/tmej_robot_setting', '削除するフォルダを選択して下さい')
                del_dir = self.dirname
                if len(del_dir) < 1:
                    return
                elif del_dir == os.path.expanduser('~')+'/ros_ws/src/tmej_robot_setting' or len(del_dir) < 42:
                    tk.messagebox.showerror('エラーが発生しました','tmej_robot_setting以下のフォルダを選択してください')
                    return
                ret = tk.messagebox.askyesno('確認', '本当に設定フォルダを \n 削除しますか？')
                if ret == True:
                    shutil.rmtree(del_dir)
        except Exception as err:
            print(err)
            tk.messagebox.showerror('エラーが発生しました',err)

    # 設定フォルダの選択
    def select_set_dir(self):
        try:
            self.show_setdir.config(state='normal')
            self.dirselect(os.path.expanduser('~')+'/ros_ws/src/tmej_robot_setting', '設定するフォルダを選択して下さい')
            select_dir = self.dirname
            self.show_dir.set(select_dir)
            self.show_setdir.config(state='readonly')
        except Exception as err:
            print(err)
            tk.messagebox.showerror('エラーが発生しました',err)

    # 設定フォルダの修正
    def select_change_dir(self):
        try:
            ret = tk.messagebox.askyesno('確認', '設定フォルダを \n 修正しますか？')
            if ret == True:
                current_dir = self.show_dir.get()
                if not os.path.isdir(current_dir):
                    tk.messagebox.showerror('エラーが発生しました','存在するフォルダを選択してください')
                    return
                subprocess.call('nautilus ' + str(current_dir), shell=True)
        except Exception as err:
            print(err)
            tk.messagebox.showerror('エラーが発生しました',err)
    
    # カメラキャリブレーションの選択
    def select_camera_calib(self):
        try:
            ret = tk.messagebox.askyesno('確認', 'カメラキャリブレーションを \n 実行しますか？')
            if ret == True:
                self.calibdata_button = tk.Button(self.frame3, text="カメラキャリブレーションファイル移動", bg="white", font=("MSゴシック", "18", "bold"), fg="black", width="32", command=self.move_calibdata)
                self.calibdata_button.grid(row=5, column=1, padx=5, pady=10)       
                self.calibflg = "camera"
                self.show_setcammaker.config(state='normal')
                self.show_cammaker.set('')
                self.show_setcammaker.config(state='readonly')
                self.show_setimg.config(state='normal')
                self.show_img.set('')
                self.show_setimg.config(state='readonly')
                self.close_flg1 = False
                current_dir = self.show_dir.get()
                if not os.path.isdir(current_dir):
                    tk.messagebox.showerror('エラーが発生しました','存在するフォルダを選択してください')
                    return
                data = ["Basler","OmronSentech"]
                self.listselect(data, 'カメラメーカーを選択して下さい')
                cam_selected = self.selected
                if self.close_flg1:
                    return
                data = ["camera1","camera2"]
                self.listselect(data, 'カメラ番号を選択して下さい')
                camno_selected = self.selected
                if self.close_flg1:
                    return
                self.show_setcammaker.config(state='normal')
                self.show_cammaker.set(cam_selected)
                self.show_setcammaker.config(state='readonly') 
                subprocess.call(str(current_dir)+'/cam_open.bash ' + camno_selected+ ' ' + cam_selected , shell=True)
                time.sleep(3)
                data = ['0.044','0.022']
                self.listselect(data, 'チェッカーボード正方形サイズ(m)を選択して下さい')
                bd_selected = self.selected
                if self.close_flg1:
                    return
                topics = rospy.get_published_topics()
                data = []
                for topic in topics:
                    data.append(topic[0])
                self.listselect(data, '生画像トピック(image_raw)を選択して下さい')
                topic_selected = self.selected
                if self.close_flg1:
                    return
                self.show_setimg.config(state='normal')
                self.show_img.set(topic_selected)
                self.show_setimg.config(state='readonly')
                subprocess.call(str(current_dir)+'/camera_calib.bash ' + bd_selected + ' ' + topic_selected , shell=True)
        except Exception as err:
            print(err)
            tk.messagebox.showerror('エラーが発生しました',err)
    
    # ロボットキャリブレーション実行
    def select_robot_calib(self):
        try:
            ret = tk.messagebox.askyesno('確認', 'ロボットキャリブレーションを \n 実行しますか？')
            if ret == True:
                self.calibflg = "robot"
                self.show_setcammaker.config(state='normal')
                self.show_cammaker.set('')
                self.show_setcammaker.config(state='readonly')
                self.show_setimg.config(state='normal')
                self.show_img.set('')
                self.show_setimg.config(state='readonly')
                self.close_flg1 = False
                current_dir = self.show_dir.get()
                if not os.path.isdir(current_dir):
                    tk.messagebox.showerror('エラーが発生しました','存在するフォルダを選択してください')
                    return
                if len(current_dir)<42 :
                    tk.messagebox.showerror('エラーが発生しました','tmej_robot_setting以下のフォルダを選択してください')
                    return
                data = ["Basler","OmronSentech"]
                self.listselect(data, 'カメラメーカーを選択して下さい')
                cam_selected = self.selected
                if self.close_flg1:
                    return
                data = ["camera1","camera2"]
                self.listselect(data, 'カメラ番号を選択して下さい')
                camno_selected = self.selected
                if self.close_flg1:
                    return
                self.show_setcammaker.config(state='normal')
                self.show_cammaker.set(cam_selected)
                self.show_setcammaker.config(state='readonly')             
                subprocess.call(str(current_dir)+'/cam_open.bash ' + camno_selected + ' ' + cam_selected , shell=True)
                time.sleep(3)
                topics = rospy.get_published_topics()
                data = []
                for topic in topics:
                    data.append(topic[0])
                self.listselect(data, '生画像トピック(image_raw)を選択して下さい')
                topic_selected = self.selected
                if self.close_flg1:
                    return
                self.show_setimg.config(state='normal')
                self.show_img.set(topic_selected)
                self.show_setimg.config(state='readonly')
                subprocess.call(str(current_dir)+'/robot_calib.bash '+ camno_selected , shell=True)
        except Exception as err:
            print(err)
            tk.messagebox.showerror('エラーが発生しました',err)

    # 露光時間変更の選択
    def select_ex_change(self):
        ret = tk.messagebox.askyesno('確認', '露光時間を \n 変更しますか？')
        if ret == True:
            self.close_flg2 = False
            current_dir = self.show_dir.get()
            if not os.path.isdir(current_dir):
                tk.messagebox.showerror('エラーが発生しました','存在するフォルダを選択してください')
                return
            cam_selected  = self.show_cammaker.get()
            if len(cam_selected)<1 :
                tk.messagebox.showerror('エラーが発生しました','各キャリブレーションを実行して \n カメラメーカーを選択してください')
                return
            topic_selected = self.show_img.get()
            idx = topic_selected.find("/image_raw")
            dev_selected  = topic_selected[:idx]
            if len(topic_selected)<1 :
                tk.messagebox.showerror('エラーが発生しました','各キャリブレーションを実行して \n 画像トピックを選択してください')
                return
            self.valueinput('露光時間を入力してください')
            exposure_time = self.input_value
            if self.close_flg2:
                return
            subprocess.call(str(current_dir)+'/change_exposure.bash ' + cam_selected + ' ' +  str(exposure_time) + ' ' + dev_selected , shell=True)
        
    # カメラキャリブレーションデータの移動(キャリブレーション実行後表示)
    def move_calibdata(self):
        current_dir = self.show_dir.get()
        if not os.path.isdir(current_dir):
            tk.messagebox.showerror('エラーが発生しました','存在するフォルダを選択してください')
            return
        self.close_flg1 = False
        calib_file ='/tmp/calibrationdata.tar.gz'
        if not os.path.isfile(calib_file):
            tk.messagebox.showerror('エラーが発生しました','キャリブレーション結果が存在しません。 \n /tmp/calibrationdata.tar.gzを確認してください')
            return
        data = ["camera1","camera2"]
        self.listselect(data, 'カメラ番号を選択して下さい')
        camno_selected = self.selected
        if self.close_flg1:
            return
        date = datetime.datetime.now()
        current_date = str(date.year) + '_' + str(date.month) + '_' + str(date.day)
        camera_calib_dir = os.path.expanduser('~') + '/camera_calib/' + current_date + '/' + camno_selected 
        os.makedirs(camera_calib_dir, exist_ok=True)
        shutil.copyfile('/tmp/calibrationdata.tar.gz', camera_calib_dir + '/calibrationdata.tar.gz')
        self.run_cmd('gnome-terminal -- bash -c \'cd  ' + camera_calib_dir + '; tar -xvzf calibrationdata.tar.gz; sleep 6; exit; bash\'')
        time.sleep(3)
        move_calib_dir = current_dir + "/params/camera/" + camno_selected
        ret = tk.messagebox.askyesno('確認', 'キャリブレーションファイルost.yamlを \n' + move_calib_dir + "に移動しますか?")
        if ret == True:
            if camno_selected == "camera1":
                ost_name = 'ost1.yaml'
            elif camno_selected == "camera2":
                ost_name = 'ost2.yaml'
            else:
                ost_name = 'ost1.yaml'
            if not os.path.isdir(move_calib_dir):
                tk.messagebox.showerror('エラーが発生しました','移動先にフォルダが存在しません')
                return
            shutil.copyfile(camera_calib_dir + '/ost.yaml', move_calib_dir + '/' + ost_name)
            subprocess.call('nautilus ' + str(move_calib_dir), shell=True)
    
    # 3穴マスター登録ソフトの起動
    def hole_master_reg(self):
        ret = tk.messagebox.askyesno('確認', '3穴マスター登録ソフトを \n 起動しますか？')
        if ret == True:
            self.run_cmd('gnome-terminal -- bash -c \'roscore; bash\'')
            subprocess.call('rosrun tmej_qrm_robot_vision hole_master_reg.py', shell=True)

    # バックアップデータ移行ソフトの起動
    def pc_bkup(self):
        ret = tk.messagebox.askyesno('確認', 'バックアップデータ移行ソフトを \n 起動しますか？')
        if ret == True:
            self.run_cmd('gnome-terminal -- bash -c \'python3 /home/tmej/ros_ws/src/tmej_qrm_robot_vision_akaze/scripts/qrm_setup_files/pc_bkup.py; bash\'')

    # subprocessの実行
    def run_cmd(self,cmd):
        try:
            run_result = subprocess.run(cmd, shell=True)
        except Exception as err:
            print(err)
            tk.messagebox.showerror('エラーが発生しました',err)    

    # リストを選択する
    def listselect(self, data,title):
        self.selected = ''
    
        self.sub_win1 = tk.Toplevel()
        self.sub_win1.protocol("WM_DELETE_WINDOW", self.closefunc1)
    
        self.sub_win1.geometry('800x500')
        self.sub_win1.title(title+"(ダブルクリック)")
    
        frame = tk.Frame(self.sub_win1)
    
        width = max(max([len(dat) for dat in data]) if len(data)>0 else 0, 100)
        self.listbox = tk.Listbox(frame, height = 30, width=width)
        for i, dat in enumerate(data):
            self.listbox.insert(i,dat)
    
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.listbox.yview)
    
        self.listbox['yscrollcommand']=scrollbar.set
    
        frame.pack(padx=10, pady=20)
        self.listbox.pack(side='left')
        scrollbar.pack(side='right', fill='both')
    
        self.listbox.bind('<Double-1>', self.select1)
    
        self.sub_win1.mainloop()
        self.sub_win1.destroy()

    # 値を入力する
    def valueinput(self, title):
        self.sub_win2 = tk.Toplevel()
        self.sub_win2.protocol("WM_DELETE_WINDOW", self.closefunc2)
        self.sub_win2.title(title) # タイトルを変更

        self.sub_win2.geometry('450x200')
        self.entry_value = tk.Entry(self.sub_win2, font=("MSゴシック", "20"), width="24")
        self.entry_value.grid(row=0, columnspan=2, column=0, padx=40, pady=40)

        self.detect_button = tk.Button(self.sub_win2, text="決定", bg="white", font=("MSゴシック", "20", "bold"), fg="black",command=self.select2)
        self.detect_button.grid(row=1, column=0, padx=10, pady=5)
        self.detect_button = tk.Button(self.sub_win2, text="閉じる", bg="white", font=("MSゴシック", "20", "bold"), fg="black",command=self.closefunc2)
        self.detect_button.grid(row=1, column=1, padx=10, pady=5)
        
        self.sub_win2.mainloop()
        self.sub_win2.destroy()

    def fileselect(self, path, title):
        if not os.path.isdir(path ):
            path  = "~/"
        self.sub_win3 = tk.Toplevel()
        self.sub_win3.withdraw()
        self.filename = filedialog.askopenfilename(initialdir=path, title=title, filetypes=[("yaml file", "*.yaml")])

    def dirselect(self, path, title):
        if not os.path.isdir(path ):
            path  = "~/"
        self.sub_win4 = tk.Toplevel()
        self.sub_win4.withdraw()
        self.dirname = filedialog.askdirectory(initialdir=path, title=title)
        
    def select1(self, vent):
        ind = self.listbox.curselection()
        self.selected = self.listbox.get(ind)
        self.sub_win1.quit()

    def closefunc(self):
        self.close_flg = True
        self.sub_win.quit()

    def closefunc1(self):
        self.close_flg1 = True
        self.sub_win1.quit()

    def select2(self):
        self.input_value = self.entry_value.get()
        self.sub_win2.quit()

    def closefunc2(self):
        self.close_flg2 = True
        self.sub_win2.quit()

if __name__ == '__main__':
    # Tkインスタンスを作成
    root = tk.Tk()
    # フレームを作成する
    app = CalibMsgBox(master=root)
    # 格納したTkインスタンスのmainloopで画面を起こす
    app.mainloop()
