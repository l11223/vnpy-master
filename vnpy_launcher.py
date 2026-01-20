#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VNPY Mac应用启动器 - 带错误捕获和日志输出
用于PyInstaller打包后的应用启动
"""

import sys
import os
import traceback
from pathlib import Path
import logging

# 设置日志文件路径（在用户目录下）
log_dir = Path.home() / ".vntrader" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "vnpy_startup.log"

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stderr)  # 同时输出到stderr
    ]
)

logger = logging.getLogger(__name__)

def show_error_dialog(message):
    """显示错误对话框（Mac）"""
    try:
        import subprocess
        script = f'''
        tell application "System Events"
            display dialog "{message}" buttons {{"确定"}} default button "确定" with icon caution with title "VNPY启动错误"
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=False)
    except:
        pass  # 如果显示对话框失败，至少日志已记录

def main():
    """主启动函数"""
    try:
        # 立即写入日志，确保即使后续失败也能看到
        log_dir = Path.home() / ".vntrader" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "vnpy_startup.log"
        
        # 写入启动信息到文件（即使logging还没配置好）
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"启动时间: {__import__('datetime').datetime.now()}\n")
            f.write(f"Python版本: {sys.version}\n")
            f.write(f"可执行文件: {sys.executable}\n")
            f.write(f"工作目录: {os.getcwd()}\n")
            f.write(f"脚本路径: {__file__}\n")
            f.write(f"Frozen: {getattr(sys, 'frozen', False)}\n")
            f.write(f"{'='*60}\n")
        
        logger.info("=" * 60)
        logger.info("VNPY Mac量化系统启动")
        logger.info("=" * 60)
        logger.info(f"Python版本: {sys.version}")
        logger.info(f"可执行文件: {sys.executable}")
        logger.info(f"工作目录: {os.getcwd()}")
        logger.info(f"脚本路径: {__file__}")
        logger.info(f"Frozen模式: {getattr(sys, 'frozen', False)}")
        
        # 添加项目路径
        if getattr(sys, 'frozen', False):
            # PyInstaller打包后的路径
            # 在--onedir模式下，sys.executable指向MacOS目录中的可执行文件
            # 所以parent是MacOS目录，parent.parent是Contents，parent.parent.parent是.app
            executable_path = Path(sys.executable)
            logger.info(f"可执行文件路径: {executable_path}")
            logger.info(f"可执行文件父目录: {executable_path.parent}")
            
            # 在--onedir模式下，所有文件都在MacOS目录中
            project_root = executable_path.parent
            logger.info(f"项目根目录（MacOS）: {project_root}")
        else:
            # 开发模式
            project_root = Path(__file__).parent
            logger.info(f"项目根目录（开发模式）: {project_root}")
        
        # 导入并启动主程序
        logger.info("正在导入VNPY模块...")
        
        # 检查关键依赖
        try:
            import PySide6
            logger.info("✅ PySide6已导入")
        except ImportError as e:
            error_msg = f"缺少PySide6依赖: {e}\n请检查安装是否正确。"
            logger.error(error_msg)
            show_error_dialog(error_msg)
            return 1
        
        try:
            from vnpy.event import EventEngine
            from vnpy.trader.engine import MainEngine
            from vnpy.trader.ui import MainWindow, create_qapp
            logger.info("✅ VNPY核心模块已导入")
        except ImportError as e:
            error_msg = f"VNPY模块导入失败: {e}\n请检查VNPY是否正确安装。"
            logger.error(error_msg)
            logger.error(traceback.format_exc())
            show_error_dialog(error_msg)
            return 1
        
        # 创建Qt应用
        logger.info("正在创建Qt应用...")
        qapp = create_qapp("VNPY Mac量化系统")
        
        # 创建事件引擎
        logger.info("正在创建事件引擎...")
        event_engine = EventEngine()
        
        # 创建主引擎
        logger.info("正在创建主引擎...")
        main_engine = MainEngine(event_engine)
        
        # 尝试加载可选模块
        try:
            from vnpy_ctastrategy import CtaStrategyApp
            main_engine.add_app(CtaStrategyApp)
            logger.info("✅ CTA策略模块已加载")
        except ImportError:
            logger.info("ℹ️  CTA策略模块未安装（可选）")
        except Exception as e:
            logger.warning(f"⚠️  CTA策略模块加载失败: {e}")
        
        try:
            from vnpy_ctabacktester import CtaBacktesterApp
            main_engine.add_app(CtaBacktesterApp)
            logger.info("✅ CTA回测模块已加载")
        except ImportError:
            logger.info("ℹ️  CTA回测模块未安装（可选）")
        except Exception as e:
            logger.warning(f"⚠️  CTA回测模块加载失败: {e}")
        
        try:
            from vnpy_datamanager import DataManagerApp
            main_engine.add_app(DataManagerApp)
            logger.info("✅ 数据管理模块已加载")
        except ImportError:
            logger.info("ℹ️  数据管理模块未安装（可选）")
        except Exception as e:
            logger.warning(f"⚠️  数据管理模块加载失败: {e}")
        
        # 创建主窗口
        logger.info("正在创建主窗口...")
        main_window = MainWindow(main_engine, event_engine)
        main_window.showMaximized()
        
        logger.info("✅ 系统启动成功！")
        logger.info("=" * 60)
        
        # 运行应用
        return qapp.exec()
        
    except Exception as e:
        # 确保错误信息被记录
        error_msg = f"启动失败: {e}\n\n详细错误信息已保存到:\n{log_file}"
        
        # 即使logging失败，也要写入文件
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*60}\n")
                f.write("启动失败！\n")
                f.write(f"{'='*60}\n")
                f.write(f"错误: {e}\n")
                f.write(f"\n完整堆栈:\n")
                f.write(traceback.format_exc())
        except:
            pass
        
        try:
            logger.error("=" * 60)
            logger.error("启动失败！")
            logger.error("=" * 60)
            logger.error(traceback.format_exc())
        except:
            pass
        
        # 显示错误对话框
        show_error_dialog(error_msg)
        
        # 也输出到stderr（如果可能）
        try:
            print(f"错误: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
        except:
            pass
        
        return 1

if __name__ == "__main__":
    sys.exit(main())
