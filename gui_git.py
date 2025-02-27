import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

#made by ken on 2025/02/23 --持續更新中～～

repo_path = ""
git_initialized = False  # 紀錄是否執行了 git init

import subprocess

def run_git_command(command):
    """執行 Git 指令，回傳輸出結果"""
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return result.strip()  # 確保回傳的是字串
    except subprocess.CalledProcessError as e:
        return f"error: {e.output}"  # 把錯誤當作字串回傳

def select_folder():
    """選擇本地端專案資料夾"""
    global repo_path
    repo_path = filedialog.askdirectory()
    label_folder.config(text=f"📂 當前目錄: {repo_path}", font=("Arial", 12, "bold"), fg="blue")
    btn_init.config(state="normal")  # 允許執行 Git Init

def git_init():
    """初始化 Git"""
    global git_initialized
    success = run_git_command("git init")
    if success:
        git_initialized = True
        entry_url.config(state="normal")  # 允許輸入 Repo URL
        btn_remote.config(state="normal")  # 允許按下「連結 GitHub Repo」
        entry_branch.config(state="normal")  # 允許輸入分支名稱

def git_remote_add():
    """設定 GitHub 遠端連結"""
    repo_url = entry_url.get()
    if repo_url:
        run_git_command(f"git remote add origin {repo_url}")
    else:
        messagebox.showerror("❌ 錯誤", "請輸入 GitHub Repo 連結！")

def git_pull():
    """從遠端拉取最新版本"""
    repo_url = entry_url.get().strip()  # 使用者輸入的 GitHub 連結
    branch = entry_branch.get().strip()  # 使用者輸入的分支名稱

    if not repo_url:
        messagebox.showerror("❌ 錯誤", "請輸入 GitHub Repo 連結！")
        return

    if not branch:
        branch = "main"  # 預設為 main 分支

    # 確保有遠端設定
    remote_check = run_git_command("git remote -v")
    if isinstance(remote_check, str) and "origin" not in remote_check:
        run_git_command(f"git remote add origin {repo_url}")

    # 執行 Pull 指令
    pull_output = run_git_command(f"git pull origin {branch} --allow-unrelated-histories")

    # 檢查輸出是否有錯誤
    if isinstance(pull_output, str) and "error" in pull_output.lower():
        messagebox.showerror("❌ Pull 失敗", "請檢查是否有權限或遠端是否允許拉取！")
    else:
        messagebox.showinfo("✅ Pull 成功", f"已成功拉取最新版本：{branch}")

def git_push():
    """Push 到 GitHub，確保遠端連結正確，並允許使用者輸入 commit 訊息"""
    repo_url = entry_url.get().strip()   # 使用者輸入的 GitHub 連結
    branch = entry_branch.get().strip()  # 使用者輸入的分支名稱
    commit_message = commit_message_entry.get().strip()  # 使用者輸入的 commit 訊息

    if not branch:
        branch = "main"  # 預設推送到 main 分支

    if not repo_url:
        messagebox.showerror("❌ 錯誤", "請輸入 GitHub Repo 連結！")
        return

    if not commit_message:
        commit_message = "Auto commit"  # 預設 commit 訊息

    # **1️⃣ 確保初始化**
    run_git_command("git init")

    # **2️⃣ 確保遠端存在**
    remote_check = run_git_command("git remote -v")
    if isinstance(remote_check, str) and "origin" not in remote_check:
        run_git_command(f"git remote add origin {repo_url}")

    # **3️⃣ 確保有該分支**
    branches = run_git_command("git branch")
    if isinstance(branches, str) and branch not in branches:
        run_git_command(f"git checkout -b {branch}")

    # **4️⃣ Pull 避免衝突**
    pull_result = run_git_command(f"git pull origin {branch} --allow-unrelated-histories")
    if isinstance(pull_result, str) and "error" in pull_result.lower():
        messagebox.showerror("❌ Pull 失敗", "請確認遠端是否允許 Pull！")

    # **5️⃣ 檢查是否有未提交變更**
    run_git_command("git add .")
    status_output = run_git_command("git status -s")  # 查看變更
    if not status_output.strip():
        messagebox.showinfo("✅ 沒有變更", "沒有新的變更可提交，跳過 commit！")
    else:
        run_git_command(f'git commit -m "{commit_message}"')

    # **6️⃣ 執行 Push**
    push_output = run_git_command(f"git push -u origin {branch}")
    if isinstance(push_output, str) and "error" in push_output:
        messagebox.showerror("❌ 推送失敗", "請檢查權限或遠端是否允許推送。")
    else:
        messagebox.showinfo("✅ 成功", f"Push 成功！分支：{branch}\nCommit 訊息：{commit_message}")
        
