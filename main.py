import requests
import datetime
import urllib3

# 보안 경고 숨기기
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 1. 데이터 가져오기 (성공했던 그 코드!)
def get_lotto_data():
    api_url = "https://www.glo.or.th/api/lottery/getLatestLottery"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://www.glo.or.th/',
            'Origin': 'https://www.glo.or.th'
        }
        response = requests.post(api_url, headers=headers, verify=False)
        data = response.json()
        
        # 필요한 정보 추출
        result = {
            "date": data['response']['date'],
            "first": data['response']['data']['first']['number'][0]['value'],
            "last2": data['response']['data']['last2']['number'][0]['value'],
            "last3f": [item['value'] for item in data['response']['data']['last3f']['number']],
            "last3b": [item['value'] for item in data['response']['data']['last3b']['number']]
        }
        return result
    except Exception as e:
        print(f"Error: {e}")
        return None

# 2. HTML 만들기
def create_html(data):
    # 데이터가 없을 때(에러 났을 때) 보여줄 문구
    if not data:
        return "<h1>Error fetching data</h1>"

    # 3자리 번호들을 쉼표(,)로 합치기
    last3_str = ", ".join(data['last3f'] + data['last3b'])
    
    # 오늘 날짜 (업데이트 시간용)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    html = f"""
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ตรวจหวย - ผลสลากกินแบ่งรัฐบาล</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap');
            body {{ font-family: 'Sarabun', sans-serif; background-color: #f0f8ff; text-align: center; padding: 20px; margin: 0; }}
            .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
            h1 {{ color: #1a237e; margin-bottom: 5px; }}
            .date {{ color: #666; font-size: 1.1em; margin-bottom: 30px; }}
            
            /* 복권 공 디자인 */
            .ball {{ display: inline-block; width: 60px; height: 60px; line-height: 60px; border-radius: 50%; color: white; font-weight: bold; font-size: 1.2em; margin: 5px; box-shadow: 2px 2px 5px rgba(0,0,0,0.2); }}
            .ball-1st {{ background: linear-gradient(135deg, #ff416c, #ff4b2b); width: 120px; border-radius: 60px; }} /* 1등은 길게 */
            .ball-2 {{ background: linear-gradient(135deg, #11998e, #38ef7d); }}
            .ball-3 {{ background: linear-gradient(135deg, #f7971e, #ffd200); color: #333; }}

            .section {{ margin: 30px 0; }}
            .label {{ font-size: 1.2em; font-weight: bold; margin-bottom: 10px; display: block; }}
            
            .update-time {{ margin-top: 40px; font-size: 0.8em; color: #999; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎉 ผลสลากกินแบ่งรัฐบาล</h1>
            <div class="date">{data['date']}</div>

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
                <div>
                    <!-- 3자리 번호들을 공으로 만들기 -->
                    {''.join([f'<div class="ball ball-3">{num}</div>' for num in (data['last3f'] + data['last3b'])])}
                </div>
            </div>
            
            <div class="update-time">
                อัปเดตล่าสุด: {now} (By AI Bot)
            </div>
        </div>
    </body>
    </html>
    """
    return html

# --- 실행 ---
print("데이터 수집 시작...")
lotto_data = get_lotto_data()

if lotto_data:
    print(f"수집 성공! 날짜: {lotto_data['date']}")
    html_content = create_html(lotto_data)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("index.html 업데이트 완료!")
else:
    print("데이터 수집 실패로 업데이트 취소")
