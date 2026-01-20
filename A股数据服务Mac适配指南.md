# A股数据服务Mac适配指南

## 概述

本指南提供在Mac系统上适配A股数据服务（RQData、XT等）的详细步骤和工具。

## 前置条件

1. **Mac系统**：macOS 10.14+（支持Intel x86_64和Apple Silicon M系列）
2. **Python环境**：Python 3.9+
3. **VNPY核心框架**：已安装并配置完成

## 适配工具

### platform_utils.py

位置：`vnpy/trader/platform_utils.py`

提供Mac系统检测和动态库处理工具，可用于数据服务的Mac适配。

## 适配步骤

### 步骤1：下载数据服务模块

#### 1.1 下载vnpy_rqdata模块

```bash
# 克隆vnpy_rqdata仓库
cd ~/Downloads/mac逆向
git clone https://github.com/vnpy/vnpy_rqdata.git

# 或下载ZIP包
# 访问 https://github.com/vnpy/vnpy_rqdata/releases
# 下载最新版本的源码包
```

#### 1.2 下载vnpy_xt模块

```bash
# 克隆vnpy_xt仓库
cd ~/Downloads/mac逆向
git clone https://github.com/vnpy/vnpy_xt.git

# 或下载ZIP包
# 访问 https://github.com/vnpy/vnpy_xt/releases
# 下载最新版本的源码包
```

### 步骤2：检查Mac兼容性

#### 2.1 检查vnpy_rqdata Mac兼容性

RQData数据服务通常使用Python标准库和第三方库，Mac兼容性较好。需要检查：

1. **网络连接**：确保能正常连接到RQData服务器
2. **依赖库**：检查所需依赖是否在Mac上正常安装
3. **文件编码**：确保配置文件使用UTF-8编码

检查方法：

```bash
# 进入vnpy_rqdata目录
cd vnpy_rqdata

# 检查Python版本
python3 --version

# 检查依赖
pip3 list | grep -i rqdata

# 检查配置文件编码
file -I vnpy_rqdata/config.py
```

#### 2.2 检查vnpy_xt Mac兼容性

XT（迅投研）数据服务需要检查：

1. **API连接**：确保Mac系统能正常连接XT API服务器
2. **SSL证书**：Mac系统SSL证书配置
3. **时区设置**：确保时区设置正确

检查方法：

```bash
# 进入vnpy_xt目录
cd vnpy_xt

# 检查网络连接
curl -I https://api.xt.com

# 检查SSL证书
python3 -c "import ssl; print(ssl.get_default_verify_paths())"
```

### 步骤3：修复Mac特定问题

#### 3.1 RQData Mac适配

RQData通常不需要特殊适配，但可以优化：

1. **配置文件路径**：使用Mac标准路径
2. **日志文件路径**：使用Mac用户目录
3. **缓存路径**：使用Mac临时目录

示例代码：

```python
import os
import platform
from pathlib import Path

def get_mac_config_path():
    """获取Mac系统配置路径"""
    if platform.system() == "Darwin":
        # Mac系统使用用户目录
        config_dir = Path.home() / ".vnpy" / "rqdata"
        config_dir.mkdir(parents=True, exist_ok=True)
        return str(config_dir / "config.json")
    else:
        # 其他系统使用默认路径
        return "config.json"

def get_mac_cache_path():
    """获取Mac系统缓存路径"""
    if platform.system() == "Darwin":
        cache_dir = Path.home() / "Library" / "Caches" / "vnpy_rqdata"
        cache_dir.mkdir(parents=True, exist_ok=True)
        return str(cache_dir)
    else:
        return "/tmp/vnpy_rqdata"
```

#### 3.2 XT Mac适配

XT数据服务可能需要处理：

1. **SSL验证**：Mac系统SSL验证配置
2. **代理设置**：如果需要代理访问
3. **超时设置**：网络请求超时配置

示例代码：

```python
import ssl
import platform
from urllib.request import Request, urlopen

def create_mac_ssl_context():
    """创建Mac系统SSL上下文"""
    if platform.system() == "Darwin":
        # Mac系统SSL配置
        context = ssl.create_default_context()
        # 可以根据需要调整SSL验证级别
        # context.check_hostname = False
        # context.verify_mode = ssl.CERT_NONE
        return context
    else:
        return ssl.create_default_context()

def make_request_with_mac_ssl(url, timeout=30):
    """使用Mac SSL配置发送请求"""
    context = create_mac_ssl_context()
    request = Request(url)
    response = urlopen(request, timeout=timeout, context=context)
    return response
```