def git_clone():
    """Clone GitHub Repo"""
    repo_url = entry_url_clone.get()
    if repo_url:
        run_git_command(f"git clone {repo_url}")
    else:
        messagebox.showerror("❌ 錯誤", "請輸入 GitHub Repo 連結！")

# 設定 Tkinter 介面
root = tk.Tk()
root.title("GitHub 小機器人")
root.geometry("650x650")  # 調整視窗大小
root.configure(bg="#F8F8F8")  # 設定背景色
# Commit 訊息輸入框
tk.Label(root, text="輸入 commit 訊息:").pack()
commit_message_entry = tk.Entry(root, width=50)
commit_message_entry.pack()
commit_message_entry.insert(0, "Auto commit")  # 預設 commit 訊息

# **第一區**（Push 專案到 GitHub）
frame_push = tk.LabelFrame(root, text="📤 我在本地端寫了一個專案，想要推到 GitHub", padx=10, pady=10, bg="white", font=("Arial", 12, "bold"))
frame_push.pack(pady=10, padx=10, fill="both")

btn_select = tk.Button(frame_push, text="📂 選擇專案資料夾", command=select_folder, width=25, height=1, bg="#4CAF50", fg="black", font=("Arial", 12))
btn_select.pack(pady=5)

label_folder = tk.Label(frame_push, text="📂 當前目錄: ", fg="blue", bg="white", font=("Arial", 12, "bold"))
label_folder.pack()

btn_init = tk.Button(frame_push, text="🌱 Git Init", command=git_init, width=25, height=1, bg="#FFC107", fg="black", font=("Arial", 12), state="disabled")
btn_init.pack(pady=5)

frame_entry = tk.Frame(frame_push, bg="white")
frame_entry.pack()

label_repo_url = tk.Label(frame_entry, text="🔗 輸入你要連結的 Repo 網址:", bg="white", font=("Arial", 10))
label_repo_url.pack(side="left")

entry_url = tk.Entry(frame_entry, width=50, font=("Arial", 12), state="disabled")
entry_url.pack(side="left", pady=5)

btn_remote = tk.Button(frame_push, text="🔗 連結 GitHub Repo", command=git_remote_add, width=25, height=1, bg="#2196F3", fg="black", font=("Arial", 12), state="disabled")
btn_remote.pack(pady=5)

# **新增 Pull 最新版本**
btn_pull = tk.Button(frame_push, text="🔄 Pull 最新版本", command=git_pull, width=25, height=1, bg="#009688", fg="black", font=("Arial", 12))
btn_pull.pack(pady=5)

label_pull_hint = tk.Label(frame_push, text="📝 如果你的 Repo 內有 README.md，請先 Pull！", bg="white", font=("Arial", 10), fg="red")
label_pull_hint.pack()

frame_branch = tk.Frame(frame_push, bg="white")
frame_branch.pack()

label_branch = tk.Label(frame_branch, text="🌿 輸入你要推送的 Branch:(若空白就是預設main)", bg="white", font=("Arial", 10))
label_branch.pack(side="left")

entry_branch = tk.Entry(frame_branch, width=20, font=("Arial", 12), state="disabled")
entry_branch.pack(side="left", pady=5)

btn_push = tk.Button(frame_push, text="🚀 Push 到 GitHub", command=git_push, width=25, height=1, bg="#FF5722", fg="black", font=("Arial", 12))
btn_push.pack(pady=5)

# **第二區**（Clone / Pull Repo）
frame_clone = tk.LabelFrame(root, text="📥 我要從 GitHub 下載別人的專案", padx=10, pady=10, bg="white", font=("Arial", 12, "bold"))
frame_clone.pack(pady=10, padx=10, fill="both")

frame_clone_entry = tk.Frame(frame_clone, bg="white")
frame_clone_entry.pack()

label_clone_url = tk.Label(frame_clone_entry, text="🔗 輸入你要下載的 Repo 網址 (.git):", bg="white", font=("Arial", 10))
label_clone_url.pack(side="left")

entry_url_clone = tk.Entry(frame_clone_entry, width=50, font=("Arial", 12))
entry_url_clone.pack(side="left", pady=5)

btn_clone = tk.Button(frame_clone, text="📥 Clone Repo", command=git_clone, width=25, height=1, bg="#673AB7", fg="black", font=("Arial", 12))
btn_clone.pack(pady=5)

btn_pull = tk.Button(frame_clone, text="🔄 Pull 最新版本", command=git_pull, width=25, height=1, bg="#009688", fg="black", font=("Arial", 12))
btn_pull.pack(pady=5)

root.mainloop()