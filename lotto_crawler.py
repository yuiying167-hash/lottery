import requests
import json

# 태국 정부 복권 공식 API 주소 (숨겨진 주소)
api_url = "https://www.glo.or.th/api/lottery/getLatestLottery"

def get_latest_lotto():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.glo.or.th/', # 정부 사이트에서 온 척하기
            'Origin': 'https://www.glo.or.th'
        }
        
        # 데이터를 요청합니다 (POST 방식)
        response = requests.post(api_url, headers=headers, verify=False) # verify=False는 SSL 에러 방지용
        
        if response.status_code == 200:
            data = response.json() # JSON 데이터로 변환
            
            # 데이터 구조 파싱
            date_thai = data['response']['date'] # 날짜
            
            # 당첨 번호들 추출 (data 리스트 안에 있음)
            # 1등: data[0]
            first_prize = data['response']['data']['first']['number'][0]['value']
            
            # 2자리 번호 (보통 last2)
            last_two = data['response']['data']['last2']['number'][0]['value']
            
            # 3자리 번호들 (last3f, last3b)
            last_three_front = [item['value'] for item in data['response']['data']['last3f']['number']]
            last_three_back = [item['value'] for item in data['response']['data']['last3b']['number']]
            
            return {
                "date": date_thai,
                "first_prize": first_prize,
                "last_two": last_two,
                "last_threes": last_three_front + last_three_back
            }
        else:
            print(f"API 호출 실패: 상태 코드 {response.status_code}")
            return None

    except Exception as e:
        print(f"에러 상세: {e}")
        return None

if __name__ == "__main__":
    # 보안 경고 메시지 숨기기 (깔끔하게 보려고)
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    data = get_latest_lotto()
    if data:
        print(f"📅 날짜: {data['date']}")
        print(f"🥇 1등: {data['first_prize']}")
        print(f"✌️ 2자리: {data['last_two']}")
        print(f"🔢 3자리: {data['last_threes']}")
    else:
        print("수집 실패")
