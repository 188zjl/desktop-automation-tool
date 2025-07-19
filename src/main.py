#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
桌面自动化脚本 - 压缩包处理和视频提取工具
功能：解压.tar.gz文件，处理内部压缩文件，提取MP4视频文件
作者：自动化脚本生成器
版本：1.0
"""

import os
import sys
import shutil
import tarfile
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import logging
from pathlib import Path
import subprocess
import time
from datetime import datetime

# 尝试导入可选依赖库
try:
    import rarfile
    RARFILE_AVAILABLE = True
except ImportError:
    RARFILE_AVAILABLE = False
    print("警告: rarfile库未安装，RAR文件支持将不可用")

try:
    import py7zr
    PY7ZR_AVAILABLE = True
except ImportError:
    PY7ZR_AVAILABLE = False
    print("警告: py7zr库未安装，7z文件支持将不可用")

class DesktopAutomationTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("桌面自动化脚本 - 高级压缩包处理工具")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # 设置默认密码
        self.default_password = "chinatkclub.com"
        
        # 获取桌面路径
        self.desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        
        # 初始化变量
        self.source_files = []  # 源文件列表
        self.file_output_dirs = {}  # 每个文件对应的输出目录
        self.output_mode = "unified"  # unified/individual
        self.output_dir = self.desktop_path
        self.temp_dir = ""
        self.extracted_files = []
        self.mp4_files = []
        self.cleanup_files = []
        self.failed_files = []  # 失败的文件列表
        self.failed_reasons = {}  # 失败原因
        
        # 设置日志
        self.setup_logging()
        
        # 创建GUI界面
        self.create_gui()
        
        # 支持的压缩格式（增强检测）
        self.supported_formats = ['.tar.gz', '.tgz', '.tar.bz2', '.tar.xz', '.zip', '.rar', '.7z', '.666z', '.001', '.part1.rar']
        
        # 智能格式映射
        self.format_mapping = {
            '.666z': '.7z',
            '.001': '.7z',  # 分卷压缩的第一部分通常是7z格式
            '.part1.rar': '.rar'
        }
        
    def setup_logging(self):
        """设置日志记录"""
        log_filename = f"automation_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        log_path = os.path.join(self.desktop_path, log_filename)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_path, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("桌面自动化脚本启动")
        
    def create_gui(self):
        """创建图形用户界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="桌面自动化脚本 - 高级压缩包处理工具",
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 文件选择区域
        file_frame = ttk.LabelFrame(main_frame, text="文件选择", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        # 源文件选择
        ttk.Label(file_frame, text="源压缩包:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        # 创建文件列表框架
        files_frame = ttk.Frame(file_frame)
        files_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        files_frame.columnconfigure(0, weight=1)
        
        # 文件列表显示
        self.files_listbox = tk.Listbox(files_frame, height=5, selectmode=tk.EXTENDED)
        files_scrollbar = ttk.Scrollbar(files_frame, orient=tk.VERTICAL, command=self.files_listbox.yview)
        self.files_listbox.configure(yscrollcommand=files_scrollbar.set)
        
        self.files_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        files_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 按钮框架
        button_frame = ttk.Frame(file_frame)
        button_frame.grid(row=0, column=2, pady=5)
        
        ttk.Button(button_frame, text="添加文件", command=self.add_source_files).grid(row=0, column=0, pady=(0, 5))
        ttk.Button(button_frame, text="清空列表", command=self.clear_source_files).grid(row=1, column=0, pady=(0, 5))
        ttk.Button(button_frame, text="设置输出", command=self.configure_output_dirs).grid(row=2, column=0)
        
        # 输出模式选择
        output_mode_frame = ttk.Frame(file_frame)
        output_mode_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(output_mode_frame, text="输出模式:").grid(row=0, column=0, sticky=tk.W)
        self.output_mode_var = tk.StringVar(value="unified")
        ttk.Radiobutton(output_mode_frame, text="统一输出到一个文件夹", variable=self.output_mode_var,
                       value="unified", command=self.on_output_mode_change).grid(row=0, column=1, padx=(10, 0))
        ttk.Radiobutton(output_mode_frame, text="每个文件输出到独立文件夹", variable=self.output_mode_var,
                       value="individual", command=self.on_output_mode_change).grid(row=0, column=2, padx=(10, 0))
        
        # 输出目录选择
        self.output_dir_frame = ttk.Frame(file_frame)
        self.output_dir_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        self.output_dir_frame.columnconfigure(1, weight=1)
        
        ttk.Label(self.output_dir_frame, text="基础输出目录:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.output_var = tk.StringVar(value=self.desktop_path)
        ttk.Entry(self.output_dir_frame, textvariable=self.output_var, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        ttk.Button(self.output_dir_frame, text="浏览", command=self.select_output_dir).grid(row=0, column=2, pady=5)
        
        # 高级选项区域
        options_frame = ttk.LabelFrame(main_frame, text="处理选项", padding="10")
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        options_frame.columnconfigure(1, weight=1)
        
        # 基础选项
        basic_options_frame = ttk.Frame(options_frame)
        basic_options_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.auto_cleanup = tk.BooleanVar(value=True)
        ttk.Checkbutton(basic_options_frame, text="自动清理中间文件", variable=self.auto_cleanup).grid(row=0, column=0, sticky=tk.W)
        
        self.recursive_extract = tk.BooleanVar(value=True)
        ttk.Checkbutton(basic_options_frame, text="递归解压内部压缩文件", variable=self.recursive_extract).grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
        
        self.smart_format_detection = tk.BooleanVar(value=True)
        ttk.Checkbutton(basic_options_frame, text="智能格式检测和转换", variable=self.smart_format_detection).grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        self.interactive_failure_handling = tk.BooleanVar(value=True)
        ttk.Checkbutton(basic_options_frame, text="交互式失败处理", variable=self.interactive_failure_handling).grid(row=1, column=1, sticky=tk.W, padx=(20, 0), pady=(5, 0))
        
        # 密码设置区域
        password_frame = ttk.LabelFrame(options_frame, text="密码设置", padding="5")
        password_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        password_frame.columnconfigure(1, weight=1)
        
        ttk.Label(password_frame, text="默认密码:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.password_var = tk.StringVar(value=self.default_password)
        ttk.Entry(password_frame, textvariable=self.password_var, show="*", width=25).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=2)
        
        ttk.Label(password_frame, text="备用密码:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.backup_passwords_var = tk.StringVar(value="123456,password,admin")
        ttk.Entry(password_frame, textvariable=self.backup_passwords_var, width=25).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=2)
        
        ttk.Label(password_frame, text="(多个密码用逗号分隔)", font=('Arial', 8)).grid(row=2, column=1, sticky=tk.W, padx=(10, 0))
        
        # 控制按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(0, 10))
        
        self.start_button = ttk.Button(button_frame, text="开始处理", command=self.start_processing)
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(button_frame, text="清空日志", command=self.clear_log).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(button_frame, text="退出", command=self.root.quit).grid(row=0, column=2)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 状态标签
        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=5, column=0, columnspan=3, sticky=tk.W)
        
        # 日志显示区域
        log_frame = ttk.LabelFrame(main_frame, text="处理日志", padding="10")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        # 创建文本框和滚动条
        self.log_text = tk.Text(log_frame, height=15, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
    def add_source_files(self):
        """添加源压缩包文件"""
        filetypes = [
            ("压缩包文件", "*.tar.gz;*.tgz;*.zip;*.rar;*.7z;*.666z"),
            ("所有文件", "*.*")
        ]
        filenames = filedialog.askopenfilenames(
            title="选择压缩包文件（可多选）",
            filetypes=filetypes
        )
        if filenames:
            for filename in filenames:
                if filename not in self.source_files:
                    self.source_files.append(filename)
                    self.files_listbox.insert(tk.END, os.path.basename(filename))
                    self.log_message(f"已添加文件: {os.path.basename(filename)}")
            
            self.log_message(f"当前共选择了 {len(self.source_files)} 个文件")
    
    def clear_source_files(self):
        """清空源文件列表"""
        self.source_files.clear()
        self.file_output_dirs.clear()
        self.files_listbox.delete(0, tk.END)
        self.log_message("已清空文件列表")
    
    def on_output_mode_change(self):
        """输出模式改变时的处理"""
        self.output_mode = self.output_mode_var.get()
        self.log_message(f"输出模式已切换为: {'统一输出' if self.output_mode == 'unified' else '独立输出'}")
        
    def configure_output_dirs(self):
        """配置每个文件的输出目录"""
        if not self.source_files:
            messagebox.showwarning("警告", "请先添加要处理的文件！")
            return
            
        if self.output_mode == "unified":
            messagebox.showinfo("提示", "当前为统一输出模式，所有文件将输出到同一目录")
            return
            
        # 创建配置窗口
        config_window = tk.Toplevel(self.root)
        config_window.title("配置输出目录")
        config_window.geometry("600x400")
        config_window.transient(self.root)
        config_window.grab_set()
        
        # 主框架
        main_frame = ttk.Frame(config_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="为每个文件配置输出目录:", font=('Arial', 12, 'bold')).pack(pady=(0, 10))
        
        # 创建滚动框架
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 为每个文件创建配置行
        self.output_entries = {}
        for i, source_file in enumerate(self.source_files):
            file_frame = ttk.Frame(scrollable_frame)
            file_frame.pack(fill=tk.X, pady=5)
            
            filename = os.path.basename(source_file)
            ttk.Label(file_frame, text=f"{filename}:", width=30).pack(side=tk.LEFT)
            
            # 获取当前设置的输出目录
            current_dir = self.file_output_dirs.get(source_file, self.output_dir)
            entry_var = tk.StringVar(value=current_dir)
            self.output_entries[source_file] = entry_var
            
            ttk.Entry(file_frame, textvariable=entry_var, width=40).pack(side=tk.LEFT, padx=(5, 5))
            ttk.Button(file_frame, text="浏览",
                      command=lambda sf=source_file: self.browse_individual_output(sf)).pack(side=tk.LEFT)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 按钮框架
        button_frame = ttk.Frame(config_window)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="确定", command=lambda: self.save_output_config(config_window)).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="取消", command=config_window.destroy).pack(side=tk.RIGHT)
        ttk.Button(button_frame, text="全部设为相同", command=self.set_all_same_output).pack(side=tk.LEFT)
        
    def browse_individual_output(self, source_file):
        """为单个文件浏览输出目录"""
        directory = filedialog.askdirectory(
            title=f"选择 {os.path.basename(source_file)} 的输出目录",
            initialdir=self.output_entries[source_file].get()
        )
        if directory:
            self.output_entries[source_file].set(directory)
            
    def set_all_same_output(self):
        """设置所有文件使用相同的输出目录"""
        directory = filedialog.askdirectory(
            title="选择统一输出目录",
            initialdir=self.desktop_path
        )
        if directory:
            for entry_var in self.output_entries.values():
                entry_var.set(directory)
                
    def save_output_config(self, config_window):
        """保存输出目录配置"""
        for source_file, entry_var in self.output_entries.items():
            self.file_output_dirs[source_file] = entry_var.get()
        
        self.log_message("已保存个性化输出目录配置")
        config_window.destroy()
            
    def select_output_dir(self):
        """选择基础输出目录"""
        directory = filedialog.askdirectory(
            title="选择基础输出目录",
            initialdir=self.desktop_path
        )
        if directory:
            self.output_var.set(directory)
            self.output_dir = directory
            self.log_message(f"已选择基础输出目录: {directory}")
            
    def log_message(self, message):
        """在GUI中显示日志消息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, formatted_message)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
        # 同时写入日志文件
        self.logger.info(message)
        
    def clear_log(self):
        """清空日志显示"""
        self.log_text.delete(1.0, tk.END)
        
    def update_progress(self, value, status=""):
        """更新进度条和状态"""
        self.progress_var.set(value)
        if status:
            self.status_var.set(status)
        self.root.update_idletasks()
        
    def start_processing(self):
        """开始处理流程"""
        if not self.source_files:
            messagebox.showerror("错误", "请至少选择一个压缩包文件！")
            return
            
        # 检查所有文件是否存在
        invalid_files = []
        for file_path in self.source_files:
            if not os.path.exists(file_path):
                invalid_files.append(os.path.basename(file_path))
        
        if invalid_files:
            messagebox.showerror("错误", f"以下文件不存在或无法访问：\n" + "\n".join(invalid_files))
            return
            
        if not self.output_dir or not os.path.exists(self.output_dir):
            messagebox.showerror("错误", "请选择有效的输出目录！")
            return
            
        # 禁用开始按钮
        self.start_button.config(state='disabled')
        
        # 在新线程中运行处理流程
        processing_thread = threading.Thread(target=self.processing_workflow)
        processing_thread.daemon = True
        processing_thread.start()
        
    def processing_workflow(self):
        """主要处理工作流程（增强版）"""
        try:
            self.log_message(f"开始高级批量处理工作流程，共 {len(self.source_files)} 个文件...")
            self.update_progress(0, "初始化...")
            
            # 清空失败文件列表
            self.failed_files.clear()
            self.failed_reasons.clear()
            
            # 步骤1: 根据输出模式创建输出目录
            if self.output_mode == "unified":
                self.create_unified_output_directory()
                self.log_message("使用统一输出模式")
            else:
                self.log_message("使用独立输出模式")
            self.update_progress(5, "创建输出目录完成")
            
            # 步骤2: 批量处理每个文件
            total_files = len(self.source_files)
            successful_files = 0
            
            for i, source_file in enumerate(self.source_files):
                try:
                    self.log_message(f"处理文件 ({i+1}/{total_files}): {os.path.basename(source_file)}")
                    
                    # 为每个文件创建临时目录
                    self.create_temp_directory_for_file(source_file, i)
                    
                    # 设置当前文件的输出目录
                    if self.output_mode == "individual":
                        self.setup_individual_output_directory(source_file)
                    
                    # 解压当前文件
                    self.extract_single_archive(source_file)
                    
                    # 处理内部压缩文件
                    if self.recursive_extract.get():
                        self.process_internal_archives()
                    
                    # 提取MP4文件
                    if self.output_mode == "unified":
                        self.extract_mp4_files_to_unified_dir()
                    else:
                        self.extract_mp4_files_to_individual_dir(source_file)
                    
                    # 清理当前文件的临时目录
                    if self.auto_cleanup.get():
                        self.cleanup_current_temp_files()
                    
                    successful_files += 1
                    
                    # 更新进度
                    progress = 10 + (i + 1) * 80 / total_files
                    self.update_progress(progress, f"已处理 {i+1}/{total_files} 个文件")
                    
                except Exception as e:
                    self.log_message(f"处理文件失败 {os.path.basename(source_file)}: {str(e)}")
                    self.failed_files.append(source_file)
                    self.failed_reasons[source_file] = str(e)
                    continue
            
            # 步骤3: 处理失败的文件
            if self.failed_files and self.interactive_failure_handling.get():
                self.handle_failed_files()
            
            # 步骤4: 最终清理
            if self.auto_cleanup.get():
                self.final_cleanup()
                self.update_progress(95, "清理完成")
            
            self.update_progress(100, "批量处理完成！")
            self.log_message(f"批量处理完成！成功处理 {successful_files}/{total_files} 个文件，提取了 {len(self.mp4_files)} 个MP4文件")
            
            if self.failed_files:
                self.log_message(f"失败文件数量: {len(self.failed_files)}")
            
            # 显示结果
            self.show_results()
            
        except Exception as e:
            self.log_message(f"批量处理过程中发生错误: {str(e)}")
            self.logger.error(f"批量处理错误: {str(e)}", exc_info=True)
            messagebox.showerror("错误", f"批量处理过程中发生错误:\n{str(e)}")
        finally:
            # 重新启用开始按钮
            self.start_button.config(state='normal')
            
    def create_unified_output_directory(self):
        """创建统一输出目录"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.unified_output_dir = os.path.join(self.output_dir, f"批量提取结果_{timestamp}")
        os.makedirs(self.unified_output_dir, exist_ok=True)
        self.log_message(f"创建统一输出目录: {self.unified_output_dir}")
        
    def create_temp_directory_for_file(self, source_file, index):
        """为单个文件创建临时工作目录"""
        filename = os.path.splitext(os.path.basename(source_file))[0]
        self.temp_dir = os.path.join(self.output_dir, f"temp_{index}_{filename}")
        os.makedirs(self.temp_dir, exist_ok=True)
        self.log_message(f"创建临时目录: {self.temp_dir}")
        
    def create_temp_directory(self):
        """创建临时工作目录（保持向后兼容）"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.temp_dir = os.path.join(self.output_dir, f"temp_extract_{timestamp}")
        os.makedirs(self.temp_dir, exist_ok=True)
        self.log_message(f"创建临时目录: {self.temp_dir}")
        
    def extract_single_archive(self, source_file):
        """解压单个压缩包"""
        self.log_message(f"开始解压: {os.path.basename(source_file)}")
        
        file_ext = Path(source_file).suffix.lower()
        
        try:
            if file_ext == '.gz' and source_file.endswith('.tar.gz'):
                # 处理.tar.gz文件
                with tarfile.open(source_file, 'r:gz') as tar:
                    tar.extractall(self.temp_dir)
                    self.log_message(f"tar.gz文件解压成功: {os.path.basename(source_file)}")
            elif file_ext == '.zip':
                # 处理.zip文件
                with zipfile.ZipFile(source_file, 'r') as zip_ref:
                    zip_ref.extractall(self.temp_dir)
                    self.log_message(f"zip文件解压成功: {os.path.basename(source_file)}")
            elif file_ext == '.rar':
                # 处理.rar文件
                if not RARFILE_AVAILABLE:
                    raise ValueError("RAR文件支持不可用，请安装rarfile库")
                with rarfile.RarFile(source_file) as rar_ref:
                    rar_ref.extractall(self.temp_dir)
                    self.log_message(f"rar文件解压成功: {os.path.basename(source_file)}")
            elif file_ext == '.7z':
                # 处理.7z文件
                self.extract_7z_file(source_file, self.temp_dir)
            else:
                raise ValueError(f"不支持的文件格式: {file_ext}")
                
        except Exception as e:
            raise Exception(f"解压文件失败 {os.path.basename(source_file)}: {str(e)}")
            
    def extract_main_archive(self):
        """解压主压缩包（保持向后兼容）"""
        if hasattr(self, 'source_file') and self.source_file:
            self.extract_single_archive(self.source_file)
        else:
            raise ValueError("未设置源文件")
            
    def process_internal_archives(self):
        """处理内部压缩文件（增强版）"""
        self.log_message("开始处理内部压缩文件...")
        
        # 步骤1: 智能格式检测和转换
        self.smart_format_detection_and_conversion()
        
        # 步骤2: 传统的.666z重命名（向后兼容）
        self.rename_666z_files()
        
        # 步骤3: 递归搜索所有压缩文件
        archive_files = []
        for root, dirs, files in os.walk(self.temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = Path(file).suffix.lower()
                
                # 扩展支持的格式
                supported_extensions = ['.zip', '.rar', '.7z', '.tar.bz2', '.tar.xz', '.001']
                if file_ext in supported_extensions or file.endswith('.tar.gz'):
                    archive_files.append(file_path)
                    
        self.log_message(f"发现 {len(archive_files)} 个内部压缩文件")
        
        # 步骤4: 解压每个压缩文件
        successful_extractions = 0
        for i, archive_file in enumerate(archive_files):
            try:
                self.log_message(f"解压内部文件 ({i+1}/{len(archive_files)}): {os.path.basename(archive_file)}")
                
                # 创建解压目录
                extract_dir = os.path.splitext(archive_file)[0] + "_extracted"
                os.makedirs(extract_dir, exist_ok=True)
                
                # 根据文件类型解压
                success = self.extract_archive_file(archive_file, extract_dir)
                if success:
                    successful_extractions += 1
                    # 将原压缩文件添加到清理列表
                    self.cleanup_files.append(archive_file)
                
            except Exception as e:
                self.log_message(f"解压文件失败 {os.path.basename(archive_file)}: {str(e)}")
                continue
        
        self.log_message(f"内部压缩文件处理完成，成功解压 {successful_extractions}/{len(archive_files)} 个文件")
                
    def smart_format_detection_and_conversion(self):
        """智能文件格式检测和转换"""
        if not self.smart_format_detection.get():
            return
            
        self.log_message("开始智能文件格式检测和转换...")
        
        converted_count = 0
        for root, dirs, files in os.walk(self.temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                converted = False
                
                # 检查是否需要格式转换
                for wrong_ext, correct_ext in self.format_mapping.items():
                    if file.endswith(wrong_ext):
                        new_name = file[:-len(wrong_ext)] + correct_ext
                        new_path = os.path.join(root, new_name)
                        
                        try:
                            os.rename(file_path, new_path)
                            self.log_message(f"格式转换: {file} -> {new_name}")
                            converted_count += 1
                            converted = True
                            break
                        except Exception as e:
                            self.log_message(f"格式转换失败 {file}: {str(e)}")
                
                # 如果没有进行格式转换，尝试通过文件头检测真实格式
                if not converted:
                    self.detect_and_fix_format(file_path)
                    
        self.log_message(f"智能格式检测完成，共转换了 {converted_count} 个文件")
        
    def detect_and_fix_format(self, file_path):
        """通过文件头检测并修正文件格式"""
        try:
            with open(file_path, 'rb') as f:
                header = f.read(16)
                
            file_dir = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            name_without_ext = os.path.splitext(file_name)[0]
            
            # 检测常见压缩格式的文件头
            if header.startswith(b'PK'):
                # ZIP格式
                if not file_name.lower().endswith('.zip'):
                    new_path = os.path.join(file_dir, name_without_ext + '.zip')
                    os.rename(file_path, new_path)
                    self.log_message(f"检测到ZIP格式，重命名: {file_name} -> {os.path.basename(new_path)}")
                    
            elif header.startswith(b'Rar!'):
                # RAR格式
                if not file_name.lower().endswith('.rar'):
                    new_path = os.path.join(file_dir, name_without_ext + '.rar')
                    os.rename(file_path, new_path)
                    self.log_message(f"检测到RAR格式，重命名: {file_name} -> {os.path.basename(new_path)}")
                    
            elif header.startswith(b'7z\xbc\xaf\x27\x1c'):
                # 7Z格式
                if not file_name.lower().endswith('.7z'):
                    new_path = os.path.join(file_dir, name_without_ext + '.7z')
                    os.rename(file_path, new_path)
                    self.log_message(f"检测到7Z格式，重命名: {file_name} -> {os.path.basename(new_path)}")
                    
            elif header.startswith(b'\x1f\x8b'):
                # GZIP格式
                if not file_name.lower().endswith(('.gz', '.tar.gz')):
                    new_path = os.path.join(file_dir, name_without_ext + '.gz')
                    os.rename(file_path, new_path)
                    self.log_message(f"检测到GZIP格式，重命名: {file_name} -> {os.path.basename(new_path)}")
                    
        except Exception as e:
            # 文件头检测失败，不影响主流程
            pass

    def rename_666z_files(self):
        """重命名.666z文件为.7z（保持向后兼容）"""
        self.log_message("搜索并重命名.666z文件...")
        
        renamed_count = 0
        for root, dirs, files in os.walk(self.temp_dir):
            for file in files:
                if file.endswith('.666z'):
                    old_path = os.path.join(root, file)
                    new_path = os.path.join(root, file[:-5] + '.7z')  # 替换.666z为.7z
                    
                    try:
                        os.rename(old_path, new_path)
                        self.log_message(f"重命名: {file} -> {os.path.basename(new_path)}")
                        renamed_count += 1
                    except Exception as e:
                        self.log_message(f"重命名失败 {file}: {str(e)}")
                        
        self.log_message(f"共重命名了 {renamed_count} 个.666z文件")
        
    def extract_archive_file(self, archive_path, extract_dir):
        """解压单个压缩文件（增强版）"""
        file_ext = Path(archive_path).suffix.lower()
        filename = os.path.basename(archive_path)
        
        try:
            if file_ext == '.zip':
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                self.log_message(f"ZIP文件解压成功: {filename}")
                return True
                
            elif file_ext == '.rar':
                if not RARFILE_AVAILABLE:
                    raise ValueError("RAR文件支持不可用，请安装rarfile库")
                with rarfile.RarFile(archive_path) as rar_ref:
                    rar_ref.extractall(extract_dir)
                self.log_message(f"RAR文件解压成功: {filename}")
                return True
                
            elif file_ext == '.7z' or file_ext == '.001':
                # .001文件通常是7z分卷压缩的第一部分
                return self.extract_7z_file(archive_path, extract_dir)
                
            elif archive_path.endswith('.tar.gz'):
                with tarfile.open(archive_path, 'r:gz') as tar:
                    tar.extractall(extract_dir)
                self.log_message(f"TAR.GZ文件解压成功: {filename}")
                return True
                
            elif archive_path.endswith('.tar.bz2'):
                with tarfile.open(archive_path, 'r:bz2') as tar:
                    tar.extractall(extract_dir)
                self.log_message(f"TAR.BZ2文件解压成功: {filename}")
                return True
                
            elif archive_path.endswith('.tar.xz'):
                with tarfile.open(archive_path, 'r:xz') as tar:
                    tar.extractall(extract_dir)
                self.log_message(f"TAR.XZ文件解压成功: {filename}")
                return True
                
            else:
                raise ValueError(f"不支持的压缩格式: {file_ext}")
                
        except Exception as e:
            self.log_message(f"解压文件失败 {filename}: {str(e)}")
            # 添加到失败列表
            self.failed_files.append(archive_path)
            self.failed_reasons[archive_path] = str(e)
            return False
            
    def extract_7z_file(self, archive_path, extract_dir):
        """解压7z文件（增强密码支持和交互式处理）"""
        if not PY7ZR_AVAILABLE:
            raise ValueError("7z文件支持不可用，请安装py7zr库")
        
        # 准备密码列表
        passwords_to_try = []
        
        # 添加默认密码
        default_password = self.password_var.get().strip()
        if default_password:
            passwords_to_try.append(default_password)
        
        # 添加备用密码
        backup_passwords = self.backup_passwords_var.get().strip()
        if backup_passwords:
            for pwd in backup_passwords.split(','):
                pwd = pwd.strip()
                if pwd and pwd not in passwords_to_try:
                    passwords_to_try.append(pwd)
        
        # 添加常用密码
        common_passwords = ["", "123456", "password", "admin", "123", "000000"]
        for pwd in common_passwords:
            if pwd not in passwords_to_try:
                passwords_to_try.append(pwd)
        
        # 尝试解压
        last_error = None
        for i, password in enumerate(passwords_to_try):
            try:
                if password == "":
                    # 无密码尝试
                    with py7zr.SevenZipFile(archive_path, mode="r") as archive:
                        archive.extractall(path=extract_dir)
                        self.log_message(f"7z文件解压成功（无密码）: {os.path.basename(archive_path)}")
                        return True
                else:
                    # 有密码尝试
                    with py7zr.SevenZipFile(archive_path, mode="r", password=password) as archive:
                        archive.extractall(path=extract_dir)
                        self.log_message(f"7z文件解压成功（密码: {password}）: {os.path.basename(archive_path)}")
                        return True
                        
            except Exception as e:
                last_error = e
                if i == 0:
                    self.log_message(f"尝试密码 '{password}' 失败: {str(e)}")
                continue
        
        # 所有密码都失败了
        filename = os.path.basename(archive_path)
        self.log_message(f"7z文件解压失败，所有密码都无效: {filename}")
        
        # 添加到失败列表
        self.failed_files.append(archive_path)
        self.failed_reasons[archive_path] = f"密码错误或文件损坏: {str(last_error)}"
        
        # 如果启用了交互式失败处理
        if self.interactive_failure_handling.get():
            return self.handle_7z_extraction_failure(archive_path, extract_dir, last_error)
        else:
            raise Exception(f"7z文件解压失败: {filename} - 所有密码尝试都失败")
    
    def handle_7z_extraction_failure(self, archive_path, extract_dir, last_error):
        """处理7z解压失败的交互式对话"""
        filename = os.path.basename(archive_path)
        
        # 创建失败处理对话框
        failure_dialog = tk.Toplevel(self.root)
        failure_dialog.title(f"解压失败 - {filename}")
        failure_dialog.geometry("500x300")
        failure_dialog.transient(self.root)
        failure_dialog.grab_set()
        
        # 主框架
        main_frame = ttk.Frame(failure_dialog, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 错误信息
        ttk.Label(main_frame, text=f"文件解压失败: {filename}", font=('Arial', 12, 'bold')).pack(pady=(0, 10))
        ttk.Label(main_frame, text=f"错误信息: {str(last_error)}", wraplength=450).pack(pady=(0, 15))
        
        # 选项
        ttk.Label(main_frame, text="请选择处理方式:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        action_var = tk.StringVar(value="manual_password")
        ttk.Radiobutton(main_frame, text="手动输入密码重试", variable=action_var, value="manual_password").pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(main_frame, text="跳过此文件", variable=action_var, value="skip").pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(main_frame, text="稍后处理", variable=action_var, value="later").pack(anchor=tk.W, pady=2)
        
        # 密码输入框
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Label(password_frame, text="新密码:").pack(side=tk.LEFT)
        manual_password_var = tk.StringVar()
        ttk.Entry(password_frame, textvariable=manual_password_var, show="*", width=20).pack(side=tk.LEFT, padx=(10, 0))
        
        # 结果变量
        dialog_result = {"action": None, "password": None}
        
        def on_confirm():
            dialog_result["action"] = action_var.get()
            dialog_result["password"] = manual_password_var.get()
            failure_dialog.destroy()
        
        def on_cancel():
            dialog_result["action"] = "skip"
            failure_dialog.destroy()
        
        # 按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(15, 0))
        ttk.Button(button_frame, text="确定", command=on_confirm).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="跳过", command=on_cancel).pack(side=tk.RIGHT)
        
        # 等待用户选择
        failure_dialog.wait_window()
        
        # 处理用户选择
        if dialog_result["action"] == "manual_password":
            new_password = dialog_result["password"]
            if new_password:
                try:
                    with py7zr.SevenZipFile(archive_path, mode="r", password=new_password) as archive:
                        archive.extractall(path=extract_dir)
                        self.log_message(f"7z文件解压成功（手动密码）: {filename}")
                        # 从失败列表中移除
                        if archive_path in self.failed_files:
                            self.failed_files.remove(archive_path)
                        if archive_path in self.failed_reasons:
                            del self.failed_reasons[archive_path]
                        return True
                except Exception as e:
                    self.log_message(f"手动密码也失败: {filename} - {str(e)}")
                    messagebox.showerror("解压失败", f"手动输入的密码也无效:\n{str(e)}")
        
        elif dialog_result["action"] == "later":
            self.log_message(f"文件标记为稍后处理: {filename}")
            return False
        
        # 默认跳过
        self.log_message(f"跳过文件: {filename}")
        return False
                
    def extract_mp4_files_to_unified_dir(self):
        """递归搜索并提取MP4文件到统一目录"""
        self.log_message("搜索当前临时目录中的MP4文件...")
        
        mp4_files = []
        for root, dirs, files in os.walk(self.temp_dir):
            for file in files:
                if file.lower().endswith('.mp4'):
                    mp4_files.append(os.path.join(root, file))
                    
        self.log_message(f"在当前文件中发现 {len(mp4_files)} 个MP4文件")
        
        # 复制MP4文件到统一输出目录
        for i, mp4_file in enumerate(mp4_files):
            try:
                filename = os.path.basename(mp4_file)
                output_path = os.path.join(self.unified_output_dir, filename)
                
                # 如果文件已存在，添加序号
                counter = 1
                original_name, ext = os.path.splitext(filename)
                while os.path.exists(output_path):
                    output_path = os.path.join(self.unified_output_dir, f"{original_name}_{counter}{ext}")
                    counter += 1
                    
                shutil.copy2(mp4_file, output_path)
                self.mp4_files.append(output_path)
                self.log_message(f"复制MP4文件: {filename}")
                
            except Exception as e:
                self.log_message(f"复制MP4文件失败 {filename}: {str(e)}")
                
    def extract_mp4_files(self):
        """递归搜索并提取所有MP4文件（保持向后兼容）"""
        self.log_message("开始搜索MP4文件...")
        
        mp4_files = []
        for root, dirs, files in os.walk(self.temp_dir):
            for file in files:
                if file.lower().endswith('.mp4'):
                    mp4_files.append(os.path.join(root, file))
                    
        self.log_message(f"发现 {len(mp4_files)} 个MP4文件")
        
        # 复制MP4文件到输出目录
        mp4_output_dir = os.path.join(self.output_dir, "extracted_mp4_files")
        os.makedirs(mp4_output_dir, exist_ok=True)
        
        for i, mp4_file in enumerate(mp4_files):
            try:
                filename = os.path.basename(mp4_file)
                output_path = os.path.join(mp4_output_dir, filename)
                
                # 如果文件已存在，添加序号
                counter = 1
                while os.path.exists(output_path):
                    name, ext = os.path.splitext(filename)
                    output_path = os.path.join(mp4_output_dir, f"{name}_{counter}{ext}")
                    counter += 1
                    
                shutil.copy2(mp4_file, output_path)
                self.mp4_files.append(output_path)
                self.log_message(f"复制MP4文件 ({i+1}/{len(mp4_files)}): {filename}")
                
            except Exception as e:
                self.log_message(f"复制MP4文件失败 {filename}: {str(e)}")
                
    def cleanup_current_temp_files(self):
        """清理当前文件的临时文件"""
        try:
            # 删除当前临时目录
            if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                self.log_message(f"删除临时目录: {os.path.basename(self.temp_dir)}")
                
        except Exception as e:
            self.log_message(f"清理当前临时文件时发生错误: {str(e)}")
            
    def final_cleanup(self):
        """最终清理所有中间文件"""
        self.log_message("开始最终清理...")
        
        try:
            # 删除所有中间文件
            for file_path in self.cleanup_files:
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        self.log_message(f"删除中间文件: {os.path.basename(file_path)}")
                except Exception as e:
                    self.log_message(f"删除文件失败 {os.path.basename(file_path)}: {str(e)}")
                    
            # 清理可能残留的临时目录
            for root, dirs, files in os.walk(self.output_dir):
                for dir_name in dirs:
                    if dir_name.startswith('temp_'):
                        temp_path = os.path.join(root, dir_name)
                        try:
                            shutil.rmtree(temp_path)
                            self.log_message(f"清理残留临时目录: {dir_name}")
                        except Exception as e:
                            self.log_message(f"清理临时目录失败 {dir_name}: {str(e)}")
                break  # 只检查顶层目录
                    
        except Exception as e:
            self.log_message(f"最终清理过程中发生错误: {str(e)}")
            
    def cleanup_temp_files(self):
        """清理临时文件和中间压缩文件（保持向后兼容）"""
        self.log_message("开始清理临时文件...")
        
        try:
            # 删除临时目录
            if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                self.log_message(f"删除临时目录: {self.temp_dir}")
                
            # 删除其他中间文件
            for file_path in self.cleanup_files:
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        self.log_message(f"删除中间文件: {os.path.basename(file_path)}")
                except Exception as e:
                    self.log_message(f"删除文件失败 {os.path.basename(file_path)}: {str(e)}")
                    
        except Exception as e:
            self.log_message(f"清理过程中发生错误: {str(e)}")
            
    def show_results(self):
        """显示处理结果"""
        if len(self.source_files) > 1:
            # 批量处理结果
            result_msg = f"批量处理完成！\n\n"
            result_msg += f"处理的文件数量: {len(self.source_files)}\n"
            result_msg += f"提取的MP4文件数量: {len(self.mp4_files)}\n"
            result_msg += f"统一输出目录: {getattr(self, 'unified_output_dir', self.output_dir)}\n\n"
            
            if self.mp4_files:
                result_msg += "提取的MP4文件:\n"
                for mp4_file in self.mp4_files[:10]:  # 只显示前10个
                    result_msg += f"- {os.path.basename(mp4_file)}\n"
                if len(self.mp4_files) > 10:
                    result_msg += f"... 还有 {len(self.mp4_files) - 10} 个文件\n"
            else:
                result_msg += "未找到MP4文件\n"
                
            result_msg += f"\n处理的源文件:\n"
            for i, source_file in enumerate(self.source_files[:5]):  # 显示前5个
                result_msg += f"- {os.path.basename(source_file)}\n"
            if len(self.source_files) > 5:
                result_msg += f"... 还有 {len(self.source_files) - 5} 个文件\n"
        else:
            # 单文件处理结果（向后兼容）
            source_name = os.path.basename(self.source_files[0]) if self.source_files else "未知文件"
            result_msg = f"处理完成！\n\n"
            result_msg += f"源文件: {source_name}\n"
            result_msg += f"输出目录: {self.output_dir}\n"
            result_msg += f"提取的MP4文件数量: {len(self.mp4_files)}\n\n"
            
            if self.mp4_files:
                result_msg += "提取的MP4文件:\n"
                for mp4_file in self.mp4_files[:10]:  # 只显示前10个
                    result_msg += f"- {os.path.basename(mp4_file)}\n"
                if len(self.mp4_files) > 10:
                    result_msg += f"... 还有 {len(self.mp4_files) - 10} 个文件\n"
                
        messagebox.showinfo("处理完成", result_msg)
        
    def setup_individual_output_directory(self, source_file):
        """为单个文件设置独立输出目录"""
        # 获取用户配置的输出目录，如果没有则使用默认目录
        individual_output_dir = self.file_output_dirs.get(source_file, self.output_dir)
        
        # 创建以文件名命名的子目录
        filename_without_ext = os.path.splitext(os.path.basename(source_file))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_individual_output_dir = os.path.join(individual_output_dir, f"{filename_without_ext}_{timestamp}")
        os.makedirs(self.current_individual_output_dir, exist_ok=True)
        
        self.log_message(f"创建独立输出目录: {self.current_individual_output_dir}")
    
    def extract_mp4_files_to_individual_dir(self, source_file):
        """提取MP4文件到独立目录"""
        self.log_message("搜索当前临时目录中的MP4文件...")
        
        mp4_files = []
        for root, dirs, files in os.walk(self.temp_dir):
            for file in files:
                if file.lower().endswith('.mp4'):
                    mp4_files.append(os.path.join(root, file))
                    
        self.log_message(f"在当前文件中发现 {len(mp4_files)} 个MP4文件")
        
        # 复制MP4文件到独立输出目录
        for i, mp4_file in enumerate(mp4_files):
            try:
                filename = os.path.basename(mp4_file)
                output_path = os.path.join(self.current_individual_output_dir, filename)
                
                # 如果文件已存在，添加序号
                counter = 1
                original_name, ext = os.path.splitext(filename)
                while os.path.exists(output_path):
                    output_path = os.path.join(self.current_individual_output_dir, f"{original_name}_{counter}{ext}")
                    counter += 1
                    
                shutil.copy2(mp4_file, output_path)
                self.mp4_files.append(output_path)
                self.log_message(f"复制MP4文件: {filename}")
                
            except Exception as e:
                self.log_message(f"复制MP4文件失败 {filename}: {str(e)}")
    
    def handle_failed_files(self):
        """处理失败的文件"""
        if not self.failed_files:
            return
            
        self.log_message(f"开始处理 {len(self.failed_files)} 个失败的文件...")
        
        # 创建失败文件处理对话框
        failure_dialog = tk.Toplevel(self.root)
        failure_dialog.title("处理失败的文件")
        failure_dialog.geometry("700x500")
        failure_dialog.transient(self.root)
        failure_dialog.grab_set()
        
        # 主框架
        main_frame = ttk.Frame(failure_dialog, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text=f"发现 {len(self.failed_files)} 个处理失败的文件",
                 font=('Arial', 14, 'bold')).pack(pady=(0, 15))
        
        # 创建失败文件列表
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # 列表框和滚动条
        failed_listbox = tk.Listbox(list_frame, height=10)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=failed_listbox.yview)
        failed_listbox.configure(yscrollcommand=scrollbar.set)
        
        failed_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 填充失败文件列表
        for failed_file in self.failed_files:
            filename = os.path.basename(failed_file)
            reason = self.failed_reasons.get(failed_file, "未知错误")
            failed_listbox.insert(tk.END, f"{filename} - {reason}")
        
        # 选项框架
        options_frame = ttk.LabelFrame(main_frame, text="处理选项", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        action_var = tk.StringVar(value="save_list")
        ttk.Radiobutton(options_frame, text="保存失败列表到文件", variable=action_var, value="save_list").pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(options_frame, text="忽略所有失败的文件", variable=action_var, value="ignore_all").pack(anchor=tk.W, pady=2)
        
        # 结果变量
        dialog_result = {"action": None}
        
        def on_confirm():
            dialog_result["action"] = action_var.get()
            failure_dialog.destroy()
        
        def on_cancel():
            dialog_result["action"] = "ignore_all"
            failure_dialog.destroy()
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="确定", command=on_confirm).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="忽略", command=on_cancel).pack(side=tk.RIGHT)
        
        # 等待用户选择
        failure_dialog.wait_window()
        
        # 处理用户选择
        if dialog_result["action"] == "save_list":
            self.save_failed_files_list()
        
        self.log_message("失败文件处理完成")
    
    def save_failed_files_list(self):
        """保存失败文件列表到文件"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            failed_list_file = os.path.join(self.desktop_path, f"失败文件列表_{timestamp}.txt")
            
            with open(failed_list_file, 'w', encoding='utf-8') as f:
                f.write(f"处理失败的文件列表 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
                
                for i, failed_file in enumerate(self.failed_files, 1):
                    filename = os.path.basename(failed_file)
                    reason = self.failed_reasons.get(failed_file, "未知错误")
                    f.write(f"{i}. {filename}\n")
                    f.write(f"   路径: {failed_file}\n")
                    f.write(f"   失败原因: {reason}\n\n")
            
            self.log_message(f"失败文件列表已保存到: {failed_list_file}")
            messagebox.showinfo("保存成功", f"失败文件列表已保存到:\n{failed_list_file}")
            
        except Exception as e:
            self.log_message(f"保存失败文件列表时出错: {str(e)}")
            messagebox.showerror("保存失败", f"保存失败文件列表时出错:\n{str(e)}")

    def run(self):
        """运行应用程序"""
        self.log_message("桌面自动化脚本已启动")
        self.log_message("请点击'添加文件'选择要处理的压缩包文件（支持批量选择）")
        self.log_message("新功能: 支持个性化输出目录、智能格式检测、交互式失败处理")
        self.root.mainloop()

def main():
    """主函数"""
    try:
        # 检查必要的依赖库
        required_modules = ['py7zr', 'rarfile']
        missing_modules = []
        
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing_modules.append(module)
                
        if missing_modules:
            print("缺少必要的依赖库，正在尝试安装...")
            for module in missing_modules:
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", module])
                    print(f"成功安装 {module}")
                except subprocess.CalledProcessError:
                    print(f"安装 {module} 失败，请手动安装")
                    
        # 启动应用程序
        app = DesktopAutomationTool()
        app.run()
        
    except Exception as e:
        print(f"程序启动失败: {str(e)}")
        input("按回车键退出...")

if __name__ == "__main__":
    main()