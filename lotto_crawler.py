import requests
from bs4 import BeautifulSoup

url = "https://news.sanook.com/lotto/"

def get_latest_lotto():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 1. 날짜 찾기 (h3 태그 안에 있음)
        # 보통 "ตรวจหวย 16 ธันวาคม 2568" 이런 식으로 되어 있음
        date_element = soup.select_one('h3.lotto-check__title') 
        if not date_element:
             # 만약 h3가 없으면 h2로 시도 (구조 변경 대비)
            date_element = soup.select_one('h2.lotto-check__title')
            
        date_text = date_element.text.strip() if date_element else "날짜 못찾음"

        # 2. 1등 번호 찾기 (strong 태그 중 첫 번째 것)
        # Sanook은 당첨 번호를 <strong class="lotto-check__number">...</strong> 안에 넣음
        numbers = soup.select('strong.lotto-check__number')
        
        if len(numbers) > 0:
            first_prize = numbers[0].text.strip() # 1등
            last_two = numbers[3].text.strip()    # 2자리 번호 (보통 4번째에 있음)
        else:
            first_prize = "번호 못찾음"
            last_two = "???"

        return {
            "date": date_text,
            "first_prize": first_prize,
            "last_two": last_two
        }

    except Exception as e:
        print(f"에러 상세: {e}")
        return None

if __name__ == "__main__":
    data = get_latest_lotto()
    if data:
        print(f"📅 날짜: {data['date']}")
        print(f"🥇 1등: {data['first_prize']}")
        print(f"✌️ 2자리: {data['last_two']}")
    else:
        print("데이터 수집 실패")
