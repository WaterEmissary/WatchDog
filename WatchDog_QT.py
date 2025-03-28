import os
import sys
import time
import shlex
import signal
import shutil
import psutil
import pickle
import tempfile
import pythoncom
import webbrowser
import threading
import subprocess
import win32com.client
from datetime import datetime

from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem, QFileDialog, QSystemTrayIcon, QMenu, \
    QHeaderView, QMessageBox, QLabel, QWidgetAction
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QTimer, Qt

from w_main import Ui_MainWindow    # pyside6-uic .\watchdog_main.ui -o .\w_main.py
from ps_dialog import Ui_Dialog     # pyside6-uic .\process_setup.ui -o .\ps_dialog.py
# pyinstaller -w -F -i ./ico.png --add-data "ico.png;." -n WatchDog.exe .\WatchDog_QT.py

# todo: 右键启动看门狗和禁止未正确显示, 后台启动无法正常拉起程序

DEFAULT_CONFIG = {
    'AUTO_HIDDEN': False,
    'MEM_UNIT': 0,
    'FLUSH_TIME': 0.5,
    'LISTENING': {},
    'REOPEN_OPT': 1,
    'START_WAY': 1,
    'FRPC_PATH': ''
}
MEM_UNIT_LIST = ['MB', 'GB']
REOPEN_LIST = ['无操作', '重启软件']
START_WAY = ['cmd', 'powershell']
# 临时文件锁路径
temp_file_path = os.path.join(tempfile.gettempdir(), ".mydog")

# 获取启动文件夹路径，并定义快捷方式文件的路径
startup_path = os.path.join(os.getenv("APPDATA"), r"Microsoft\Windows\Start Menu\Programs\Startup", "WatchDog.lnk")
# 配置文件路径
config_path = os.path.join(os.path.expanduser("~"), '.watchdog_config')
# 配置文件读写锁
config_lock = threading.Lock()

version_log = [['v1.1', '正式版'],
               ['v1.2', '修改关闭按钮为缩小而不是退出'],
               ['v1.3', '只能选择可执行文件监测, 可以自己设置开机自启, 配置文件生成在用户目录下, 窗口大小可以拉伸'],
               ['v1.31', '修复了若干BUG， 优化了用户体验'],['v1.32', '修改配置文件格式, 修改软件图标'],
               ['v1.4', '添加了浏览功能，一键跳转到软件目录'], ['v1.41', '修改浏览为打开工作目录'],
               ['v1.5', '添加了移除前询问功能'], ['v1.6', "添加重复打开相关功能, 添加单进程右键菜单"],
               ['v1.7', '修复了在某些情况下无法正常拉起进程的bug'],
               ['v1.8', '添加了排序功能, 添加了自动创建启动脚本功能'],
               ['v1.9', '更改启动功能到WMI中, 添加了对powershell支持'],
               ['v1.91', '添加了复制启动命令的功能, 修改了保存逻辑'],
               ['v1.10.1', '每次启动前都会清除win32com的缓存文件'],
               ['v1.11.0', '添加了frpc编辑、启动服务页功能, 修复了移除时名字显示错误的问题']]

