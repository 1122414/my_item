## tmux相关：

~~~bash
# 创建新会话：
tmux new -s session_name

# 列出会话：
tmux ls

# 接入会话
tmux at -t my-session

# 杀死会话
tmux kill-session -t session_name

# 杀死所有会话
tmux kill-server

# 退出
ctrl + d(exit)

# 脱离会话
ctrl + b d

# 创建窗口
ctrl b c

# 切换窗口
ctrl b n(下一个)
ctrl b p(上一个)
ctrl b <数字> 指定窗口

# 重命名窗口
ctrl b

# 关闭窗口
ctrl b &

# 关闭指定窗口
tmux kill-window -t 1 -t 2

# 查看窗口列表
ctrl b w
~~~



