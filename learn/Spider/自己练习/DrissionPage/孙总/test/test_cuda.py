import torch

print(f"PyTorch 版本: {torch.__version__}")
print(f"CUDA 可用: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA 版本: {torch.version.cuda}")
    print(f"当前 GPU: {torch.cuda.get_device_name(0)}")
else:
    print("请检查以下内容：")
    print("1. 确认已安装 NVIDIA 显卡驱动")
    print("2. 确认已安装与驱动匹配的 CUDA Toolkit")
    print("3. 确认安装的是 GPU 版 PyTorch")