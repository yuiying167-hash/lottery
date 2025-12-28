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

# 2. HTML 생성 (디자인 적용)
def create_html(data):
    if not data:
        return "<h1>Data Error / กำลังปรับปรุงระบบ</h1>"

    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # --- 숫자 공(Ball) 만들기 로직 ---
    
    # 1. 1등 번호 (한 글자씩 쪼개기)
    first_balls_html = ""
    for char in data['first']:
        first_balls_html += f'<div class="ball ball-1st" role="listitem">{char}</div>'

    # 2. 2자리 번호 (한 글자씩 쪼개기)
    last2_balls_html = ""
    for char in data['last2']:
        last2_balls_html += f'<div class="ball ball-2nd" role="listitem">{char}</div>'

    # 3. 3자리 번호들 (4개 세트)
    last3_balls_html = ""
    # 3자리 앞번호 + 뒷번호 합치기
    all_3digits = data['last3f'] + data['last3b']
    
    for num_str in all_3digits:
        # 각 숫자 세트마다 감싸는 컨테이너 추가 (가독성 위해)
        last3_balls_html += '<div style="display:flex; gap:4px; margin:5px;">'
        for char in num_str:
            last3_balls_html += f'<div class="ball ball-3rd" role="listitem">{char}</div>'
        last3_balls_html += '</div>'

    # --- HTML 조립 (CSS 포함) ---
    # f-string에서 CSS의 중괄호 {}는 {{ }}로 두 번 써야 함
    html = f"""
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ตรวจหวย - ผลสลากกินแบ่งรัฐบาล</title>
    <meta name="description" content="ตรวจหวยย้อนหลัง ผลสลากกินแบ่งรัฐบาล งวดล่าสุด {data['date']}">
    
    <!-- Google AdSense 자동 광고 스크립트 -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3198582468837090"
         crossorigin="anonymous"></script>

    <style>
        /* ===================================
           1. CSS 변수 (색상 팔레트)
        =================================== */
        :root {{
            --bg-primary: #0a1628;
            --bg-secondary: #0d1f3c;
            --bg-gradient: linear-gradient(180deg, #0a1628 0%, #152238 50%, #0d1f3c 100%);
            
            --glass-bg: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
            --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            
            --gold-primary: #d4af37;
            --gold-light: #f4e5b2;
            --gold-gradient: linear-gradient(135deg, #f4e5b2 0%, #d4af37 50%, #aa8c2c 100%);
            
            --ball-1st: linear-gradient(145deg, #f4e5b2 0%, #d4af37 30%, #aa8c2c 70%, #8b7225 100%);
            --ball-2nd: linear-gradient(145deg, #34d399 0%, #10b981 50%, #059669 100%);
            --ball-3rd: linear-gradient(145deg, #fbbf24 0%, #f59e0b 50%, #d97706 100%);
            
            --text-primary: #ffffff;
            --text-secondary: rgba(255, 255, 255, 0.7);
            --text-muted: rgba(255, 255, 255, 0.5);
            
            --ad-bg: rgba(255, 255, 255, 0.03);
            --ad-border: rgba(212, 175, 55, 0.3);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600;700&display=swap');

        body {{
            font-family: 'Sarabun', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-gradient);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            padding: 20px;
            color: var(--text-primary);
        }}

        .container {{
            width: 100%;
            max-width: 420px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}

        .glass-card {{
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 24px;
            box-shadow: var(--glass-shadow);
        }}

        .header {{
            text-align: center;
            padding-bottom: 20px;
            border-bottom: 1px solid rgba(212, 175, 55, 0.2);
            margin-bottom: 24px;
        }}

        .header h1 {{
            font-size: 1.6em;
            font-weight: 700;
            background: var(--gold-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
        }}

        .header .date {{
            font-size: 0.95em;
            color: var(--text-secondary);
        }}

        .header .emoji {{
            font-size: 1.4em;
            margin-bottom: 8px;
            display: block;
        }}

        .result-section {{
            text-align: center;
            margin-bottom: 24px;
        }}

        .result-section:last-of-type {{
            margin-bottom: 0;
        }}

        .result-label {{
            display: inline-block;
            font-size: 0.9em;
            font-weight: 600;
            color: var(--text-secondary);
            margin-bottom: 12px;
            padding: 4px 16px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
        }}

        .balls-container {{
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .ball {{
            width: 48px;
            height: 48px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1.2em;
            color: #1a1a1a;
            text-shadow: 0 1px 2px rgba(255, 255, 255, 0.3);
            box-shadow: 
                0 4px 15px rgba(0, 0, 0, 0.3),
                inset 0 2px 4px rgba(255, 255, 255, 0.4),
                inset 0 -2px 4px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .ball:hover {{
            transform: translateY(-3px) scale(1.05);
            box-shadow: 
                0 8px 25px rgba(0, 0, 0, 0.4),
                inset 0 2px 4px rgba(255, 255, 255, 0.4),
                inset 0 -2px 4px rgba(0, 0, 0, 0.2);
        }}

        .ball-1st {{
            background: var(--ball-1st);
            width: 52px;
            height: 52px;
            font-size: 1.3em;
        }}

        .ball-2nd {{
            background: var(--ball-2nd);
            color: #ffffff;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
        }}

        .ball-3rd {{
            background: var(--ball-3rd);
        }}

        .ad-section {{
            background: var(--ad-bg);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid var(--ad-border);
            border-radius: 16px;
            padding: 16px;
            position: relative;
        }}

        .ad-label {{
            position: absolute;
            top: 8px;
            right: 12px;
            font-size: 0.7em;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .ad-container {{
            min-height: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 12px;
            border: 1px dashed rgba(255, 255, 255, 0.1);
        }}
        
        .ad-container ins {{
            display: block;
            width: 100%;
        }}

        .footer {{
            text-align: center;
            padding: 16px;
            font-size: 0.75em;
            color: var(--text-muted);
        }}

        .footer a {{
            color: var(--gold-primary);
            text-decoration: none;
        }}

        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .glass-card {{ animation: fadeInUp 0.6s ease-out; }}
        .result-section {{ animation: fadeInUp 0.6s ease-out backwards; }}
        .result-section:nth-child(2) {{ animation-delay: 0.1s; }}
        .result-section:nth-child(3) {{ animation-delay: 0.2s; }}
        .result-section:nth-child(4) {{ animation-delay: 0.3s; }}
        
        .ball {{ animation: fadeInUp 0.5s ease-out backwards; }}
        .balls-container .ball:nth-child(1) {{ animation-delay: 0.1s; }}
        .balls-container .ball:nth-child(2) {{ animation-delay: 0.15s; }}
        .balls-container .ball:nth-child(3) {{ animation-delay: 0.2s; }}
        
        @media (max-width: 380px) {{
            .ball {{ width: 42px; height: 42px; font-size: 1em; }}
            .ball-1st {{ width: 46px; height: 46px; }}
            .header h1 {{ font-size: 1.4em; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 메인 결과 카드 -->
        <main class="glass-card" role="main" aria-label="ผลสลากกินแบ่งรัฐบาล">
            
            <header class="header">
                <span class="emoji">🎉</span>
                <h1>ผลสลากกินแบ่งรัฐบาล</h1>
                <p class="date">งวดประจำวันที่ {data['date']}</p>
            </header>

            <!-- 1등 -->
            <section class="result-section" aria-labelledby="prize-1st">
                <span id="prize-1st" class="result-label">🏆 รางวัลที่ 1 (1등)</span>
                <div class="balls-container" role="list">
                    {first_balls_html}
                </div>
            </section>

            <!-- 2자리 -->
            <section class="result-section" aria-labelledby="prize-2digit">
                <span id="prize-2digit" class="result-label">เลขท้าย 2 ตัว (2자리)</span>
                <div class="balls-container" role="list">
                    {last2_balls_html}
                </div>
            </section>

            <!-- 3자리 -->
            <section class="result-section" aria-labelledby="prize-3digit">
                <span id="prize-3digit" class="result-label">เลขท้าย 3 ตัว (3자리)</span>
                <div class="balls-container" role="list">
                    {last3_balls_html}
                </div>
            </section>

        </main>

        <!-- ✅ 광고 영역 (결과 하단 배치) -->
        <aside class="ad-section" aria-label="โฆษณา">
            <span class="ad-label">Sponsored</span>
            <div class="ad-container">
                <!-- Google AdSense 디스플레이 광고 -->
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
        </aside>

        <!-- 푸터 -->
        <footer class="footer">
            <p>อัปเดตอัตโนมัติ: <time datetime="{now}">{now}</time></p>
            <p>Powered by <a href="#">LotteryBot</a></p>
        </footer>

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
