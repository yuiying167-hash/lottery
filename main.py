import requests
import datetime
import urllib3
import json

# 보안 경고 숨기기
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 1. 태국 정부 공식 데이터 가져오기
def get_lotto_data():
    api_url = "https://www.glo.or.th/api/lottery/getLatestLottery"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://www.glo.or.th/',
            'Origin': 'https://www.glo.or.th'
        }
        # SSL 인증서 무시하고 요청 (verify=False)
        response = requests.post(api_url, headers=headers, verify=False)
        data = response.json()
        
        result = {
            "date": data['response']['date'],
            "first": data['response']['data']['first']['number'][0]['value'],
            "last2": data['response']['data']['last2']['number'][0]['value'],
            "last3f": [item['value'] for item in data['response']['data']['last3f']['number']],
            "last3b": [item['value'] for item in data['response']['data']['last3b']['number']]
        }
        return result
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# 2. HTML 생성 (광고 포함)
def create_html(data):
    if not data:
        return "<h1>Data Error / กำลังปรับปรุงระบบ</h1>"

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 3자리 번호들을 HTML 공 모양으로 변환
    last3_balls = ""
    for num in (data['last3f'] + data['last3b']):
        last3_balls += f'<div class="ball ball-3">{num}</div>'

    html = f"""
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ตรวจหวย - ผลสลากกินแบ่งรัฐบาล</title>
        <meta name="description" content="ตรวจหวยย้อนหลัง ผลสลากกินแบ่งรัฐบาล งวดล่าสุด {data['date']}">
        
        <!-- [광고 1] 구글 자동 광고 스크립트 -->
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3198582468837090"
             crossorigin="anonymous"></script>

        <style>
            @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap');
            body {{ font-family: 'Sarabun', sans-serif; background-color: #f4f6f8; text-align: center; margin: 0; padding: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }}
            
            h1 {{ color: #1a237e; margin: 0 0 10px 0; font-size: 1.8em; }}
            .date {{ color: #555; font-size: 1.1em; margin-bottom: 20px; font-weight: bold; }}
            
            .ad-container {{ margin: 20px 0; min-height: 100px; background: #fafafa; border: 1px dashed #ddd; }}
            
            .section {{ margin-bottom: 30px; }}
            .label {{ display: block; font-size: 1.1em; color: #333; margin-bottom: 10px; font-weight: bold; }}
            
            /* 공 디자인 */
            .ball {{ display: inline-block; width: 60px; height: 60px; line-height: 60px; border-radius: 50%; 
                     color: white; font-weight: bold; font-size: 1.3em; margin: 5px; box-shadow: 2px 2px 5px rgba(0,0,0,0.15); }}
            
            .ball-1st {{ background: linear-gradient(45deg, #ff512f, #dd2476); width: 140px; border-radius: 30px; }}
            .ball-2 {{ background: linear-gradient(45deg, #11998e, #38ef7d); }}
            .ball-3 {{ background: linear-gradient(45deg, #f09819, #edde5d); color: #333; text-shadow: none; }}

            .footer {{ margin-top: 40px; font-size: 0.8em; color: #aaa; border-top: 1px solid #eee; padding-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎉 ผลสลากกินแบ่งรัฐบาล</h1>
            <div class="date">งวดประจำวันที่ {data['date']}</div>

            <!-- [광고 2] 로또 결과 바로 위 상단 광고 -->
            <div class="ad-container">
                <ins class="adsbygoogle"
                     style="display:block"
                     data-ad-client="ca-pub-3198582468837090"
                     data-ad-slot="5807274060"
                     data-ad-format="auto"
                     data-full-width-responsive="true"></ins>
                <script>
                     (adsbygoogle = window.adsbygoogle || []).push({{}});
                </script>
            </div>
            <!-- 광고 끝 -->

            <div class="section">
                <span class="label">รางวัลที่ 1 (1등)</span>
                <div class="ball ball-1st">{data['first']}</div>
            </div>

            <div class="section">
                <span class="label">เลขท้าย 2 ตัว (2자리)</span>
                <div class="ball ball-2">{data['last2']}</div>
            </div>

            <div class="section">
                <span class="label">เลขท้าย 3 ตัว (3자리)</span>
                <div>{last3_balls}</div>
            </div>
            
            <div class="footer">
                อัปเดตอัตโนมัติ: {now}<br>
                Powered by LotteryBot
            </div>
        </div>
    </body>
    </html>
    """
    return html

# --- 메인 실행 ---
if __name__ == "__main__":
    print("Collecting data...")
    data = get_lotto_data()
    
    if data:
        print(f"Success! Date: {data['date']}")
        html = create_html(data)
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("index.html created successfully.")
    else:
        print("Failed to collect data.")
