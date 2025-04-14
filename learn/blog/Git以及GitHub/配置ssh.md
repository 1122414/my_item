以下是使用 GitHub SSH 的完整步骤，包括密钥生成、配置和验证：

---

### **1. 生成 SSH 密钥**
#### **Windows/Mac/Linux**
1. **打开终端**（Windows 使用 Git Bash）。
2. **生成密钥对**（替换邮箱为你的 GitHub 邮箱）：
   ```bash
   ssh-keygen #生成公钥到.ssh
   ```
   - 按回车接受默认保存路径（`~/.ssh/id_ed25519`）。
   - 设置密钥密码（可选，增强安全性）。

---

### **2. 添加公钥到 GitHub**
1. **复制公钥内容**：
   ```bash
   # Windows
   cat ~/.ssh/id_ed25519.pub | clip

   # Mac
   pbcopy < ~/.ssh/id_ed25519.pub

   # Linux
   xclip -sel clip < ~/.ssh/id_ed25519.pub
   ```
   **或手动打开文件复制**：
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

2. **粘贴到 GitHub**：
   - 登录 GitHub → **Settings** → **SSH and GPG Keys** → **New SSH Key**。
   - **Title**：自定义名称（如 `My Laptop`）。
   - **Key type**：保持默认 `Authentication Key`。
   - **Key**：粘贴复制的公钥内容（以 `ssh-ed25519` 开头）。
   - 点击 **Add SSH Key**。

---

### **3. 测试 SSH 连接**
```bash
ssh -T git@github.com
```
- 成功提示：`Hi 用户名! You've successfully authenticated...`
- **失败处理**：
  - 确保密钥已添加到 GitHub。
  - 检查 `~/.ssh` 目录权限（应为 `700`）：
    ```bash
    chmod 700 ~/.ssh
    chmod 600 ~/.ssh/id_ed25519
    ```

---

### **4. 配置 Git 使用 SSH**
#### **克隆仓库**
直接使用 SSH URL 克隆：
```bash
git clone git@github.com:用户名/仓库名.git
```

#### **修改现有仓库的远程 URL**
如果已用 HTTPS 克隆，切换为 SSH：
```bash
git remote set-url origin git@github.com:用户名/仓库名.git
```

---

### **5. 管理多个 SSH 密钥（可选）**
如果有多个 GitHub 账户或密钥：
1. **创建新密钥**（如 `~/.ssh/id_ed25519_work`）。
2. **配置 `~/.ssh/config`**：
   ```bash
   Host github-work
     HostName github.com
     User git
     IdentityFile ~/.ssh/id_ed25519_work
   ```
3. **克隆仓库时使用别名**：
   ```bash
   git clone github-work:用户名/仓库名.git
   ```

---

### **6. 常见问题解决**
#### **权限错误 `Permissions 0644 are too open`**
```bash
chmod 600 ~/.ssh/id_ed25519
```

#### **SSH 代理未启动**
```bash
# 启动代理并添加密钥
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

---

### **总结**
```bash
# 完整流程示例
ssh-keygen -t ed25519 -C "you@example.com"  # 生成密钥
cat ~/.ssh/id_ed25519.pub                  # 复制公钥到 GitHub
ssh -T git@github.com                       # 测试连接
git clone git@github.com:user/repo.git      # 克隆仓库
```

使用 SSH 后，无需每次输入密码（除非设置了密钥密码），同时避免了 HTTPS 的 403 权限问题。