# WMI控制程序
class WMI:
    def __init__(self, flush_time=0.1, qt=None):
        self.execution = False
        self.sleep_time = flush_time
        self.processes_dict = {}
        self.run_time_dict = {}
        self.system_usage = {'cpu_percent': 0.0, 'memory_percent': 0.0}
        self.qt = qt
        threading.Thread(target=self.get_processes, daemon=True).start()
        threading.Thread(target=self.get_system_usage, daemon=True).start()
        threading.Thread(target=self.wmi_watch_dog, daemon=True).start()

    # 获取系统运行状态
    def get_system_usage(self):
        while True:
            try:
                # 获取 CPU 占用百分比
                self.system_usage['cpu_percent'] = round(psutil.cpu_percent(interval=1), 1)
            except Exception as e:
                self.system_usage['cpu_percent'] = 0
            try:
                # 获取内存占用百分比
                self.system_usage['memory_percent'] = round(psutil.virtual_memory().percent, 1)
            except Exception as e:
                self.system_usage['memory_percent'] = 0
            time.sleep(self.sleep_time)

    # 获取所有进程方法, 转换成字典
    def get_processes(self):
        while True:
            pythoncom.CoInitialize()  # 初始化 COM 库
            wmi = win32com.client.Dispatch("WbemScripting.SWbemLocator")
            wmi_service = wmi.ConnectServer(".", "root\\cimv2")
            # 获取所有进程信息
            processes = wmi_service.ExecQuery("SELECT * FROM Win32_PerfFormattedData_PerfProc_Process")
            processes_32 = wmi_service.ExecQuery(f"SELECT * FROM Win32_Process")
            self.processes_dict = {process.Name : process for process in processes}
            self.run_time_dict = {p.ProcessID: p.CreationDate for p in processes_32}
            pythoncom.CoUninitialize()  # 卸载 COM 库
            time.sleep(self.sleep_time)

    # wmi启动
    def wmi_watch_dog(self):
        while True:
            # 获取在监听的程序列表
            self.qt.load_config()
            listening = self.qt.config.get('LISTENING')
            self.qt.process_list = []
            # 遍历存储的进程, 从实时进程列表中获取对应的数据
            for index, (name, info) in enumerate(listening.items()):
                # 初始化数据
                process = dict(
                    id=index,
                    use_listen=info.get('use_listen'),
                    other_name=info.get('other_name'),
                    exe_path=info.get('exe_path'),
                    work_dir=info.get('work_dir'),
                    arguments=info.get('arguments'),
                    hidden=info.get('hidden'),
                    url=info.get('url'),
                    run_status=False,
                    pid='--',
                    name='--',
                    command_line='--',
                    thread_count='--',
                    cpu_percent='--',
                    memory_usage='--',
                    visual_memory='--',
                    running_time='--',
                )
                if self.check_process(name):  # 进程存在, 更新数据
                    process['run_status'] = True
                    process.update(self.optimize_process_data(name, self.qt.config.get('MEM_UNIT')))

                if process.get('use_listen') and self.execution is False:  # 如果进程启用监听状态, 并且不在执行状态
                    if self.processes_dict:  # 至少已经检查完一次进程状态
                        if process.get('run_status'):  # 如果进程在运行, 不做任何操作
                            pass
                        else:  # 进程不存在, 启动
                            # self.start_process(process)
                            self.start_process(process)
                            # time.sleep(1)

                self.qt.process_list.append(process)
                self.qt.update_table_row(process)
            time.sleep(self.qt.config.get('FLUSH_TIME'))

    # 将进程对象转换成实际的数据
    def optimize_process_data(self, process_name, mem_unit=0):
        process = self.processes_dict.get(process_name.split('.')[0], None)
        if process:
            process_dict = dict()
            process_dict["pid"] = str(process.IDProcess)  # 进程ID
            process_dict["name"] = process.Name  # 进程名称（软件名）
            # process_dict["exe_path"] = process.ExecutablePath  # 进程可执行文件路径
            # process_dict["command_line"] = process.CommandLine  # 进程启动命令行参数
            process_dict["thread_count"] = str(process.ThreadCount)  # 子线程数量
            process_dict["cpu_percent"] = f"{process.PercentProcessorTime} %" # CPU百分比

            # 占用运行内存
            process_dict['memory_usage'] = f"{int(process.WorkingSet) /(1024 ** (mem_unit+2) ):.2f} {'MB' if mem_unit == 0 else 'GB'}"
            # process_dict['visual_memory'] = f"{int(process.VirtualBytes) /(1024 ** (mem_unit+2) ):.2f} {'MB' if mem_unit == 0 else 'GB'}"
            # process_dict['memory'] = f"{process_dict['memory_usage']} / {process_dict['visual_memory']} {'MB' if mem_unit == 0 else 'GB'}"

            run_time = self.run_time_dict.get(process.IDProcess)
            if run_time:
                create_time = datetime.strptime(run_time.split('.')[0], '%Y%m%d%H%M%S')
                run_time = datetime.now() - create_time
                hours, remainder = divmod(run_time.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                process_dict['running_time'] = f"{run_time.days}:{hours}:{minutes}:{seconds}"
            return process_dict

    # 检查进程是否存在
    def check_process(self, process_name):
        return process_name.split('.')[0] in list(self.processes_dict.keys())

    # 启动进程任务流
    def start_process(self, process):
        def thread_run(command, args):
            self.execution = True
            if self.qt.config.get('START_WAY') == 0:
                self._start_process(command, args)
            elif self.qt.config.get('START_WAY') == 1:
                self._start_process_powershell(command, args)
            time.sleep(3)
            self.execution = False

        command, args = self._create_command(process, self.qt.config.get('START_WAY'))
        if self.execution is True:
            return
        threading.Thread(target=thread_run, args=(command, args,)).start()

    # 创建启动命令
    def _create_command(self, process, way):
        if way == 0:
            exe_path = process.get('exe_path')
            work_dir = process.get('work_dir')
            if not work_dir:
                work_dir = None
            arguments = process.get('arguments')
            hidden = process.get('hidden')

            program_command = f'"{exe_path}" {arguments}'
            command = f'cmd.exe /c start {"/b " if hidden else ""} "" {program_command}'
            print(command)
            return command, work_dir
        elif way == 1:
            exe_path = process.get('exe_path')
            work_dir = process.get('work_dir')
            if not work_dir:
                work_dir = None
            arguments = process.get('arguments')
            hidden = process.get('hidden')

            # 使用 shlex.quote() 安全地转义参数，防止命令注入
            quoted_exe_path = shlex.quote(exe_path)

            # 构建 PowerShell 命令
            powershell_command = [
                "Start-Process",
                "-FilePath", quoted_exe_path,
            ]
            # 如果有参数,再传参数
            if arguments:
                arguments_list = arguments.split()
                powershell_command.append("-ArgumentList")
                arg_str = ','.join(f"'{a}'" for a in arguments_list)
                powershell_command.append(f"@({arg_str})")

            if work_dir:
                powershell_command.extend(["-WorkingDirectory", shlex.quote(work_dir)])

            if hidden:
                powershell_command.extend(["-WindowStyle", "Hidden"])

            command_arg = " ".join(powershell_command)
            command = f'powershell.exe -NoProfile -Command "{command_arg}"'
            print(command)  # 打印最终执行的命令，方便调试
            return command, hidden

    # 启动进程
    def _start_process(self, command, work_dir):
        subprocess.Popen(command, shell=True, cwd=work_dir)

    # 使用powershell启动
    def _start_process_powershell(self, command, hidden):
        """使用 PowerShell 启动进程，可控制是否隐藏窗口。"""
        try:
            subprocess.Popen(command,
                             creationflags=subprocess.CREATE_NO_WINDOW if hidden else 0)  # powershell本身窗口也隐藏
        except FileNotFoundError:
            print(f"Error: PowerShell not found.")
        except subprocess.SubprocessError as e:
            print(f"Error executing command: {e}")

    # 停止进程任务流
    def stop_process(self, process):
        def thread_run():
            self.execution = True
            self._stop_process(process)
            time.sleep(3)
            self.execution = False

        if self.execution is True:
            return
        threading.Thread(target=thread_run).start()

    # 停止进程
    @staticmethod
    def _stop_process(process):
        pid = process.get('pid')
        if pid.isdigit():
            os.kill(int(pid), signal.SIGTERM)
        else:
            pass

    # 重启进程任务流
    def restart_process(self, process):
        def thread_run():
            self.execution = True
            self._stop_process(process)
            time.sleep(1.5)
            self.execution = False
            self.start_process(process)
            time.sleep(3)
            self.execution = False

        if self.execution is True:
            return
        threading.Thread(target=thread_run).start()

# QT主界面
class WatchDogQT:
    def __init__(self):
        self.init_temp_file()

        self.app = QApplication(sys.argv)
        self.win = QMainWindow()
        self.win.closeEvent = self.dog_closeEvent
        self.dialog = None
        self.ui = Ui_MainWindow()
        self.dialog_ui = Ui_Dialog()
        self.ui.setupUi(self.win)

        self.init_icon()

        self.app.setWindowIcon(self.icon)

        # self.win.setFixedSize(640, 330)
        self.win.setWindowTitle('WatchDog')
        self.win.setWindowIcon(self.icon)

        self.config = {}
        self.process_list = []
        self.AUTO_START = os.path.exists(startup_path)

        self._init()
        self.function_init()
        self.init_tray()

        self.wmi = WMI(qt=self)

        self.flush_data()

        self.timer = QTimer()
        self.timer.setInterval(self.config.get('FLUSH_TIME')*1000)
        self.timer.timeout.connect(self.flush_data)
        self.timer.start()

        if self.config.get("AUTO_HIDDEN"):
            self.win.hide()
        else:
            self.win.show()

        self.app.aboutToQuit.connect(self.before_exit)

    # 初始化图标
    def init_icon(self):
        # 判断是否是打包后的应用
        if getattr(sys, 'frozen', False):
            # 如果是打包后的应用，从 sys._MEIPASS 获取资源文件路径
            icon_path = os.path.join(sys._MEIPASS, 'ico.png')
        else:
            # 如果是开发环境，直接使用当前目录的图标文件
            icon_path = 'ico.png'

        self.icon = QIcon(icon_path)

    # 覆盖原来的关闭窗口方法
    def dog_closeEvent(self, event):
        self.win.hide()
        event.ignore()  # 阻止真正的关闭

    # 临时文件初始化
    def init_temp_file(self):
        self.temp_file_handle = open(temp_file_path, "w")

    # 开机自启
    def set_start_up(self):
        try:
            # 获取当前文件路径
            if getattr(sys, 'frozen', False):  # 检查是否为打包后的可执行文件
                current_path = os.path.abspath(sys.executable)
            else:
                current_path = os.path.abspath(__file__)

            # 创建快捷方式
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortcut(startup_path)
            shortcut.TargetPath = current_path  # 目标路径
            shortcut.WorkingDirectory = os.path.dirname(current_path)  # 工作目录
            shortcut.IconLocation = current_path  # 图标路径
            shortcut.save()  # 保存快捷方式
            self.show_message("开机自启设置成功")
            self.AUTO_START = True
        except Exception as e:
            self.show_message(f"开机自启设置失败{str(e)}", level='alarm')

    # 取消开机自启
    def un_set_start_up(self):
        try:
            # 检查快捷方式文件是否存在，存在则删除
            os.remove(startup_path)
            self.show_message("开机自启取消成功")
            self.AUTO_START = False
        except Exception as e:
            self.show_message(f"开机自启设置失败{str(e)}", level='alarm')

    # 创建开机计划任务脚本
    def create_start_script(self):
        if os.path.exists("./start_dog.bat"):
            self.show_message("脚本已存在, 请勿重复创建!", level='alarm')
        else:
            with open("./start_dog.bat", "w", encoding='utf-8') as f:
                f.write(f'''@echo off\nstart "" "{os.path.join(os.getcwd(), 'WatchDog.exe')}"''')
            self.show_message("脚本已在当前目录创建成功,如需移动请自行修改")

    # QT_切换开机自启状态
    def switch_start_up(self):
        if os.path.exists(startup_path):
            self.un_set_start_up()
        else:
            self.set_start_up()

    # 界面初始化
    def _init(self):
        # 设置默认第0页
        self.ui.stackedWidget.setCurrentIndex(0)

        # 初始化列表字段
        self.ui.WatchDogList.setColumnCount(9)
        self.ui.WatchDogList.setHorizontalHeaderLabels(['启用', '运行', '别名', 'pid', '程序名', 'cpu', '内存', '线程', '运行时间'])
        _row = 0
        self.ui.WatchDogList.setColumnWidth(_row, 30)  # 启用
        _row += 1
        self.ui.WatchDogList.setColumnWidth(_row, 40)  # 运行
        _row += 1
        self.ui.WatchDogList.setColumnWidth(_row, 70)  # 别名
        _row += 1
        self.ui.WatchDogList.setColumnWidth(_row, 60)  # pid
        _row += 1
        self.ui.WatchDogList.setColumnWidth(_row, 110) # 程序名
        _row += 1
        self.ui.WatchDogList.setColumnWidth(_row, 60) # cpu
        _row += 1
        self.ui.WatchDogList.setColumnWidth(_row, 90) # 内存
        _row += 1
        self.ui.WatchDogList.setColumnWidth(_row, 40)  # 线程
        _row += 1
        self.ui.WatchDogList.setColumnWidth(_row, 100)  # 运行时间
        header = self.ui.WatchDogList.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.ui.WatchDogList.setEditTriggers(self.ui.WatchDogList.EditTrigger.NoEditTriggers)   # 设置不能修改单元格
        self.ui.WatchDogList.setSelectionMode(self.ui.WatchDogList.SelectionMode.SingleSelection)   # 设置单选
        self.ui.WatchDogList.setSelectionBehavior(self.ui.WatchDogList.SelectionBehavior.SelectRows)    # 设置选一行
        self.ui.WatchDogList.currentItemChanged.connect(self.table_row_select)
        self.ui.WatchDogList.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)   # 设置可以右键
        self.ui.WatchDogList.customContextMenuRequested.connect(self.show_watchdog_list_menu)


        self.ui.SystemUsageStateLabel.setStyleSheet("""color: #4A90E2;""")

        # 禁用进程按钮
        self.disabled_process_button()
        # 进程按钮信号槽
        self.ui.UseButton.clicked.connect(self.switch_selected_listening_process)
        self.ui.SwitchButton.clicked.connect(self.switch_selected_process)
        self.ui.RemoveButton.clicked.connect(self.remove_listening_process)
        self.ui.ServerUrlButton.clicked.connect(self.server_url_listening_process)
        self.ui.RestartButton.clicked.connect(self.restart_selected_process)
        self.ui.BrowseButton.clicked.connect(self.browse_selected_process)
        self.ui.ProcessSetupButton.clicked.connect(self.setup_selected_process)

        # 添加菜单Action
        self.ui.addProcessAction = QAction("添加检测进程")
        self.ui.FullSetupAction = QAction("全局设置")
        self.ui.extendAction = QAction("扩展功能")
        self.ui.menubar.addActions([self.ui.addProcessAction, self.ui.FullSetupAction, self.ui.extendAction])

        self.ui.addProcessAction.triggered.connect(lambda :self.create_dialog(opt='add', process=None))
        self.ui.FullSetupAction.triggered.connect(lambda : self.switch_page(1))
        self.ui.extendAction.triggered.connect(self.show_extend_menu)

        # 全局设置界面
        self.ui.show_version_label.setText(f"[ 当前版本: {version_log[-1][0]} ]")
        self.ui.show_version_label.setStyleSheet("""color: #888888""")
        self.ui.autoStartUpCheckBox.setChecked(self.AUTO_START)
        self.ui.create_start_script_button.clicked.connect(self.create_start_script)
        self.ui.start_way_combobox.addItems(START_WAY)
        self.ui.FullSetupMemComboBox.addItems(MEM_UNIT_LIST)
        self.ui.FullSetupReopenComboBox.addItems(REOPEN_LIST)
        self.ui.FullSetupFlushSpin.setDecimals(1)
        self.ui.FullSetupFlushSpin.setSingleStep(0.1)
        self.ui.FullSetupFlushSpin.setRange(0.5, 5)
        self.ui.FullSetupFlushSpin.setValue(1)

        self.ui.autoStartUpCheckBox.stateChanged.connect(self.switch_start_up)
        self.ui.FullSetup_HiddenButton.toggled.connect(self.setup_auto_hidden_checkbox)
        self.ui.start_way_combobox.currentIndexChanged.connect(self.setup_start_way)
        self.ui.FullSetupMemComboBox.currentIndexChanged.connect(self.setup_switch_mem_unit)
        self.ui.FullSetupReopenComboBox.currentIndexChanged.connect(self.setup_switch_reopen)
        self.ui.FullSetupFlushSpin.valueChanged.connect(self.setup_flush_spin)

        self.ui.frpc_path_button.clicked.connect(self.setup_frpc_path)
        self.ui.frpc_clear_button.clicked.connect(self.clear_frpc_path)

        self.ui.FullSetupBackMainButton.clicked.connect(lambda : self.switch_page(0))

    # 功能初始化
    def function_init(self):
        self.auto_check_config()
        # 读取配置
        self.load_config()
        # 初始化表格
        self.create_table_row()

    # 初始化系统托盘图标
    def init_tray(self):
        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setIcon(self.icon)  # 使用你自己的图标文件
        # 显示托盘图标
        self.tray_icon.show()
        # 设置双击托盘图标显示/隐藏窗口
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.setToolTip("看门狗")

        # 创建右键菜单
        self.tray_icon_menu = QMenu()

        self.tray_icon_show = QAction("显示")
        self.tray_icon_exit_action = QAction("退出")
        self.tray_icon_show.triggered.connect(lambda :self.win.hide() if self.win.isVisible() else self.win.show())
        self.tray_icon_exit_action.triggered.connect(self.before_exit)

        # 将菜单项添加到菜单
        self.tray_icon_menu.addActions([self.tray_icon_show, self.tray_icon_exit_action])
        self.tray_icon.setContextMenu(self.tray_icon_menu)

    # 小图标
    def on_tray_icon_activated(self, reason):
        # 双击托盘图标显示/隐藏窗口
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.win.isVisible():
                self.win.hide()
            else:
                self.win.show()

    # 退出前操作
    def before_exit(self):
        self.timer.stop()
        self.tray_icon.hide()
        if self.temp_file_handle:
            self.temp_file_handle.close()
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        self.app.quit()

    # 设置_初始化配置文件
    @staticmethod
    def init_config():
        # 如果配置文件不存在, 创建
        if not os.path.exists(config_path):
            with open(config_path, 'wb') as f:
                pickle.dump(DEFAULT_CONFIG, f)

    # 设置_自检配置文件
    def auto_check_config(self):
        with open(config_path, 'rb') as f:
            self.config = pickle.load(f)
        flag = False
        for k, v in DEFAULT_CONFIG.items():
            if k in self.config.keys():
                pass
            else:
                flag = True
                self.config[k] = v
        if flag:
            self.save_config()


    # 设置_读取本地配置文件
    def load_config(self):
        self.init_config()
        try:
            with config_lock:
                with open(config_path, 'rb') as f:
                    self.config = pickle.load(f)
        except:
            os.remove(config_path)
            self.init_config()
            with open(config_path, 'rb') as f:
                self.config = pickle.load(f)

    # 设置_保存配置到本地
    def save_config(self):
        self.init_config()
        with config_lock:
            try:
                temp_file = tempfile.NamedTemporaryFile(mode='wb', delete=False)
                with temp_file as tf:
                    pickle.dump(self.config, tf)
                shutil.move(temp_file.name, config_path)
            except Exception as e:
                self.show_message(f"保存配置出错{str(e)}", level='alarm')
            finally:
                if os.path.exists(temp_file.name):
                    os.remove(temp_file.name)
        self.show_message("保存成功")
        print(f"save_config: {self.config}")


    # 设置_自动隐藏复选框
    def setup_auto_hidden_checkbox(self, toggled):
        self.config['AUTO_HIDDEN'] = toggled
        self.save_config()

    # 设置_更换启动方式
    def setup_start_way(self, index):
        self.config['START_WAY'] = index
        self.save_config()

    # 设置_更换内存全局单位
    def setup_switch_mem_unit(self, index):
        self.config['MEM_UNIT'] = index
        self.save_config()

    # 设置_更换启动选项
    def setup_switch_reopen(self, index):
        self.config['REOPEN_OPT'] = index
        self.save_config()

    # 设置_刷新时间间隔
    def setup_flush_spin(self, value):
        self.config['FLUSH_TIME'] = float(value)
        self.save_config()

    # 设置_浏览frpc.toml位置
    def setup_frpc_path(self):
        file_path, _ = QFileDialog.getOpenFileName(self.win, "选择文件", "", "frp配置文件 (*.toml)")
        if file_path:
            self.ui.frpc_path_line_edit.setText(file_path)
            self.config['FRPC_PATH'] = file_path
            self.save_config()

    # 设置_清空frpc.toml位置
    def clear_frpc_path(self):
        self.config['FRPC_PATH'] = ""
        self.ui.frpc_path_line_edit.setText("")
        self.save_config()

    # 扩展功能_显示扩展功能菜单栏
    def show_extend_menu(self, pos):
        menu = QMenu()

        # 添加菜单动作
        frps_edit = menu.addAction("Frpc编辑")
        frps_edit.triggered.connect(self.edit_frpc_config)

        # 在 extendAction 的位置弹出菜单
        # 获取触发动作的控件的全局位置
        global_pos = self.ui.menubar.mapToGlobal(self.ui.menubar.actionGeometry(self.ui.extendAction).bottomRight())

        # 在全局位置显示菜单
        menu.exec(global_pos)

    # 扩展功能_编辑frpc.toml
    def edit_frpc_config(self):
        if self.config.get('FRPC_PATH') == '':
            QMessageBox.information(self.win, '提示', '未配置frpc.toml位置, 请进行配置')
            self.switch_page(1)
        else:
            try:
                os.startfile(self.config.get('FRPC_PATH'))
            except Exception as e:
                QMessageBox.warning(self.win, '提示', 'frpc.toml打开失败, 请检查配置是否正确')

    # QT_禁用所有进程按钮
    def disabled_process_button(self):
        self.ui.UseButton.setEnabled(False)
        self.ui.RemoveButton.setEnabled(False)
        self.ui.SwitchButton.setEnabled(False)
        self.ui.RestartButton.setEnabled(False)
        self.ui.BrowseButton.setEnabled(False)
        self.ui.ProcessSetupButton.setEnabled(False)

    # QT_改变进程按钮的内容状态
    def update_process_button(self, process):
        # 启用看门狗
        if process.get('use_listen'):
            self.ui.UseButton.setText('禁用看门狗')
        else:
            self.ui.UseButton.setText('启用看门狗')
        self.ui.UseButton.setEnabled(True)
        self.ui.RemoveButton.setEnabled(True)
        # 切换运行状态按钮
        if process.get('run_status'):
            self.ui.SwitchButton.setText("停止")
        else:
            self.ui.SwitchButton.setText("启动")
        self.ui.SwitchButton.setEnabled(True)
        self.ui.RestartButton.setEnabled(True)
        self.ui.BrowseButton.setEnabled(True)
        self.ui.ProcessSetupButton.setEnabled(True)

    # QT_获取颜色
    @staticmethod
    def get_health_color(value: float) -> str:
        # 直接根据数值区间返回颜色的十六进制字符串
        if value <= 20:
            return "#66cc66"  # 浅绿色[0~20]
        elif value <= 40:
            return "#32cd32"  # 健康绿色[20~40]
        elif value <= 60:
            return "#00bfff"  # 蓝色[40~60]
        elif value <= 80:
            return "#ff8000"  # 橙色[60~80]
        else:
            return "#ff0000"  # 红色[80~100]

    # QT_单次更新数据
    def flush_data(self):
        self.ui.CPUusageLabel.setText(f"[CPU]: {self.wmi.system_usage.get('cpu_percent')} % ")
        self.ui.MEMusageLabel.setText(f" [内存]: {self.wmi.system_usage.get('memory_percent')} %")
        self.ui.CPUusageLabel.setStyleSheet(f"""color: {self.get_health_color(self.wmi.system_usage.get('cpu_percent'))};""")
        self.ui.MEMusageLabel.setStyleSheet(f"""color: {self.get_health_color(self.wmi.system_usage.get('memory_percent'))};""")
        # # 获取在监听的程序列表
        # self.load_config()
        # listening = self.config.get('LISTENING')
        # self.process_list = []
        # # 遍历存储的进程, 从实时进程列表中获取对应的数据
        # for index, (name, info) in enumerate(listening.items()):
        #     # 初始化数据
        #     process = dict(
        #         id=index,
        #         use_listen=info.get('use_listen'),
        #         other_name=info.get('other_name'),
        #         exe_path=info.get('exe_path'),
        #         work_dir=info.get('work_dir'),
        #         arguments=info.get('arguments'),
        #         hidden=info.get('hidden'),
        #         run_status=False,
        #         pid='--',
        #         name='--',
        #         command_line='--',
        #         thread_count='--',
        #         cpu_percent='--',
        #         memory_usage='--',
        #         visual_memory='--',
        #         running_time='--',
        #     )
        #     if self.wmi.check_process(name):  # 进程存在, 更新数据
        #         process['run_status'] = True
        #         process.update(self.wmi.optimize_process_data(name, self.config.get('MEM_UNIT')))
        #
        #     if process.get('use_listen') and self.wmi.execution is False:  # 如果进程启用监听状态, 并且不在执行状态
        #         if self.wmi.processes_dict:  # 至少已经检查完一次进程状态
        #             if process.get('run_status'):  # 如果进程在运行, 不做任何操作
        #                 pass
        #             else:  # 进程不存在, 启动
        #                 self.wmi.start_process(process)
        #                 time.sleep(1)
        #
        #     self.process_list.append(process)
        #     self.update_table_row(process)
        # 更新当前选中进程的按钮状态
        process = self.get_process_by_selected()
        if process:
            self.update_process_button(process)
        else:
            self.disabled_process_button()

    # QT_输出状态栏
    def show_message(self, message, timeout=2000, level='normal'):
        if level == 'normal':
            self.ui.statusbar.setStyleSheet("")
        elif level == 'alarm':
            self.ui.statusbar.setStyleSheet("QStatusBar { color: red; }")
        self.ui.statusbar.showMessage(message, timeout)

    # QT_获取选中行的进程运行时信息
    def get_process_by_selected(self):
        try:
            row = self.get_selected_row()
            if row == -1:
                return None
            return self.process_list[row]
        except:
            return None


    # QT_选中行内容
    def table_row_select(self):
        process = self.get_process_by_selected()
        if process:
            self.update_process_button(process)

    # QT_获取当前选中行
    def get_selected_row(self):
        return self.ui.WatchDogList.currentRow()

    # QT_获取当前监听中字典
    def get_config_listening(self):
        self.load_config()
        listening = self.config.get('LISTENING')
        return listening

    # QT_切换页面
    def switch_page(self, page):
        if page == 0:   # 主界面
            self.timer.start()
            self.ui.FullSetupAction.setText('全局设置')
            self.ui.FullSetupAction.triggered.disconnect()
            self.ui.FullSetupAction.triggered.connect(lambda: self.switch_page(1))
            # 启用添加按钮
            self.ui.addProcessAction.setEnabled(True)
        elif page == 1: # 全局设置界面
            self.ui.FullSetupAction.setText('回主界面')
            self.ui.FullSetupAction.triggered.disconnect()
            self.ui.FullSetupAction.triggered.connect(lambda : self.switch_page(0))
            self.timer.stop()
            # 禁用添加按钮
            self.ui.addProcessAction.setEnabled(False)
            # 读取配置并显示
            self.load_config()
            self.ui.autoStartUpCheckBox.setChecked(self.AUTO_START)
            self.ui.FullSetup_HiddenButton.setChecked(self.config.get('AUTO_HIDDEN'))
            self.ui.start_way_combobox.setCurrentIndex(self.config.get('START_WAY'))
            self.ui.FullSetupMemComboBox.setCurrentIndex(self.config.get('MEM_UNIT'))
            self.ui.FullSetupReopenComboBox.setCurrentIndex(self.config.get('REOPEN_OPT'))
            self.ui.FullSetupFlushSpin.setValue(self.config.get('FLUSH_TIME'))
            self.ui.frpc_path_line_edit.setText(self.config.get('FRPC_PATH'))
        self.ui.stackedWidget.setCurrentIndex(page)

    # QT_初始化表格内容
    def create_table_row(self):
        # 清空表格内容
        self.ui.WatchDogList.setRowCount(0)
        # 清除选中行
        self.ui.WatchDogList.clearSelection()
        self.load_config()
        _row = len(self.config.get('LISTENING').keys())
        self.ui.WatchDogList.setRowCount(_row)

    # QT_更新表格内容
    def update_table_row(self, process_dict):
        def QTableWidgetItemCenter(value):
            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            return item
        _c = 0
        self.ui.WatchDogList.setItem(process_dict.get('id'), _c, QTableWidgetItemCenter('是' if process_dict.get('use_listen') else '否'))  # 状态
        _c += 1
        self.ui.WatchDogList.setItem(process_dict.get('id'), _c, QTableWidgetItemCenter('运行' if process_dict.get('run_status') else '停止'))  # 状态
        _c += 1
        self.ui.WatchDogList.setItem(process_dict.get('id'), _c, QTableWidgetItemCenter(process_dict.get('other_name')))  # 别名
        _c += 1
        self.ui.WatchDogList.setItem(process_dict.get('id'), _c, QTableWidgetItemCenter(process_dict.get('pid')))  # pid
        _c += 1
        self.ui.WatchDogList.setItem(process_dict.get('id'), _c, QTableWidgetItemCenter(process_dict.get('name')))  # 程序名
        _c += 1
        self.ui.WatchDogList.setItem(process_dict.get('id'), _c, QTableWidgetItemCenter(process_dict.get('cpu_percent')))  # cpu
        _c += 1
        self.ui.WatchDogList.setItem(process_dict.get('id'), _c, QTableWidgetItemCenter(process_dict.get('memory_usage')))  # 内存
        _c += 1
        self.ui.WatchDogList.setItem(process_dict.get('id'), _c, QTableWidgetItemCenter(process_dict.get('thread_count')))  # 线程
        _c += 1
        self.ui.WatchDogList.setItem(process_dict.get('id'), _c, QTableWidgetItemCenter(process_dict.get('running_time')))  # 运行时间

    # QT_创建对话框(添加监听项)
    def create_dialog(self, opt='add', process=None):
        # 关闭对话框
        def close_dialog(instance):
            instance.dialog.close()
            instance.dialog = None
        # 文件选择对话框
        def open_file_dialog(instance):
            # 打开文件选择对话框
            file_name, _ = QFileDialog.getOpenFileName(instance.dialog, "打开文件", "", "可执行文件 (*.exe)")
            if file_name:
                instance.dialog_ui.ExePathEdit.setText(file_name)
                instance.dialog_ui.WorkDirEdit.setText(os.path.dirname(file_name))
            else:
                pass
        # 工作路径选择对话框
        def open_workdir_dialog(instance):
            # 打开文件选择对话框
            directory  = QFileDialog.getExistingDirectory(instance.dialog, "打开文件夹", "")
            if directory:
                instance.dialog_ui.WorkDirEdit.setText(directory)
            else:
                pass
        # 添加监听文件到目录
        def add_listen_process(instance):
            other_name = instance.dialog_ui.OtherNameEdit.text()
            exe_path = instance.dialog_ui.ExePathEdit.text()
            work_dir = instance.dialog_ui.WorkDirEdit.text()
            arguments = instance.dialog_ui.ArgumentsEdit.text()
            hidden = instance.dialog_ui.HiddenCheckBox.isChecked()
            url = instance.dialog_ui.UrlServiceEdit.text()

            if not other_name:
                instance.show_message("请输入别名", level='alarm')
                return
            if not exe_path:
                instance.show_message("请输入可执行文件路径", level='alarm')
                return
            if opt == 'add':
                if os.path.basename(exe_path) not in instance.config.get('LISTENING').keys():
                    instance.config['LISTENING'][os.path.basename(exe_path)] = dict(use_listen=False,
                                                                                    other_name=other_name,
                                                                                    exe_path=exe_path,
                                                                                    work_dir=work_dir,
                                                                                    arguments=arguments,
                                                                                    hidden=hidden,
                                                                                    url=url)
                    close_dialog(instance)
                else:
                    instance.show_message(f"{os.path.basename(exe_path)} 已存在", level='alarm')
                    return
                instance.save_config()
            elif opt == 'edit':
                _process = self.config.get('LISTENING').get(os.path.basename(exe_path))
                _process['other_name'] = other_name
                _process['work_dir'] = work_dir
                _process['arguments'] = arguments
                _process['hidden'] = hidden
                _process['url'] = url
                self.config['LISTENING'][os.path.basename(exe_path)] = _process
                self.save_config()
                close_dialog(instance)
            self.create_table_row()

        # 初始化对话框窗口
        self.dialog = QDialog(self.win)
        self.dialog_ui.setupUi(self.dialog)

        self.dialog_ui.ExePathButton.clicked.connect(lambda: open_file_dialog(self))
        self.dialog_ui.WorkDirButton.clicked.connect(lambda: open_workdir_dialog(self))
        self.dialog_ui.SaveButton.clicked.connect(lambda: add_listen_process(self))

        self.dialog_ui.ExePathEdit.setReadOnly(True)
        self.dialog_ui.WorkDirEdit.setReadOnly(True)



        # self.dialog.setFixedSize(390, 260)
        if opt == 'add':
            self.dialog.setWindowTitle("添加监听项")
            self.dialog_ui.UrlServiceEdit.setText('http://127.0.0.1:80')
        elif opt == 'edit':
            self.dialog.setWindowTitle("修改监听项")
            self.dialog_ui.exe_label.setText("可执行文件路径(不可修改)")
            self.dialog_ui.ExePathButton.setDisabled(True)
            self.dialog_ui.OtherNameEdit.setText(process.get('other_name'))
            self.dialog_ui.ExePathEdit.setText(process.get('exe_path'))
            self.dialog_ui.WorkDirEdit.setText(process.get('work_dir'))
            self.dialog_ui.ArgumentsEdit.setText(process.get('arguments'))
            self.dialog_ui.HiddenCheckBox.setChecked(process.get('hidden'))
            self.dialog_ui.UrlServiceEdit.setText(process.get('url'))
        self.dialog_ui.CancelButton.clicked.connect(lambda: close_dialog(self))
        self.dialog.exec()

    # QT_列表选中右键菜单
    def show_watchdog_list_menu(self, pos):
        item = self.ui.WatchDogList.itemAt(pos)
        process = self.get_process_by_selected()
        if item:
            menu = QMenu(self.ui.WatchDogList)
            label = QLabel(process.get('other_name'))
            label.setStyleSheet("font-weight: bold; margin: 5px;margin-left: 20px")  # 设置样式
            label_action = QWidgetAction(menu)
            label_action.setDefaultWidget(label)
            menu.addAction(label_action)
            menu.addSeparator()
            switch = menu.addAction("停止" if process.get('run_status') else "启动")
            restart = menu.addAction("重启")
            start_url = menu.addAction("打开服务页")
            menu.addSeparator()
            if process.get('use_listen'):
                use = menu.addAction("禁用看门狗")
            else:
                use = menu.addAction("启用看门狗")
            remove = menu.addAction("移除")
            browse = menu.addAction("浏览")
            setup = menu.addAction("设置")
            copy_command = menu.addAction("复制启动命令")
            menu.addSeparator()
            move_up = menu.addAction("上移")
            move_down = menu.addAction("下移")
            action = menu.exec(self.ui.WatchDogList.mapToGlobal(pos))  # 显示菜单

            if action == use:
                self.switch_selected_listening_process()
            elif action == remove:
                self.remove_listening_process()
            elif action == start_url:
                self.server_url_listening_process()
            elif action == switch:
                self.switch_selected_process()
            elif action == restart:
                self.restart_selected_process()
            elif action == browse:
                self.browse_selected_process()
            elif action == setup:
                self.setup_selected_process()
            elif action == move_up:
                self.move_up_process()
            elif action == move_down:
                self.move_down_process()
            elif action == copy_command:
                self.get_start_command()

    # QT_移除选中监听项
    def remove_listening_process(self):
        row = self.get_selected_row()
        listening = self.get_config_listening()

        msg_box = QMessageBox()
        msg_box.setWindowTitle("移除监听项")
        msg_box.setText(f"你确定要移除 {listening.get(list(listening.keys())[row]).get('other_name')} 吗")
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        # 显示对话框并获取用户选择
        user_choice = msg_box.exec()

        # 根据用户选择执行操作
        if user_choice == QMessageBox.Yes:
            self.config['LISTENING'].pop(list(listening.keys())[row])
            self.save_config()
            self.create_table_row()
        elif user_choice == QMessageBox.No:
            pass

    # QT_打开服务页面
    def server_url_listening_process(self):
        process = self.get_process_by_selected()
        self.start_url(process.get('url', 'http://127.0.0.1:80'))

    # QT_启用/禁用选中进程的监听
    def switch_selected_listening_process(self):
        process = self.get_process_by_selected()
        if process.get('use_listen'):
            self.config['LISTENING'][os.path.basename(process.get('exe_path'))]['use_listen'] = False
        else:
            self.config['LISTENING'][os.path.basename(process.get('exe_path'))]['use_listen'] = True
        self.save_config()

    # QT_启动/停止进程
    def switch_selected_process(self):
        process = self.get_process_by_selected()
        if process.get('run_status'):
            self.wmi.stop_process(process)
        else:
            self.wmi.start_process(process)

    # QT_重启进程
    def restart_selected_process(self):
        process = self.get_process_by_selected()
        self.wmi.restart_process(process)

    # QT_打开进程的目录
    def browse_selected_process(self):
        process = self.get_process_by_selected()
        os.startfile(process.get('work_dir'))

    # QT_设置选中监听项
    def setup_selected_process(self):
        process = self.get_process_by_selected()
        self.create_dialog(opt='edit', process=process)

    # QT_上移选中监听项
    def move_up_process(self):
        process = self.get_process_by_selected()
        process_name = os.path.basename(process.get('exe_path'))
        meta_list = list(self.config.get('LISTENING').keys())
        p_index = meta_list.index(process_name)
        if p_index == 0:
            return
        element = meta_list.pop(p_index)
        meta_list.insert(p_index - 1, element)
        new_listening = {}
        for item in meta_list:
            new_listening[item] = self.config.get('LISTENING').get(item)
        self.config['LISTENING'] = new_listening
        self.save_config()

    # QT_下移选中监听项
    def move_down_process(self):
        process = self.get_process_by_selected()
        process_name = os.path.basename(process.get('exe_path'))
        meta_list = list(self.config.get('LISTENING').keys())
        p_index = meta_list.index(process_name)
        if p_index == len(meta_list) -1:
            return
        element = meta_list.pop(p_index)
        meta_list.insert(p_index + 1, element)
        new_listening = {}
        for item in meta_list:
            new_listening[item] = self.config.get('LISTENING').get(item)
        self.config['LISTENING'] = new_listening
        self.save_config()

    # QT_获取启动命令
    def get_start_command(self):
        process = self.get_process_by_selected()
        command, args = self.wmi._create_command(process, self.config.get('START_WAY'))
        self.copy_to_clipboard(command)

    # QT_复制到剪切板
    def copy_to_clipboard(self, msg):
        clipboard = self.app.clipboard()
        clipboard.setText(msg)
        self.show_message("复制成功")  # 提示用户

    # QT_打开服务页
    def start_url(self, url):
        try:
            webbrowser.open(url)
        except webbrowser.Error as e:
            self.show_message(f"打开 URL 时出错: {e}", level='alarm')

