import os #这个是用来加载文件
import sys #这个包用来推出程序
import random #这个包用来生成随机数
# PyQt5是一个用于创建图形用户界面的Python库
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class DesktopPet(QWidget):
    def __init__(self, parent=None, **kwargs):
        # 在这里初始化你的宠物桌面应用程序
        super(DesktopPet, self).__init__(parent)
        self.is_follow_mouse = False
        self.role = 'character_2'  # 定义宠物角色
        # 窗体初始化函数
        self.init()
        # 托盘初始化函数
        self.initPall()
        # 宠物静态gif图加载函数
        self.initPetImage()
        # 宠物正常待机，实现随机切换动作函数
        self.petNormalAction()
        

    # 窗体初始化
    def init(self):
        # 初始化
        # 设置窗口属性:窗口无标题栏且固定在最前面
        # FrameWindowHint:无边框窗口
        # WindowStaysOnTopHint: 窗口总显示在最上面
        # SubWindow: 新窗口部件是一个子窗口，而无论窗口部件是否有父窗口部件
        # https://blog.csdn.net/kaida1234/article/details/79863146
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        # setAutoFillBackground(True)表示的是自动填充背景,False为透明背景
        self.setAutoFillBackground(False)
        # 窗口透明，窗体空间不透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 重绘组件、刷新
        self.repaint()
   
   # 托盘初始化
    def initPall(self):
        # 导入托盘图标
        icons = os.path.join(os.path.dirname(__file__), 'resource','icons','icon.png')
        # 设置右键显示最小化的菜单
        #菜单退出，点击后调用quit函数
        quit_action = QAction('告别', self, triggered=self.quit)
        # 设置这个点击选项的图片
        quit_action.setIcon(QIcon(icons))
        # 在菜单项中显示，点击后调用showing 函数
        showing = QAction('出现', self, triggered=self.showwin)
        #新建一个菜单项控件
        self.tray_icon_menu = QMenu(self)
        # 在菜单栏添加一个无子菜单的菜单项 “退出” 以及 “显示”
        self.tray_icon_menu.addAction(quit_action)
        self.tray_icon_menu.addAction(showing)
        # QsystemTrayIcon是一个系统托盘图标类,使用它为应用程序在系统托盘中提供一个图标
        self.tray_icon = QSystemTrayIcon(self)
        # 设置托盘图标
        self.tray_icon.setIcon(QIcon(icons))
        # 设置托盘图标的菜单
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        # 展示托盘图标
        self.tray_icon.show()
    
    def quit(self):
        # 退出应用程序
        self.close()
        sys.exit()

    def showwin(self):
        self.setWindowOpacity(1.0)  # 设置窗口不透明

    def initPetImage(self):
        # # 对话框定义
        # self.talkLabel = QLabel(self)
        # # 设置对话框的样式
        # self.talkLabel.setStyleSheet("font:15pt '楷体';border-width: 1px;color:blue;")
        # 定义显示图片的部分
        self.image = QLabel(self)
        # QMovie是一个可以存放动态视频的类，一般是配合QLabel使用的,可以用来存放GIF动态图
        movie = os.path.join(os.path.dirname(__file__), 'resource', self.role, 'show_up', 'show.gif')
        self.movie = QMovie(movie)
        # 设置标签大小
        self.movie.setScaledSize(QSize(500, 500))
        # Qmovie在定义的image中显示
        self.image.setMovie(self.movie)
        self.movie.start()
        self.resize(400, 400)  # 设置窗口大小
        
        # 展示图片
        self.show()

        # 将宠物正常待机状态的动图放入pet1中（只包含GIF文件）
        normal_dir = os.path.join(os.path.dirname(__file__), "resource", self.role, "normal")
        self.pet1 = [os.path.join(normal_dir, f) for f in os.listdir(normal_dir) if f.lower().endswith('.gif')]

    def petNormalAction(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.randonmPetAct)
        self.timer.start(3000)  # 每隔1秒切换一次图片
        self.condition = 0  # 用于判断是否跟随鼠标移动

    def randonmPetAct(self):
        if self.condition == 0:
            # 如果鼠标没有跟随移动
            # 随机选择一张图片
            self.movie = QMovie(random.choice(self.pet1))
            # 设置图片
            self.movie.setScaledSize(QSize(500, 500))
            # 把动画添加到标签中
            self.image.setMovie(self.movie)
            # 启动动画
            self.movie.start()

    def mousePressEvent(self, event): # 鼠标按下事件
        self.condition = 1
        # 鼠标按下事件
        if event.button() == Qt.LeftButton:
            # 如果鼠标左键按下，获取鼠标位置
            self.is_follow_mouse = True
        self.mouse_drag_pos = event.globalPos() - self.pos()
        event.accept()
        self.setCursor(Qt.OpenHandCursor)  # 鼠标按下时，设置鼠标形状为手型
    
    def mouseMoveEvent(self, event): # 鼠标移动事件
        if Qt.LeftButton and self.is_follow_mouse:
            # 如果鼠标左键按下并且跟随鼠标移动
            self.move(event.globalPos() - self.mouse_drag_pos)
        event.accept()

    def mouseReleaseEvent(self, event): # 鼠标释放事件
        self.is_follow_mouse = False
        self.setCursor(Qt.ClosedHandCursor) # 鼠标释放时，设置鼠标形状为箭头


    def enterEvent(self, event):
        # 鼠标进入事件
        # 鼠标进入时，设置鼠标形状为手型
        self.setCursor(Qt.ClosedHandCursor)
    """
    Qt.PointingHandCursor   指向手            Qt.WaitCursor  旋转的圆圈
    ArrowCursor   正常箭头                 Qt.ForbiddenCursor 红色禁止圈
    Qt.BusyCursor      箭头+旋转的圈      Qt.WhatsThisCursor   箭头+问号
    Qt.CrossCursor      十字              Qt.SizeAllCursor    箭头十字
    Qt.UpArrowCursor 向上的箭头            Qt.SizeBDiagCursor  斜向上双箭头
    Qt.IBeamCursor   I形状                 Qt.SizeFDiagCursor  斜向下双箭头
    Qt.SizeHorCursor  水平双向箭头          Qt.SizeVerCursor  竖直双向箭头
    Qt.SplitHCursor                        Qt.SplitVCursor  
    Qt.ClosedHandCursor   非指向手          Qt.OpenHandCursor  展开手
    """

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        # 定义菜单项
        quit_action = menu.addAction('告别')
        hide_action = menu.addAction('收纳')
        # 使用exec_方法显示菜单。从鼠标右键事件对象中获得当前坐标。
        # mapToGlobal()方法把当前组件的相对坐标转换为窗口（window）
        action = menu.exec_(self.mapToGlobal(event.pos()))
        # 如果点击了退出菜单项
        if action == quit_action:
            self.quit()
        elif action == hide_action:
            # 如果点击了隐藏
            self.setWindowOpacity(0.0)

# 主代码
if __name__ == "__main__":
    # 创建一个应用程序对象,对象名为app
    # 所有的PyQt5应用必须创建一个应用（Application）对象。sys.argv参数是一个来自命令行的参数列表。
    app = QApplication(sys.argv)
    #窗口组件初始化
    # 创建了一个名为DesktopPet的窗口类的事例
    pet = DesktopPet()
     # 1. 进入时间循环；
    # 2. wait，直到响应app可能的输入；
    # 3. QT接收和处理用户及系统交代的事件（消息），并传递到各个窗口；
    # 4. 程序遇到exit()退出时，机会返回exec()的值。
    sys.exit(app.exec_())
