import requests
import datetime
import urllib3
import json
import pytz  # pip install pytz (필수: 시간대 처리용)

# 보안 경고 숨기기
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==========================================
# 1. 태국 정부 공식 데이터 가져오기 (Session 적용)
# ==========================================
def get_lotto_data():
    api_url = "https://www.glo.or.th/api/lottery/getLatestLottery"
    
    # 세션을 사용하여 연결 안정성 확보
    session = requests.Session()
    
    try:
        # 1. 메인 페이지 접속 흉내 (쿠키 획득)
        headers_main = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.glo.or.th/'
        }
        session.get("https://www.glo.or.th/", headers=headers_main, verify=False, timeout=10)

        # 2. 실제 데이터 요청
        headers_api = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.glo.or.th/',
            'Origin': 'https://www.glo.or.th',
            'Content-Type': 'application/json'
        }
        
        response = session.post(api_url, headers=headers_api, verify=False, timeout=10)
        
        if response.status_code != 200:
            print(f"Server returned status: {response.status_code}")
            return None
            
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

# ==========================================
# 2. [수정됨] 오늘의 행운 정보 (태국 시간 기준)
# ==========================================
def get_daily_lucky_info():
    # 📌 핵심 수정: 서버 시간이 아닌 '태국 시간' 기준으로 요일 계산
    tz_bkk = pytz.timezone('Asia/Bangkok')
    now_bkk = datetime.datetime.now(tz_bkk)
    weekday = now_bkk.weekday()  # 0:월요일 ~ 6:일요일
    
    daily_data = [
        {"day": "วันจันทร์ (Monday)", "color_name": "เหลือง (Yellow)", "color_code": "#FFD700", "car_num": "2, 5"},
        {"day": "วันอังคาร (Tuesday)", "color_name": "ชมพู (Pink)", "color_code": "#FF69B4", "car_num": "3, 0"},
        {"day": "วันพุธ (Wednesday)", "color_name": "เขียว (Green)", "color_code": "#4CAF50", "car_num": "4, 8"},
        {"day": "วันพฤหัสบดี (Thursday)", "color_name": "ส้ม (Orange)", "color_code": "#FF9800", "car_num": "1, 5"},
        {"day": "วันศุกร์ (Friday)", "color_name": "ฟ้า (Blue)", "color_code": "#00BFFF", "car_num": "6, 9"},
        {"day": "วันเสาร์ (Saturday)", "color_name": "ม่วง (Purple)", "color_code": "#9C27B0", "car_num": "7, 3"},
        {"day": "วันอาทิตย์ (Sunday)", "color_name": "แดง (Red)", "color_code": "#F44336", "car_num": "1, 8"},
    ]
    
    today_info = daily_data[weekday]
    
    return f'''
    <section class="lucky-daily-section">
        <div class="lucky-header">
            <span class="emoji">🍀</span>
            <h3>ดวงประจำวัน: {today_info['day']}</h3>
        </div>
        <div class="lucky-content">
            <div class="lucky-item">
                <span class="lucky-label">สีมงคล</span>
                <div class="lucky-value">
                    <span class="color-circle" style="background-color: {today_info['color_code']};"></span>
                    {today_info['color_name']}
                </div>
            </div>
            <div class="lucky-item">
                <span class="lucky-label">เลขทะเบียนรถ</span>
                <div class="lucky-value">
                    🚗 ลงท้าย {today_info['car_num']}
                </div>
            </div>
        </div>
    </section>
    '''