def kill_process_by_name(process_name):
    """通过进程名称结束进程"""
    current_pid = os.getpid()  # 获取当前进程 ID
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            # 检查进程名是否匹配
            if proc.info['name'] == process_name and proc.info["pid"] != current_pid:
                print(f"正在终止进程: {proc.info['name']} (PID: {proc.info['pid']})")
                os.kill(int(proc.info['pid']), signal.SIGTERM)
                print(f"进程 {proc.info['name']} 已终止")

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    print(f"未找到名为 {process_name} 的进程")
    return False

# 清除win32com缓存
def clear_gencache():
    """
    清除 win32com gencache 缓存文件夹
    """
    cache_dir = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Temp", "gen_py")
    if os.path.exists(cache_dir):
        print(f"发现缓存文件夹: {cache_dir}")
        try:
            shutil.rmtree(cache_dir)  # 删除整个缓存文件夹
            print("已清除 gencache 缓存。")
        except Exception as e:
            print(f"清除缓存时出错: {e}")
    else:
        print("未找到 gencache 缓存文件夹。")

if __name__ == '__main__':
    clear_gencache()
    if os.path.exists(temp_file_path):
        try:    # 如果文件存在, 尝试删除, 删除成功则说明软件未运行, 启动
            fd = os.open(temp_file_path, os.O_RDWR | os.O_EXCL)
            os.close(fd)    # 文件未被占用, 移除
            os.remove(temp_file_path)
            time.sleep(1)
            wd = WatchDogQT()
            sys.exit(wd.app.exec())
        except: # 如果删除失败, 则说明软件运行中, 需要判断是否重启
            with open(config_path, 'rb') as f:
                config = pickle.load(f)
            if config.get('REOPEN_OPT') == 0:   # 无操作
                pass
            elif config.get('REOPEN_OPT') == 1: # 重启
                process_name = "WatchDog.exe"  # 需要杀掉的进程名
                # 杀掉进程
                kill_process_by_name(process_name)
                time.sleep(1)  # 等待一段时间确保资源释放

                wd = WatchDogQT()
                sys.exit(wd.app.exec())
    else:
        wd = WatchDogQT()
        sys.exit(wd.app.exec())



