import requests
from bs4 import BeautifulSoup
import datetime

# 태국 Sanook 복권 페이지 URL
url = "https://news.sanook.com/lotto/"

def get_latest_lotto():
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 최신 회차 날짜 가져오기
        date_text = soup.find('h2', class_='lotto-check__title').text.strip()
        
        # 1등 당첨 번호 (6자리)
        first_prize = soup.find('strong', class_='lotto-check__number').text.strip()
        
        # 마지막 2자리 숫자 (가장 인기 많음)
        last_two = soup.find_all('strong', class_='lotto-check__number')[3].text.strip()
        
        # 마지막 3자리 숫자들 (여러 개)
        last_three_tags = soup.find_all('strong', class_='lotto-check__number')
        last_three = [tag.text.strip() for tag in last_three_tags[1:3]] # 보통 2개

        return {
            "date": date_text,
            "first_prize": first_prize,
            "last_two": last_two,
            "last_three": last_three
        }

    except Exception as e:
        print(f"에러 발생: {e}")
        return None

# 실행 및 테스트
if __name__ == "__main__":
    data = get_latest_lotto()
    if data:
        print("🎉 최신 태국 복권 정보 수집 성공!")
        print(f"날짜: {data['date']}")
        print(f"1등 번호: {data['first_prize']}")
        print(f"2자리 행운 숫자: {data['last_two']}")
        print(f"3자리 숫자들: {data['last_three']}")
    else:
        print("데이터를 가져오지 못했습니다.")