### 步骤4：使用platform_utils工具

在数据服务模块中使用platform_utils进行Mac检测：

```python
from vnpy.trader.platform_utils import is_mac_system

class RqdataDatafeed:
    def __init__(self):
        if is_mac_system():
            # Mac特定配置
            self.config_path = self._get_mac_config_path()
            self.cache_path = self._get_mac_cache_path()
        else:
            # 其他系统配置
            self.config_path = "config.json"
            self.cache_path = "/tmp/rqdata"
    
    def _get_mac_config_path(self):
        """获取Mac配置路径"""
        from pathlib import Path
        config_dir = Path.home() / ".vnpy" / "rqdata"
        config_dir.mkdir(parents=True, exist_ok=True)
        return str(config_dir / "config.json")
    
    def _get_mac_cache_path(self):
        """获取Mac缓存路径"""
        from pathlib import Path
        cache_dir = Path.home() / "Library" / "Caches" / "vnpy_rqdata"
        cache_dir.mkdir(parents=True, exist_ok=True)
        return str(cache_dir)
```

### 步骤5：测试数据获取

#### 5.1 测试RQData连接

```python
# test_rqdata_mac.py
from vnpy.trader.platform_utils import is_mac_system

def test_rqdata_connection():
    """测试RQData连接"""
    try:
        from vnpy_rqdata import RqdataDatafeed
        
        datafeed = RqdataDatafeed()
        
        # 测试连接
        if datafeed.connect():
            print("✓ RQData连接成功")
            
            # 测试获取数据
            bars = datafeed.query_bar_history(
                symbol="000001.SZ",
                exchange="SZSE",
                interval="1d",
                start=datetime(2024, 1, 1),
                end=datetime(2024, 1, 31)
            )
            
            if bars:
                print(f"✓ 成功获取 {len(bars)} 条K线数据")
                return True
            else:
                print("✗ 未获取到数据")
                return False
        else:
            print("✗ RQData连接失败")
            return False
            
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print(f"当前系统: {'Mac' if is_mac_system() else '非Mac'}")
    test_rqdata_connection()
```

#### 5.2 测试XT连接

```python
# test_xt_mac.py
from vnpy.trader.platform_utils import is_mac_system

def test_xt_connection():
    """测试XT连接"""
    try:
        from vnpy_xt import XtDatafeed
        
        datafeed = XtDatafeed()
        
        # 测试连接
        if datafeed.connect():
            print("✓ XT连接成功")
            
            # 测试获取数据
            bars = datafeed.query_bar_history(
                symbol="000001",
                exchange="SZSE",
                interval="1d",
                start=datetime(2024, 1, 1),
                end=datetime(2024, 1, 31)
            )
            
            if bars:
                print(f"✓ 成功获取 {len(bars)} 条K线数据")
                return True
            else:
                print("✗ 未获取到数据")
                return False
        else:
            print("✗ XT连接失败")
            return False
            
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print(f"当前系统: {'Mac' if is_mac_system() else '非Mac'}")
    test_xt_connection()
```

## 常见问题

### Q1: RQData连接超时

**原因**：
- 网络连接问题
- 防火墙阻止
- 服务器地址配置错误

**解决**：
1. 检查网络连接：`ping api.ricequant.com`
2. 检查防火墙设置
3. 验证服务器地址配置

### Q2: XT SSL证书验证失败

**原因**：
- Mac系统SSL证书配置问题
- 证书链不完整

**解决**：
```python
# 在XT数据服务中调整SSL验证
import ssl

context = ssl.create_default_context()
# 如果需要，可以临时禁用SSL验证（仅用于测试）
# context.check_hostname = False
# context.verify_mode = ssl.CERT_NONE
```

### Q3: 数据格式不匹配

**原因**：
- A股代码格式问题
- 交易所代码映射错误

**解决**：
1. 确保使用正确的A股代码格式（如：000001.SZ）
2. 检查交易所代码映射（SSE/SZSE）

## 参考资源

1. **VNPY官方文档**：https://www.vnpy.com/docs
2. **RQData文档**：https://www.ricequant.com/doc
3. **XT文档**：联系迅投研获取
4. **Mac安装指南**：`docs/community/install/mac_install.md`

## 注意事项

1. **不改动核心逻辑**：仅修复Mac兼容性问题
2. **保持向后兼容**：适配代码不影响Windows/Linux系统
3. **错误处理完善**：提供清晰的错误信息
4. **文档更新**：更新数据服务模块的README说明Mac适配情况
