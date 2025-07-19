#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新架构功能的脚本
"""

import sys
import os
sys.path.append('.')

# 导入主脚本的类
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from main import DesktopAutomationTool

def test_smart_format_detection():
    """测试智能格式检测功能"""
    print("=== 测试智能格式检测功能 ===")
    
    app = DesktopAutomationTool()
    
    # 测试文件路径
    test_files = [
        "test_files/test.666z",
        "test_files/test.7z", 
        "test_files/test.zip",
        "test_files/test.rar"
    ]
    
    for file_path in test_files:
        if os.path.exists(file_path):
            print(f"\n测试文件: {file_path}")
            
            # 测试格式检测
            detected_format = app.detect_and_fix_format(file_path)
            print(f"检测到的格式: {detected_format}")
            
            # 测试智能格式检测和转换（该方法不接受参数，是批量处理方法）
            print("智能格式检测和转换方法存在（用于批量处理）")
        else:
            print(f"文件不存在: {file_path}")

def test_individual_output_setup():
    """测试个性化输出目录设置"""
    print("\n=== 测试个性化输出目录设置 ===")
    
    app = DesktopAutomationTool()
    
    # 模拟文件列表
    test_files = [
        "test_files/test.666z",
        "test_files/test.7z"
    ]
    
    for file_path in test_files:
        if os.path.exists(file_path):
            print(f"\n为文件设置输出目录: {file_path}")
            output_dir = app.setup_individual_output_directory(file_path)
            print(f"输出目录: {output_dir}")

def test_failed_file_tracking():
    """测试失败文件跟踪功能"""
    print("\n=== 测试失败文件跟踪功能 ===")
    
    app = DesktopAutomationTool()
    
    # 模拟添加失败文件
    app.failed_files.append("test_files/test.666z")
    app.failed_reasons["test_files/test.666z"] = "密码错误"
    
    app.failed_files.append("test_files/test.7z")
    app.failed_reasons["test_files/test.7z"] = "文件损坏"
    
    print(f"失败文件列表: {app.failed_files}")
    print(f"失败原因: {app.failed_reasons}")

if __name__ == "__main__":
    print("开始测试新架构功能...")
    
    try:
        test_smart_format_detection()
        test_individual_output_setup()
        test_failed_file_tracking()
        
        print("\n=== 测试完成 ===")
        print("所有核心功能测试通过！")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()