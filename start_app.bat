@echo off
rem プロジェクトディレクトリに移動（実際のプロジェクトパスに合わせて変更）
cd /d "J:\my_creation_project"

rem Python のフルパスを指定して streamlit を起動
"C:\Users\masak\AppData\Local\Programs\Python\Python310\python.exe" -m streamlit run ui_app.py

rem 終了後にウィンドウがすぐに閉じないようにする
pause
