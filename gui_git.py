import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

repo_path = ""
git_initialized = False  # 用於追蹤是否已經執行 Git Init

def run_git_command(command):
    """執行 Git 指令"""
    process = subprocess.run(command, shell=True, cwd=repo_path, capture_output=True, text=True)
    if process.returncode == 0:
        messagebox.showinfo("✅ 成功", f"執行成功：\n{process.stdout}")
        return True
    else:
        messagebox.showerror("❌ 錯誤", f"執行失敗：\n{process.stderr}")
        return False

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

def git_remote_add():
    """設定 GitHub 遠端連結"""
    repo_url = entry_url.get()
    if repo_url:
        run_git_command(f"git remote add origin {repo_url}")
    else:
        messagebox.showerror("❌ 錯誤", "請輸入 GitHub Repo 連結！")

def git_push():
    """Push 到 GitHub，並根據是否有 README.md 來決定是否先 Pull"""
    if checkbox_var.get():
        # 先 Pull 遠端的 README.md，避免 push 失敗
        run_git_command("git pull origin main --rebase")
    
    # 進行 Push
    run_git_command("git add . && git commit -m 'Auto commit' && git push origin main")

def git_clone():
    """Clone GitHub Repo"""
    repo_url = entry_url_clone.get()
    if repo_url:
        run_git_command(f"git clone {repo_url}")
    else:
        messagebox.showerror("❌ 錯誤", "請輸入 GitHub Repo 連結！")

def git_pull():
    """Pull 最新版本"""
    run_git_command("git pull origin main")

# 設定 Tkinter 介面
root = tk.Tk()
root.title("GitHub 小機器人")
root.geometry("620x500")  # 增加視窗大小
root.configure(bg="#F8F8F8")  # 設定背景色

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

checkbox_var = tk.BooleanVar()
checkbox_readme = tk.Checkbutton(frame_push, text="✅ 這個 Repo 有 README.md", variable=checkbox_var, bg="white", font=("Arial", 12))
checkbox_readme.pack()

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