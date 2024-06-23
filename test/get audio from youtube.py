import vlc
from pytube import YouTube
from youtube_search import YoutubeSearch
import re
from datetime import timedelta
import threading
import keyboard

# Nhập từ khóa từ người dùng
search_keyword = input("Nhập từ khóa cần tìm trên YouTube: ")

# Tìm kiếm video trên YouTube và sắp xếp theo số lượt xem cao nhất
results = YoutubeSearch(search_keyword, max_results=10).to_dict()

# Chọn video có số lượt xem cao nhất từ kết quả tìm kiếm
if results:
    try:
        def get_views(view_count):
            # Attempt to process the view count as a string
            return int(re.sub(r'\D', '', view_count))

        # Sắp xếp kết quả theo số lượt xem (lớn đến nhỏ)
        sorted_results = sorted(
            results, key=lambda x: get_views(x['views']), reverse=True)

        # Lấy URL của video có số lượt xem cao nhất
        top_video = sorted_results[0]
        video_url = f"https://www.youtube.com{top_video['url_suffix']}"

        # Sử dụng pytube để lấy thông tin chi tiết về video
        yt_video = YouTube(video_url)
        print("Thông tin video:")
        print("Tên video:", yt_video.title)
        print("Thời lượng:", str(timedelta(seconds=yt_video.length)))

        # Lấy URL của luồng âm thanh tốt nhất (chỉ âm thanh)
        audio_stream = yt_video.streams.filter(only_audio=True).first().url

        # Tạo instance của VLC
        instance = vlc.Instance()

        # Tạo media player
        player = instance.media_player_new()

        # Tạo media từ URL của âm thanh
        media = instance.media_new(audio_stream)

        # Đưa media vào player
        player.set_media(media)

        # Bắt đầu phát âm thanh
        player.play()

        # Lắng nghe sự kiện phát kết thúc hoặc gặp lỗi
        event_manager = player.event_manager()

        # Hàm xử lý sự kiện phát kết thúc hoặc lỗi
        def handle_event(event):
            if event.type == vlc.EventType.MediaPlayerEndReached:
                print("Phát kết thúc")
            elif event.type == vlc.EventType.MediaPlayerEncounteredError:
                print("Lỗi khi phát")

        # Đăng ký hàm xử lý sự kiện với event manager
        event_manager.event_attach(
            vlc.EventType.MediaPlayerEndReached, handle_event)
        event_manager.event_attach(
            vlc.EventType.MediaPlayerEncounteredError, handle_event)

        # Hàm chờ sự kiện nhấn Enter để dừng phát và thoát chương trình
        def wait_for_enter_to_stop():
            keyboard.wait('enter')
            player.stop()
            instance.release()

        # Bỏ vòng lặp chờ sự kiện phát kết thúc hoặc lỗi ra ngoài
        thread = threading.Thread(target=wait_for_enter_to_stop)
        thread.start()

    except (TypeError, ValueError) as e:
        print(f"An error occurred: {e}")
        print("Không tìm thấy kết quả nào cho từ khóa đã nhập.")
else:
    print("Không tìm thấy kết quả nào cho từ khóa đã nhập.")
