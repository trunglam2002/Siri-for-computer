import vlc
from pytube import YouTube
from youtube_search import YoutubeSearch
import re
from datetime import timedelta
import threading
import keyboard


def get_views(view_count):
    """Process the view count string and return an integer."""
    return int(re.sub(r'\D', '', view_count))


def handle_event(event):
    """Handle VLC player events."""
    if event.type == vlc.EventType.MediaPlayerEndReached:
        print("Playback finished.")
    elif event.type == vlc.EventType.MediaPlayerEncounteredError:
        print("An error occurred during playback.")


def wait_for_enter_to_stop(player, instance):
    """Wait for Enter key to stop playback and release resources."""
    keyboard.wait('enter')
    player.stop()
    instance.release()


def main():
    # Input search keyword
    search_keyword = input("Nhập từ khóa cần tìm trên YouTube: ")

    # Search for videos on YouTube
    results = YoutubeSearch(search_keyword, max_results=10).to_dict()

    # Process search results
    if results:
        try:
            # Sort results by view count in descending order
            sorted_results = sorted(
                results, key=lambda x: get_views(x['views']), reverse=True)

            # Get the URL of the most viewed video
            top_video = sorted_results[0]
            video_url = f"https://www.youtube.com{top_video['url_suffix']}"

            # Fetch video details using pytube
            yt_video = YouTube(video_url)
            print("Thông tin video:")
            print("Tên video:", yt_video.title)
            print("Thời lượng:", str(timedelta(seconds=yt_video.length)))

            # Get the URL of the best audio stream
            audio_stream = yt_video.streams.filter(only_audio=True).first().url

            # Initialize VLC
            instance = vlc.Instance()
            player = instance.media_player_new()
            media = instance.media_new(audio_stream)
            player.set_media(media)

            # Start playback
            player.play()

            # Attach event handler
            event_manager = player.event_manager()
            event_manager.event_attach(
                vlc.EventType.MediaPlayerEndReached, handle_event)
            event_manager.event_attach(
                vlc.EventType.MediaPlayerEncounteredError, handle_event)

            # Wait for Enter key to stop playback
            thread = threading.Thread(
                target=wait_for_enter_to_stop, args=(player, instance))
            thread.start()

        except Exception as e:
            print(f"An error occurred: {e}")
            print("Không tìm thấy kết quả nào cho từ khóa đã nhập.")
    else:
        print("Không tìm thấy kết quả nào cho từ khóa đã nhập.")


if __name__ == "__main__":
    main()
