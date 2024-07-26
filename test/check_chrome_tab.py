from pywinauto import Desktop
import time
import re

pattern = r"^.*?-(.*?)-(.*?)-(.*?)-"

# Kết nối đến cửa sổ Chrome
desktop = Desktop(backend="uia")
chrome_window = desktop.window(
    title_re=".* Google Chrome$", control_type="Pane")

# Tìm tất cả các tab trong cửa sổ Chrome
tabs = chrome_window.descendants(control_type="TabItem")

# Xác định tab YouTube và đóng nó
for tab in tabs:
    # print(tab.window_text)
    match = re.match(pattern, str(tab.window_text))
    if match:
        if "youtube" in match.group(3).lower() or "youtube" in match.group(2).lower() or ('youtube' in match.group(1).lower() and "usage" in match.group(2).lower()):
            print(True)
    # try:
    #     match = re.match(pattern, str(tab.window_text))
    #     if match:
    #         if "youtube" in match.group(2).lower() or ('youtube' in match.group(1).lower() and "usage" in match.group(2).lower()):
    #             chrome_window.set_focus()
    #             tab.click_input(double=True)  # Đảm bảo tab được chọn
    #             time.sleep(1)  # Đợi để đảm bảo tab đã được chọn
    #             tab.type_keys("^w")  # Đóng tab
    #             break  # Thoát khỏi vòng lặp sau khi đóng tab YouTube
    # except Exception as e:
    #     # Tiếp tục vòng lặp
    #     print(f"Lỗi: {e}")
    #     continue
