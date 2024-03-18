import datetime as dt
import FinanceDataReader as fdr
import plotly.graph_objs as go
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import warnings

# 경고를 무시하도록 설정
warnings.filterwarnings("ignore", message="A date index has been provided, but it has no associated frequency information")
warnings.filterwarnings("ignore", message="No supported index is available.")

# 이랜시스 종목의 데이터 불러오기
이랜시스 = fdr.DataReader(symbol='264850', start='2023-06-01')

# 이동평균선 5일선 계산하기
이랜시스['MA5'] = 이랜시스['Close'].rolling(window=5).mean()

# ARIMA 모델 학습
model = ARIMA(이랜시스['MA5'], order=(5,1,0))  # ARIMA(p,d,q) 모델 설정
model_fit = model.fit()

# 다음 주의 5일 이동평균 예측
forecast = model_fit.forecast(steps=5).values # 다음 5일치 예측 값을 리스트로 변환
print(forecast)
# 마지막날 거래 종가
last = 이랜시스['Close'].iloc[-1]
print("막날 종가 : ", last)

# Candlestick 그래프 생성
candlestick_data = {
    'x': 이랜시스.index,
    'open': 이랜시스['Open'],
    'high': 이랜시스['High'],
    'low': 이랜시스['Low'],
    'close': 이랜시스['Close'],
    'type': 'candlestick',
    'name': 'Candlesticks'
}
candlestick = go.Candlestick(**candlestick_data)

# 다음 주 예측을 표시하는 Candlestick 그래프 생성
next_week_index = pd.date_range(start='2024-03-18', periods=5)  # 다음 주 날짜 범위 생성
next_week_data = {
    'open': forecast,
    'high': forecast,
    'low': forecast,
    'close': forecast
}
next_week_candlestick = go.Candlestick(x=next_week_index, **next_week_data, name='다음 주 예측')

# 그래프 레이아웃 설정
layout = go.Layout(title='이랜시스 주식 데이터 예측',
                   xaxis=dict(title='날짜'),
                   yaxis=dict(title='가격'))

# 그래프 플롯
fig = go.Figure(data=[candlestick, next_week_candlestick], layout=layout)
fig.show()
