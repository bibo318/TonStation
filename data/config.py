# api id, hash
API_ID = xxxx
API_HASH = 'xxxxx'

DELAYS = {
    "RELOGIN": [5, 7],  # trì hoãn sau lần thử đăng nhập
    'ACCOUNT': [5, 15],  #độ trễ giữa các kết nối với tài khoản (càng nhiều tài khoản thì độ trễ càng lâu)
    'CLAIM': [10, 20],   # sự chậm trễ giữa các lần rót bia
    'TASK': [2, 5],  # trì hoãn sau khi hoàn thành nhiệm vụ
    'REPEAT': [2, 5]  # trì hoãn sau khi hoàn thành
}

PROXY = {
    "USE_PROXY_FROM_FILE": False,  # True - nếu sử dụng proxy từ tệp, Sai -nếu sử dụng proxy từ accounts.json
    "PROXY_PATH": "data/proxy.txt",  # đường dẫn đến tập tin proxy
    "TYPE": {
        "TG": "http",  # loại proxy cho máy khách tg. "socks4", "socks5" và "http" được hỗ trợ
        "REQUESTS": "http"  # loại proxy cho các yêu cầu. "http" cho proxy https và http, "sock5" cho proxy vớ5.
        }
}

# thư mục phiên (không thay đổi)
WORKDIR = "sessions/"

# thời gian chờ tính bằng giây để kiểm tra tài khoản hợp lệ
TIMEOUT = 30

SOFT_INFO = f"""{"TON Station".center(40)}
Game https://t.me/tonstationgames_bot
{"Functional:".center(40)}
Đăng ký tài khoản trong ứng dụng web; start Và claim farming; 

Phần mềm cũng thu thập số liệu thống kê về tài khoản và sử dụng proxy từ {f"file {PROXY['PROXY_PATH']}" if PROXY['USE_PROXY_FROM_FILE'] else "file accounts.json "}
Để mua phần mềm này với tùy chọn đặt liên kết giới thiệu của bạn, hãy viết thư cho tôi: https://t.me/debugs0
"""