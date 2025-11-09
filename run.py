import streamlit.web.cli  as stcli
import sys
import os

if __name__ == "__main__":
    # PyInstaller onefile 模式下的解压临时目录
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    
    # 切换工作目录到真正的程序根目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 这里的 streamlit app 是什么名字，需要修改下，我的这里叫main.py
    app_path = os.path.join(base_path, "index.py")
    # 确保工作目录正确
    if not os.path.exists(app_path):
        print("找不到 index.py:", app_path)
        sys.exit(1)
    
    sys.argv = [
        "streamlit",
        "run",
        app_path, 
        "--global.developmentMode=false",
    ]
    sys.exit(stcli.main())