# ==========================================
# 3. 통계 HTML (변경 없음, 그대로 사용)
# ==========================================
def create_stats_html():
    # ... (기존 코드와 동일)
    stats_data = {
        'hot_numbers': [(79, 9), (85, 8), (98, 8)],
        'cold_numbers': [(3, 1), (17, 2)],
        'top_5': [(79, 9), (85, 8), (98, 8), (42, 7), (56, 6)]
    }

    hot_balls = ""
    for num, freq in stats_data['hot_numbers']:
        hot_balls += f'''
        <div class="stat-ball-wrapper">
            <div class="stat-ball hot">{num:02d}</div>
            <span class="frequency-label">{freq} ครั้ง</span>
        </div>
        '''
    
    cold_balls = ""
    for num, freq in stats_data['cold_numbers']:
        cold_balls += f'''
        <div class="stat-ball-wrapper">
            <div class="stat-ball cold">{num:02d}</div>
            <span class="frequency-label">{freq} ครั้ง</span>
        </div>
        '''
    
    max_freq = stats_data['hot_numbers'][0][1]
    chart_bars = ""
    for i, (num, freq) in enumerate(stats_data['top_5']):
        width = (freq / max_freq) * 100
        bar_class = 'hot' if i < 2 else ('warm' if i < 4 else 'neutral')
        chart_bars += f'''
        <div class="chart-bar-row">
            <span class="chart-label">{num:02d}</span>
            <div class="chart-bar-bg">
                <div class="chart-bar-fill {bar_class}" style="width: {width}%;"></div>
            </div>
            <span class="chart-value">{freq} ครั้ง</span>
        </div>
        '''
    
    return f'''
    <section class="stats-section">
        <div class="stats-header">
            <span class="emoji">📊</span>
            <h3>สถิติหวยย้อนหลัง 10 ปี</h3>
        </div>
        <div class="hot-cold-container">
            <div class="hot-section">
                <div class="section-label">🔥 HOT เลขออกบ่อย</div>
                <div class="stats-balls">{hot_balls}</div>
            </div>
            <div class="cold-section">
                <div class="section-label">❄️ COLD เลขออกน้อย</div>
                <div class="stats-balls">{cold_balls}</div>
            </div>
        </div>
        <div class="mini-chart">
            <div class="chart-title">TOP 5 เลขท้าย 2 ตัว</div>
            <div class="chart-bar-container">{chart_bars}</div>
        </div>
        <div class="stats-footer">* ข้อมูล พ.ศ. 2557-2567</div>
    </section>
    '''

