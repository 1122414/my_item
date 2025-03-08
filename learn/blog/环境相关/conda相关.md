## conda相关：

### 一些conda命令：

1. 虚拟环境创建：

   conda create -n 环境名 python==3.X

2. 查看当前已创建所有虚拟环境：

   conda info --envs：

3. 查看当前环境下的包：

   conda list

4. 激活环境：

   conda activate 环境：

5. 设置默认源：

   conda config --show channels

6. 添加源：

   ~~~
   conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
   conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge 
   conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/
   ~~~

7. 退出当前已激活环境：

   conda deactivate

8. 删除虚拟环境

   conda remove -n 环境名 --all

9. 卸载第三方库：

   ~~~
   conda uninstall 包名
   pip uninstall 包名
   注：尽量使用下载该第三方库时使用的管理器进行卸载。
   ~~~

10. 

    

    

    

    

    

    

    

    

    





