# A股交易接口Mac适配指南

## 概述

本指南提供在Mac系统上适配A股交易接口（XTP、TORA等）的详细步骤和工具。

## 前置条件

1. **Mac系统**：macOS 10.14+（支持Intel x86_64和Apple Silicon M系列）
2. **Python环境**：Python 3.9+
3. **VNPY核心框架**：已安装并配置完成

## 适配工具

### gateway_mac_adapter.py

位置：`vnpy/trader/gateway_mac_adapter.py`

提供统一的Mac动态库加载适配器，支持：
- `.dylib`动态库加载
- `.framework`框架加载
- 自动路径搜索
- 库验证和错误处理

## 适配步骤

### 步骤1：下载Gateway模块

#### 1.1 下载vnpy_xtp模块

```bash
# 克隆vnpy_xtp仓库
cd ~/Downloads/mac逆向
git clone https://github.com/vnpy/vnpy_xtp.git

# 或下载ZIP包
# 访问 https://github.com/vnpy/vnpy_xtp/releases
# 下载最新版本的源码包
```

#### 1.2 下载vnpy_tora模块

```bash
# 克隆vnpy_tora仓库
cd ~/Downloads/mac逆向
git clone https://github.com/vnpy/vnpy_tora.git

# 或下载ZIP包
# 访问 https://github.com/vnpy/vnpy_tora/releases
# 下载最新版本的源码包
```

### 步骤2：检查Mac动态库支持

#### 2.1 检查XTP动态库

XTP接口通常提供以下动态库：
- `libxtpapi.dylib`（Mac动态库）
- `XTP.framework`（Mac框架）

检查方法：

```bash
# 进入vnpy_xtp目录
cd vnpy_xtp

# 查找动态库文件
find . -name "*.dylib" -o -name "*.framework"

# 检查库架构（Intel或Apple Silicon）
file libxtpapi.dylib
# 或
file XTP.framework/XTP
```

#### 2.2 检查TORA动态库

TORA接口通常提供：
- `libtoraapi.dylib`
- `TORA.framework`

检查方法同上。

### 步骤3：适配动态库加载

#### 3.1 使用gateway_mac_adapter适配XTP

在vnpy_xtp模块的Gateway文件中，使用适配器加载动态库：

```python
from vnpy.trader.gateway_mac_adapter import get_gateway_adapter

class XtpGateway(BaseGateway):
    def __init__(self, event_engine, gateway_name: str = "XTP"):
        super().__init__(event_engine, gateway_name)
        
        # 创建Mac适配器
        self.mac_adapter = get_gateway_adapter("XTP")
        
        # 配置库搜索路径（根据实际安装路径调整）
        self.library_paths = [
            os.path.join(os.path.dirname(__file__), "lib"),
            os.path.expanduser("~/vnpy_xtp/lib"),
        ]
    
    def connect(self, setting: dict):
        """连接"""
        try:
            # 使用适配器加载库
            lib = self.mac_adapter.load_library(
                "xtpapi",
                search_paths=self.library_paths,
                framework_name="XTP",
                required=True
            )
            
            # 后续使用lib进行API调用
            # ...
            
        except OSError as e:
            self.write_log(f"加载XTP动态库失败: {e}")
            return
```

#### 3.2 适配TORA

类似地，在vnpy_tora模块中使用适配器：

```python
from vnpy.trader.gateway_mac_adapter import get_gateway_adapter

class ToraGateway(BaseGateway):
    def __init__(self, event_engine, gateway_name: str = "TORA"):
        super().__init__(event_engine, gateway_name)
        
        self.mac_adapter = get_gateway_adapter("TORA")
        self.library_paths = [
            os.path.join(os.path.dirname(__file__), "lib"),
            os.path.expanduser("~/vnpy_tora/lib"),
        ]
    
    def connect(self, setting: dict):
        """连接"""
        try:
            lib = self.mac_adapter.load_library(
                "toraapi",
                search_paths=self.library_paths,
                framework_name="TORA",
                required=True
            )
            # ...
        except OSError as e:
            self.write_log(f"加载TORA动态库失败: {e}")
            return
```

**TORA适配要点**：
1. TORA接口通常提供`libtoraapi.dylib`或`TORA.framework`
2. 库文件通常位于vnpy_tora模块的`lib`目录下
3. 如果使用Framework格式，确保Framework结构正确
4. 检查库的架构（x86_64或arm64）与Mac系统匹配

### 步骤4：处理架构兼容性

#### 4.1 Intel x86_64架构

