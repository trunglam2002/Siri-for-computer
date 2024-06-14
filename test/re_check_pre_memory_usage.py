import re

text = "<bound method BaseWrapper.window_text of <uiawrapper.UIAWrapper - '[SD]_Labeling_Guide_1.0v_240402 [VIET].pdf - Google Drive', TabItem, 1998727900832712318>>"

pattern = r"^.*?\s-\s.*?-(.*?)-"
match = re.match(pattern, text)

if match:
    google_drive = match.group(1)
    print(google_drive)  # In this case, it will print "Google Drive"
