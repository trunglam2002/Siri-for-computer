from pywinauto import Desktop
import time
import re

pattern = r"^(.*?)-"
pattern_after = r"^.*?-(.*?)-"

# Kết nối đến cửa sổ Chrome
desktop = Desktop(backend="uia")
chrome_window = desktop.window(
    title_re=".* Google Chrome$", control_type="Pane")

# Tìm tất cả các tab trong cửa sổ Chrome
tabs = chrome_window.descendants(control_type="TabItem")

# Xác định tab YouTube và đóng nó
for tab in tabs:
    match = re.match(pattern, tab.window_text())
    after_match = re.match(pattern_after, tab.window_text())
    if "youtube" in match.group(1).lower() and "usage" in after_match.group(1).lower():
        chrome_window.set_focus()
        tab.click_input(double=True)  # Đảm bảo tab được chọn
        time.sleep(1)  # Đợi để đảm bảo tab đã được chọn
        tab.type_keys("^w")  # Đóng tab
        break  # Thoát khỏi vòng lặp sau khi đóng tab YouTube
