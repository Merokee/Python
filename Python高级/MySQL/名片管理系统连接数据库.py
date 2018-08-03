"""名片管理系统"""
import card_system_tools


while True:
    # 1.功能选择界面
    card_system_tools.welcome()
    # 2.输入接收
    ctrl_num = input("请输入你想使用的功能：")

    # 3.功能实现

    # 新建名片
    if ctrl_num == "1":
        print("你选择的功能是：")
        print("1.新建名片")
        card_system_tools.new_card()
        print("名片创建成功！")

    # 显示全部
    elif ctrl_num == "2":
        card_system_tools.show_all()

    # 查询名片
    elif ctrl_num == "3":
        card_system_tools.check_card()
    # 退出系统
    elif ctrl_num == "0":
        print("欢迎下次使用名片管理系统！")
        break
    else:
        print("你输入的格式有误，请重新输入！")