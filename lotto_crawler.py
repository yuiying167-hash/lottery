import requests
from bs4 import BeautifulSoup

# 태국 Sanook 복권 페이지 URL
url = "https://news.sanook.com/lotto/"

def get_latest_lotto():
    try:
        # ⭐️ 중요: 로봇이 아닌 척하기 위한 헤더 추가
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers) # 헤더를 같이 보냄
        response.encoding = 'utf-8' # 한글/태국어 깨짐 방지
        
        soup = BeautifulSoup(response.content, 'html.parser')

        # --- (디버깅용) 사이트가 제대로 열렸는지 확인 ---
        # print(soup.title.text) 

        # 1. 날짜 가져오기 (구조가 자주 바뀌니 예외처리 강화)
        title_tag = soup.find('h2', class_='lotto-check__title')
        if title_tag:
            date_text = title_tag.text.strip()
        else:
            date_text = "날짜 정보 없음"

        # 2. 1등 번호 가져오기
        first_prize_tag = soup.find('strong', class_='lotto-check__number')
        if first_prize_tag:
            first_prize = first_prize_tag.text.strip()
        else:
            first_prize = "???"

        # 3. 데이터 반환
        return {
            "date": date_text,
            "first_prize": first_prize
        }

    except Exception as e:
        print(f"에러 발생: {e}")
        return None

# 실행 및 테스트
if __name__ == "__main__":
    data = get_latest_lotto()
    if data:
        print("🎉 크롤링 성공!")
        print(f"날짜: {data['date']}")
        print(f"1등 번호: {data['first_prize']}")
    else:
        print("실패 ㅠㅠ")
