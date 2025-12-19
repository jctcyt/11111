@echo off
echo 正在启动企业数字化转型指数查询系统...
echo.
echo 请确保以下文件存在于当前目录：
echo - 合并后的文件.xlsx (数据文件)
echo - digital_transformation_app.py (应用文件)
echo.
echo 如果是第一次运行，请先安装依赖：
echo pip install -r requirements.txt
echo.
echo 正在启动Streamlit应用...
streamlit run digital_transformation_app.py
pause