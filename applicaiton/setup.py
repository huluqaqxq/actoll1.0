from cx_Freeze import setup, Executable
#指定的模块
include_modules = ['tool', 'db.json']
#打包配置
setup(name="ACTool", version="0.1", description="数据库对比工具",
      options={"build_exe": {"include_files": include_modules}},
      executables=[Executable("actapplication.py", base="Win32GUI")])