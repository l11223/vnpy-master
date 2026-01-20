"""
Mac系统Gateway动态库适配器

为A股交易接口（XTP、TORA等）提供Mac系统动态库加载适配。
统一处理Mac系统特有的动态库加载问题，包括.dylib和.framework的处理。
"""

import ctypes
import ctypes.util
import os
import platform
from pathlib import Path
from typing import Optional, Dict, List

from .platform_utils import (
    is_mac_system,
    get_dylib_path,
    get_framework_path,
    load_mac_library,
    find_framework_library,
    validate_mac_library
)
from .logger import logger


class GatewayMacAdapter:
    """
    Mac系统Gateway动态库适配器
    
    为A股交易接口Gateway提供Mac系统动态库加载支持。
    支持.dylib和.framework两种格式的动态库。
    """
    
    def __init__(self, gateway_name: str):
        """
        初始化适配器
        
        Args:
            gateway_name: Gateway名称（如'XTP', 'TORA'等）
        """
        self.gateway_name = gateway_name
        self.loaded_libraries: Dict[str, ctypes.CDLL] = {}
        self.library_paths: Dict[str, str] = {}
        
        if not is_mac_system():
            logger.warning(f"{gateway_name}适配器在非Mac系统上初始化")
    
    def find_library(
        self,
        lib_name: str,
        search_paths: Optional[List[str]] = None,
        framework_name: Optional[str] = None
    ) -> Optional[str]:
        """
        查找动态库路径
        
        Args:
            lib_name: 库名称（不含扩展名）
            search_paths: 搜索路径列表（可选）
            framework_name: Framework名称（可选，用于.framework格式）
            
        Returns:
            Optional[str]: 找到的库路径，如果未找到返回None
        """
        if not is_mac_system():
            # 非Mac系统，使用标准方式查找
            lib_path = ctypes.util.find_library(lib_name)
            if lib_path:
                return lib_path
            return None
        
        # Mac系统：优先查找.framework，然后查找.dylib
        
        # 1. 尝试查找Framework
        if framework_name:
            framework_path = find_framework_library(framework_name, lib_name)
            if framework_path and validate_mac_library(framework_path):
                logger.info(f"找到Framework: {framework_path}")
                return framework_path
        
        # 2. 在指定路径中查找
        if search_paths:
            for base_path in search_paths:
                # 尝试.dylib
                dylib_path = get_dylib_path(base_path, lib_name)
                if os.path.exists(dylib_path) and validate_mac_library(dylib_path):
                    logger.info(f"找到动态库: {dylib_path}")
                    return dylib_path
                
                # 尝试.framework
                if framework_name:
                    framework_path = get_framework_path(base_path, framework_name, lib_name)
                    if os.path.exists(framework_path) and validate_mac_library(framework_path):
                        logger.info(f"找到Framework: {framework_path}")
                        return framework_path
        
        # 3. 使用系统默认查找
        lib_path = ctypes.util.find_library(lib_name)
        if lib_path:
            return lib_path
        
        logger.warning(f"未找到库: {lib_name}")
        return None
    
    def load_library(
        self,
        lib_name: str,
        search_paths: Optional[List[str]] = None,
        framework_name: Optional[str] = None,
        required: bool = True
    ) -> Optional[ctypes.CDLL]:
        """
        加载动态库
        
        Args:
            lib_name: 库名称
            search_paths: 搜索路径列表
            framework_name: Framework名称
            required: 是否必需（如果必需但未找到会抛出异常）
            
        Returns:
            Optional[ctypes.CDLL]: 加载的库对象，如果未找到且非必需返回None
            
        Raises:
            OSError: 如果库是必需的但未找到或加载失败
        """
        # 检查是否已加载
        if lib_name in self.loaded_libraries:
            logger.debug(f"库 {lib_name} 已加载，返回已加载的实例")
            return self.loaded_libraries[lib_name]
        
        # 查找库路径
        lib_path = self.find_library(lib_name, search_paths, framework_name)
        
        if not lib_path:
            if required:
                error_msg = f"{self.gateway_name}: 未找到必需的库 {lib_name}"
                logger.error(error_msg)
                raise OSError(error_msg)
            else:
                logger.warning(f"{self.gateway_name}: 未找到可选库 {lib_name}")
                return None
        
        # 加载库
        try:
            if is_mac_system():
                lib = load_mac_library(lib_path)
            else:
                lib = ctypes.CDLL(lib_path)
            
            self.loaded_libraries[lib_name] = lib
            self.library_paths[lib_name] = lib_path
            
            logger.info(f"{self.gateway_name}: 成功加载库 {lib_name} from {lib_path}")
            return lib
            
        except OSError as e:
            error_msg = f"{self.gateway_name}: 加载库 {lib_name} 失败: {e}"
            logger.error(error_msg)
            if required:
                raise OSError(error_msg) from e
            return None
    
    def get_library_path(self, lib_name: str) -> Optional[str]:
        """
        获取已加载库的路径
        
        Args:
            lib_name: 库名称
            
        Returns:
            Optional[str]: 库路径，如果未加载返回None
        """
        return self.library_paths.get(lib_name)
    
    def is_library_loaded(self, lib_name: str) -> bool:
        """
        检查库是否已加载
        
        Args:
            lib_name: 库名称
            
        Returns:
            bool: 是否已加载
        """
        return lib_name in self.loaded_libraries
    
    def get_loaded_libraries(self) -> Dict[str, str]:
        """
        获取所有已加载的库及其路径
        
        Returns:
            Dict[str, str]: {库名称: 库路径}
        """
        return dict(self.library_paths)
    
    def unload_library(self, lib_name: str) -> bool:
        """
        卸载库（如果可能）
        
        Args:
            lib_name: 库名称
            
        Returns:
            bool: 是否成功卸载
        """
        if lib_name not in self.loaded_libraries:
            return False
        
        try:
            # Python的ctypes无法真正卸载已加载的库
            # 这里只是从记录中移除
            del self.loaded_libraries[lib_name]
            del self.library_paths[lib_name]
            logger.info(f"{self.gateway_name}: 从记录中移除库 {lib_name}")
            return True
        except KeyError:
            return False


