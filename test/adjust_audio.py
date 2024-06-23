from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import comtypes


def set_system_volume(volume):
    # Lấy danh sách tất cả các sessions âm thanh đang chạy
    sessions = AudioUtilities.GetAllSessions()

    # Duyệt qua từng session và điều chỉnh âm lượng
    for session in sessions:
        volume_object = session._ctl.QueryInterface(ISimpleAudioVolume)
        volume_object.SetMasterVolume(volume, None)

    return f"System volume set to {int(volume * 100)}%"


# Sử dụng hàm để thiết lập âm lượng hệ thống (volume trong khoảng từ 0.0 đến 1.0)
volume_level = 0.5  # Ví dụ: âm lượng 50%
print(set_system_volume(volume_level))
