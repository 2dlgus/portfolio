import os
import requests
import yfinance as yf

# 수집 대상 종목 리스트 (섹터별 상위 3개씩 예시)
tickers = [
    "TSLA", "AAPL", "NVDA",       # 기술주
    "JPM", "BAC", "GS",           # 금융
    "PG", "KO", "PEP",            # 소비재
    "XOM", "CVX", "COP",          # 에너지
    "UNH", "JNJ", "PFE",          # 헬스케어
]

# 저장 디렉토리
save_dir = "static/assets/img/logos"
os.makedirs(save_dir, exist_ok=True)

def get_domain_from_yf(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        website = info.get("website", "")
        if website:
            domain = website.replace("http://", "").replace("https://", "").split('/')[0]
            return domain
    except Exception as e:
        print(f"[{ticker}] 야후 정보 조회 실패: {e}")
    return None

def download_logo(ticker, domain):
    logo_url = f"https://logo.clearbit.com/{domain}"
    try:
        r = requests.get(logo_url, timeout=10)
        if r.status_code == 200:
            filepath = os.path.join(save_dir, f"{ticker}.png")
            with open(filepath, "wb") as f:
                f.write(r.content)
            print(f"[{ticker}] 로고 저장 완료")
        else:
            print(f"[{ticker}] 로고 다운로드 실패 (status {r.status_code})")
    except Exception as e:
        print(f"[{ticker}] 요청 실패: {e}")

for ticker in tickers:
    domain = get_domain_from_yf(ticker)
    if domain:
        download_logo(ticker, domain)
    else:
        print(f"[{ticker}] 도메인 없음, 건너뜀")