def create_xtp_adapter() -> GatewayMacAdapter:
    """
    创建XTP Gateway适配器
    
    Returns:
        GatewayMacAdapter: XTP适配器实例
    """
    adapter = GatewayMacAdapter("XTP")
    
    # XTP库的典型搜索路径
    # 这些路径会在实际使用时由用户配置或从环境变量读取
    default_paths = [
        os.path.expanduser("~/vnpy_xtp/lib"),
        "/usr/local/lib",
        "/opt/vnpy_xtp/lib"
    ]
    
    # 可以在这里预配置XTP特定的库名称
    # adapter.load_library("xtp_api", default_paths, framework_name="XTP")
    
    return adapter


def create_tora_adapter() -> GatewayMacAdapter:
    """
    创建TORA Gateway适配器
    
    Returns:
        GatewayMacAdapter: TORA适配器实例
    """
    adapter = GatewayMacAdapter("TORA")
    
    # TORA库的典型搜索路径
    default_paths = [
        os.path.expanduser("~/vnpy_tora/lib"),
        "/usr/local/lib",
        "/opt/vnpy_tora/lib"
    ]
    
    return adapter


def get_gateway_adapter(gateway_name: str) -> GatewayMacAdapter:
    """
    获取指定Gateway的适配器
    
    Args:
        gateway_name: Gateway名称（'XTP', 'TORA'等）
        
    Returns:
        GatewayMacAdapter: 适配器实例
    """
    gateway_name_upper = gateway_name.upper()
    
    if gateway_name_upper == "XTP":
        return create_xtp_adapter()
    elif gateway_name_upper == "TORA":
        return create_tora_adapter()
    else:
        # 通用适配器
        return GatewayMacAdapter(gateway_name)
