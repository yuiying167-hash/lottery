import requests
from bs4 import BeautifulSoup

# 타겟 변경: Mthai (구조가 단순함)
url = "https://lotto.mthai.com/"

def get_latest_lotto():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 1. 날짜 가져오기
        # Mthai는 h4 태그 안에 날짜가 있음
        date_element = soup.find('h4')
        date_text = date_element.text.strip() if date_element else "날짜 못찾음"

        # 2. 1등 번호 (li.lot-first span)
        first_prize_tag = soup.select_one('li.lot-first span')
        first_prize = first_prize_tag.text.strip() if first_prize_tag else "못찾음"

        # 3. 2자리 번호 (li.lot-last2 span)
        last_two_tag = soup.select_one('li.lot-last2 span')
        last_two = last_two_tag.text.strip() if last_two_tag else "못찾음"
        
        # 4. 3자리 번호들 (li.lot-last3 span) - 보통 2개 또는 4개
        last_three_tags = soup.select('li.lot-last3 span')
        last_threes = [tag.text.strip() for tag in last_three_tags]

        return {
            "date": date_text,
            "first_prize": first_prize,
            "last_two": last_two,
            "last_threes": last_threes
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
        print(f"🔢 3자리: {data['last_threes']}")
    else:
        print("수집 실패")