如果Mac是Intel芯片，需要x86_64版本的动态库：

```python
import platform

def get_library_arch():
    """获取库架构"""
    machine = platform.machine()
    if machine == "x86_64":
        return "x86_64"
    elif machine == "arm64":
        return "arm64"
    else:
        return "universal"
```

#### 4.2 Apple Silicon (M系列)架构

如果Mac是Apple Silicon，需要arm64版本的动态库。

如果接口提供商只提供x86_64版本，可以使用Rosetta 2运行：

```bash
# 使用Rosetta 2运行Python（如果需要）
arch -x86_64 python3 your_script.py
```

### 步骤5：配置库路径

#### 5.1 环境变量配置

可以在环境变量中设置库搜索路径：

```bash
# 在~/.zshrc或~/.bash_profile中添加
export VNPY_XTP_LIB_PATH="$HOME/vnpy_xtp/lib"
export VNPY_TORA_LIB_PATH="$HOME/vnpy_tora/lib"
```

#### 5.2 配置文件配置

在VNPY配置文件中设置：

```python
# 在vnpy/trader/setting.py或Gateway配置中
SETTINGS["xtp.library_path"] = "~/vnpy_xtp/lib"
SETTINGS["tora.library_path"] = "~/vnpy_tora/lib"
```

## 测试验证

### 测试脚本

创建测试脚本验证动态库加载：

```python
# test_gateway_mac.py
from vnpy.trader.gateway_mac_adapter import get_gateway_adapter

def test_xtp_adapter():
    """测试XTP适配器"""
    adapter = get_gateway_adapter("XTP")
    
    # 测试库查找
    lib_path = adapter.find_library(
        "xtpapi",
        search_paths=["~/vnpy_xtp/lib"],
        framework_name="XTP"
    )
    
    if lib_path:
        print(f"✓ 找到XTP库: {lib_path}")
        
        # 测试加载
        try:
            lib = adapter.load_library(
                "xtpapi",
                search_paths=["~/vnpy_xtp/lib"],
                framework_name="XTP"
            )
            print(f"✓ XTP库加载成功")
            return True
        except Exception as e:
            print(f"✗ XTP库加载失败: {e}")
            return False
    else:
        print("✗ 未找到XTP库")
        return False

def test_tora_adapter():
    """测试TORA适配器"""
    adapter = get_gateway_adapter("TORA")
    
    # 测试库查找
    lib_path = adapter.find_library(
        "toraapi",
        search_paths=["~/vnpy_tora/lib"],
        framework_name="TORA"
    )
    
    if lib_path:
        print(f"✓ 找到TORA库: {lib_path}")
        
        # 测试加载
        try:
            lib = adapter.load_library(
                "toraapi",
                search_paths=["~/vnpy_tora/lib"],
                framework_name="TORA"
            )
            print(f"✓ TORA库加载成功")
            return True
        except Exception as e:
            print(f"✗ TORA库加载失败: {e}")
            return False
    else:
        print("✗ 未找到TORA库")
        return False

if __name__ == "__main__":
    print("测试XTP适配器:")
    test_xtp_adapter()
    print("\n测试TORA适配器:")
    test_tora_adapter()
```

## 常见问题

### Q1: 找不到动态库

**原因**：
- 库文件不存在
- 搜索路径不正确
- 库文件权限问题

**解决**：
1. 确认库文件存在：`ls -la ~/vnpy_xtp/lib/`
2. 检查搜索路径配置
3. 检查文件权限：`chmod +r libxtpapi.dylib`

### Q2: 架构不匹配

**原因**：
- 库是x86_64，Mac是arm64（或反之）

**解决**：
1. 下载对应架构的库
2. 使用Rosetta 2（仅x86_64→arm64）

### Q3: 依赖库缺失

**原因**：
- 动态库依赖其他系统库

**解决**：
```bash
# 使用otool查看依赖
otool -L libxtpapi.dylib

# 安装缺失的依赖（如使用Homebrew）
brew install missing-library
```

## 参考资源

1. **VNPY官方文档**：https://www.vnpy.com/docs
2. **Mac安装指南**：`docs/community/install/mac_install.md`
3. **XTP官方文档**：联系中泰证券获取
4. **TORA官方文档**：联系华鑫证券获取

## 注意事项

1. **不改动Gateway核心逻辑**：仅适配动态库加载部分
2. **保持向后兼容**：适配代码不影响Windows/Linux系统
3. **错误处理完善**：提供清晰的错误信息
4. **文档更新**：更新Gateway模块的README说明Mac适配情况