# ==========================================
# 4. 전체 HTML 조립 (OG 태그 추가 및 광고 최적화)
# ==========================================
def create_html(data):
    if not data:
        return "<h1>Data Error / กำลังปรับปรุงระบบ</h1>"

    # 태국 시간 기준 업데이트 시간 표시
    tz_bkk = pytz.timezone('Asia/Bangkok')
    now = datetime.datetime.now(tz_bkk).strftime("%d/%m/%Y %H:%M")
    
    first_balls_html = "".join([f'<div class="ball ball-1st" role="listitem">{char}</div>' for char in data['first']])
    last2_balls_html = "".join([f'<div class="ball ball-2nd" role="listitem">{char}</div>' for char in data['last2']])
    
    last3_balls_html = ""
    for num_str in (data['last3f'] + data['last3b']):
        last3_balls_html += '<div style="display:flex; gap:4px; margin:5px;">'
        for char in num_str:
            last3_balls_html += f'<div class="ball ball-3rd" role="listitem">{char}</div>'
        last3_balls_html += '</div>'

    stats_section_html = create_stats_html()
    daily_lucky_html = get_daily_lucky_info()
    
    # 📌 [NEW] 사이트 URL (본인 도메인으로 수정하세요)
    my_site_url = "https://lottery.spattra.com"

    html = f"""
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ตรวจหวย {data['date']} - ผลสลากกินแบ่งรัฐบาลล่าสุด</title>
    <meta name="description" content="ตรวจผลสลากกินแบ่งรัฐบาล งวดวันที่ {data['date']} รางวัลที่ 1 คือ {data['first']} เลขท้าย 2 ตัว คือ {data['last2']} ตรวจหวยย้อนหลังฟรี">
    
    <!-- 📌 [NEW] Open Graph (SNS 공유 시 썸네일/제목 설정) -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="📢 ผลหวยงวด {data['date']} ออกแล้ว!">
    <meta property="og:description" content="รางวัลที่ 1: {data['first']} | เลขท้าย 2 ตัว: {data['last2']}">
    <meta property="og:image" content="{my_site_url}/og-image.png">
    <meta property="og:url" content="{my_site_url}">
    
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🎱</text></svg>">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    
    <!-- Google AdSense -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3198582468837090" crossorigin="anonymous"></script>

    <style>
        :root {{
            --bg-primary: #0a1628;
            --bg-secondary: #0d1f3c;
            --bg-gradient: linear-gradient(180deg, #0a1628 0%, #152238 50%, #0d1f3c 100%);
            --glass-bg: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
            --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            --gold-primary: #d4af37;
            --gold-gradient: linear-gradient(135deg, #f4e5b2 0%, #d4af37 50%, #aa8c2c 100%);
            --ball-1st: linear-gradient(145deg, #f4e5b2 0%, #d4af37 30%, #aa8c2c 70%, #8b7225 100%);
            --ball-2nd: linear-gradient(145deg, #34d399 0%, #10b981 50%, #059669 100%);
            --ball-3rd: linear-gradient(145deg, #fbbf24 0%, #f59e0b 50%, #d97706 100%);
            --text-primary: #ffffff;
            --text-secondary: rgba(255, 255, 255, 0.7);
            --text-muted: rgba(255, 255, 255, 0.5);
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Sarabun', sans-serif; background: var(--bg-gradient); min-height: 100vh; color: var(--text-primary); overflow-x: hidden; }}
        
        .layout-wrapper {{ display: flex; justify-content: center; align-items: flex-start; gap: 20px; padding: 20px; max-width: 1200px; margin: 0 auto; }}
        .side-rail {{ width: 160px; height: 600px; position: sticky; top: 20px; display: none; }}
        
        /* 📌 [NEW] 모바일 최적화 (너비 제한 완화) */
        .main-content {{ flex: 1; max-width: 500px; width: 100%; }}
        
        @media (min-width: 1024px) {{ .side-rail {{ display: block; }} }}
        @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600;700&display=swap');
        
        .glass-card {{ background: var(--glass-bg); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid var(--glass-border); border-radius: 24px; padding: 24px; box-shadow: var(--glass-shadow); margin-bottom: 20px; }}
        
        .header h1 {{ font-size: 1.6em; font-weight: 700; background: var(--gold-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 8px; text-align: center; }}
        .header .date {{ display: block; text-align: center; color: var(--text-secondary); margin-bottom: 20px; }}
        .header .emoji {{ display: block; text-align: center; font-size: 1.5em; margin-bottom: 5px; }}
        
        .result-section {{ text-align: center; margin-bottom: 24px; }}
        .result-label {{ display: inline-block; font-size: 0.9em; font-weight: 600; color: var(--text-secondary); margin-bottom: 12px; padding: 4px 16px; background: rgba(255,255,255,0.05); border-radius: 20px; }}
        
        .balls-container {{ display: flex; justify-content: center; flex-wrap: wrap; gap: 8px; }}
        .ball {{ width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 1.1em; color: #1a1a1a; box-shadow: 0 4px 15px rgba(0,0,0,0.3), inset 0 2px 4px rgba(255,255,255,0.4); }}
        .ball-1st {{ background: var(--ball-1st); width: 48px; height: 48px; }}
        .ball-2nd {{ background: var(--ball-2nd); color: white; }}
        .ball-3rd {{ background: var(--ball-3rd); }}

        /* 럭키 섹션 스타일 */
        .lucky-daily-section {{ background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 20px; margin: 20px 0; }}
        .lucky-header {{ display: flex; align-items: center; gap: 8px; margin-bottom: 15px; border-bottom: 1px solid rgba(255, 255, 255, 0.1); padding-bottom: 10px; }}
        .lucky-content {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }}
        .lucky-item {{ background: rgba(0, 0, 0, 0.2); padding: 12px; border-radius: 12px; text-align: center; }}
        .lucky-label {{ font-size: 0.8em; color: var(--text-muted); display: block; margin-bottom: 5px; }}
        .lucky-value {{ font-size: 0.95em; font-weight: bold; color: #f4e5b2; display: flex; align-items: center; justify-content: center; gap: 6px; }}
        .color-circle {{ width: 14px; height: 14px; border-radius: 50%; display: inline-block; border: 1px solid rgba(255,255,255,0.3); }}

        /* 통계 섹션 스타일 */
        .stats-section {{ background: var(--glass-bg); backdrop-filter: blur(20px); border: 1px solid var(--glass-border); border-radius: 24px; padding: 24px; margin-top: 16px; }}
        .stats-header {{ display: flex; align-items: center; gap: 8px; margin-bottom: 20px; border-bottom: 1px solid rgba(212,175,55,0.2); padding-bottom: 10px; }}
        .hot-cold-container {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px; }}
        .hot-section {{ background: rgba(255, 87, 51, 0.1); border: 1px solid rgba(255, 87, 51, 0.3); padding: 10px; border-radius: 12px; text-align:center; }}
        .cold-section {{ background: rgba(0, 188, 212, 0.1); border: 1px solid rgba(0, 188, 212, 0.3); padding: 10px; border-radius: 12px; text-align:center; }}
        .stats-balls {{ display: flex; justify-content: center; gap: 4px; flex-wrap: wrap; }}
        .stat-ball {{ width: 30px; height: 30px; font-size: 0.8em; display:flex; align-items:center; justify-content:center; border-radius:50%; }}
        .stat-ball.hot {{ background: linear-gradient(145deg, #ffab40, #e65100); color: black; }}
        .stat-ball.cold {{ background: linear-gradient(145deg, #4dd0e1, #00838f); color: white; }}
        
        .mini-chart {{ margin-top: 20px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.1); }}
        .chart-bar-row {{ display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }}
        .chart-label {{ width: 20px; font-size: 0.8em; text-align: right; }}
        .chart-bar-bg {{ flex: 1; height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; }}
        .chart-bar-fill {{ height: 100%; border-radius: 3px; }}
        .chart-bar-fill.hot {{ background: #ff6d00; }}
        .chart-bar-fill.warm {{ background: #ffc107; }}
        .chart-bar-fill.neutral {{ background: #8bc34a; }}
        
        /* SNS 공유 버튼 */
        .share-section-home {{ text-align: center; margin: 30px 0 20px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.1); }}
        .share-title {{ color: rgba(255,255,255,0.6); font-size: 0.85rem; margin-bottom: 12px; }}
        .share-buttons {{ display: flex; gap: 12px; justify-content: center; }}
        .share-btn {{ width: 45px; height: 45px; border-radius: 50%; display: flex; align-items: center; justify-content: center; text-decoration: none; color: white; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.15); transition: all 0.3s ease; font-size: 1.2rem; cursor: pointer; }}
        .share-btn:hover {{ transform: scale(1.1); }}
        .share-facebook {{ background: #1877F2; }}
        .share-line {{ background: #06C755; }}
        .share-twitter {{ background: #000000; }}
        
        .copy-toast {{ position: fixed; bottom: 80px; left: 50%; transform: translateX(-50%) translateY(20px); background: rgba(16,185,129,0.9); color: white; padding: 10px 20px; border-radius: 20px; opacity: 0; visibility: hidden; transition: all 0.3s; z-index: 1000; }}
        .copy-toast.show {{ opacity: 1; visibility: visible; transform: translateX(-50%) translateY(0); }}

        /* 궁합 버튼 */
        .btn-zodiac {{ display: block; background: linear-gradient(135deg, #6c5ce7, #a29bfe); color: white; text-decoration: none; padding: 15px; border-radius: 15px; font-weight: bold; text-align: center; margin: 20px 0; box-shadow: 0 4px 15px rgba(108, 92, 231, 0.3); transition: transform 0.2s; }}
        .btn-zodiac:hover {{ transform: translateY(-3px); }}

        .footer {{ text-align: center; padding: 20px; font-size: 0.75em; color: var(--text-muted); }}
        .ad-container {{ background: rgba(255,255,255,0.02); border-radius: 12px; overflow: hidden; margin: 20px 0; text-align: center; }}
        .ad-label {{ font-size: 0.6em; color: #555; text-align: right; padding-right: 5px; }}
    </style>
</head>
<body>

<div class="layout-wrapper">
    <aside class="side-rail">
        <div class="ad-label">AD</div>
        <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3198582468837090" data-ad-slot="5807274060" data-ad-format="auto" data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
    </aside>

    <div class="main-content">
        <main class="glass-card">
            <header class="header">
                <span class="emoji">🎉</span>
                <h1>ผลสลากกินแบ่งรัฐบาล</h1>
                <p class="date">งวดประจำวันที่ {data['date']}</p>
            </header>

            <section class="result-section">
                <span class="result-label">🏆 รางวัลที่ 1</span>
                <div class="balls-container">{first_balls_html}</div>
            </section>

            <section class="result-section">
                <span class="result-label">เลขท้าย 2 ตัว</span>
                <div class="balls-container">{last2_balls_html}</div>
            </section>

            <section class="result-section">
                <span class="result-label">เลขท้าย 3 ตัว</span>
                <div class="balls-container">{last3_balls_html}</div>
            </section>
        </main>

        {daily_lucky_html}

        <div class="ad-container">
             <div class="ad-label">AD</div>
             <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3198582468837090" data-ad-slot="5807274060" data-ad-format="auto" data-full-width-responsive="true"></ins>
            <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
        </div>

        {stats_section_html}

        <a href="https://zodiac.spattra.com" target="_blank" class="btn-zodiac">
            💘 เช็คดวงความรัก <br>
            <span style="font-size:0.9em; opacity:0.9;">12 นักษัตร ชาย-หญิง / LGBTQ+</span>
        </a>

        <div class="share-section-home">
            <p class="share-title">แชร์ให้เพื่อน</p>
            <div class="share-buttons">
                <a href="https://www.facebook.com/sharer/sharer.php?u=" onclick="this.href+=encodeURIComponent(window.location.href);return true;" target="_blank" class="share-btn share-facebook"><i class="fab fa-facebook-f"></i></a>
                <a href="https://social-plugins.line.me/lineit/share?url=" onclick="this.href+=encodeURIComponent(window.location.href);return true;" target="_blank" class="share-btn share-line"><i class="fab fa-line"></i></a>
                <a href="https://twitter.com/intent/tweet?url=" onclick="this.href+=encodeURIComponent(window.location.href)+'&text='+encodeURIComponent(document.title);return true;" target="_blank" class="share-btn share-twitter"><i class="fab fa-x-twitter"></i></a>
                <button onclick="copyLink()" class="share-btn share-copy" title="Copy Link"><i class="fas fa-link"></i></button>
            </div>
            <div id="copy-toast" class="copy-toast">✅ คัดลอกแล้ว!</div>
        </div>

        <footer class="footer">
            <p>อัปเดต: {now} (เวลาไทย)</p>
            <p>© 2025 Lottery Result Thailand</p>
        </footer>
    </div>

    <aside class="side-rail">
        <div class="ad-label">AD</div>
        <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3198582468837090" data-ad-slot="5807274060" data-ad-format="auto" data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
    </aside>

</div>

<script>
    function copyLink() {{
        navigator.clipboard.writeText(window.location.href).then(() => {{
            const t = document.getElementById('copy-toast');
            t.classList.add('show');
            setTimeout(() => t.classList.remove('show'), 2000);
        }}).catch(err => {{
            alert('URL Copy Failed');
        }});
    }}
</script>

</body>
</html>
    """
    return html

# --- 메인 실행 ---
if __name__ == "__main__":
    print("Collecting data...")
    try:
        data = get_lotto_data()
        
        if data:
            print(f"Success! Date: {data['date']}")
            html = create_html(data)
            with open("index.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("index.html created successfully.")
        else:
            print("Failed to collect data.")
    except Exception as e:
        print(f"Fatal Error: {e}")
