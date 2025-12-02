try:
    # 尝试导入web_app模块
    from web_app import *
    print("导入成功")
except Exception as e:
    import traceback
    print(f"导入错误: {str(e)}")
    print("\n详细错误信息:")
    traceback.print_exc()