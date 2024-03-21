import FinanceDataReader as fdr
import plotly.graph_objs as go
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import warnings

# 경고를 무시하도록 설정
warnings.filterwarnings("ignore", message="A date index has been provided, but it has no associated frequency information")
warnings.filterwarnings("ignore", message="No supported index is available.")

# 이랜시스 종목의 데이터 불러오기
이랜시스 = fdr.DataReader(symbol='264850', start='2023-01-01')

# 이동평균선 5일선 계산하기
이랜시스['MA5'] = 이랜시스['Close'].rolling(window=5).mean()
이랜시스['MA20'] = 이랜시스['Close'].rolling(window=20).mean()
이랜시스['MA60'] = 이랜시스['Close'].rolling(window=60).mean()
이랜시스['MA90'] = 이랜시스['Close'].rolling(window=90).mean()

# ARIMA 모델 학습
models = {}
forecasts = {}
for ma_col in ['MA5', 'MA20', 'MA60', 'MA90']:
    model = ARIMA(이랜시스[ma_col], order=(5,1,0))
    model_fit = model.fit()
    models[ma_col] = model_fit
    forecasts[ma_col] = model_fit.forecast(steps=30).values

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
next_week_index = pd.date_range(start='2024-03-19', periods=30)  # 다음 주 날짜 범위 생성
next_week_candlestick_data = {}
for ma_col, forecast in forecasts.items():
    next_week_candlestick_data[ma_col] = {
        'open': forecast,
        'high': forecast,
        'low': forecast,
        'close': forecast,
        'name': f'{ma_col} 다음 주 예측'
    }
next_week_candlesticks = [go.Candlestick(x=next_week_index, **data) for data in next_week_candlestick_data.values()]

# 그래프 레이아웃 설정
layout = go.Layout(title='이랜시스 주식 데이터 예측',
                   xaxis=dict(title='날짜'),
                   yaxis=dict(title='가격'))

# 그래프 플롯
fig = go.Figure(data=[candlestick, *next_week_candlesticks], layout=layout)
fig.show()


# 오차율 계산 함수 정의
def calculate_error_rate(predicted_values, actual_values):
    error_rates = []
    for predicted, actual in zip(predicted_values, actual_values):
        error = abs(predicted - actual) / actual
        error_rate = error * 100
        error_rates.append(error_rate)
    return error_rates

predicted_values = next_week_candlestick_data['MA5']['close']  # MA5 다음 주 예측값 리스트
actual_values = [7770]
# 오차율 계산
error_rates = calculate_error_rate(predicted_values, actual_values)

# 결과 출력
for i, error_rate in enumerate(error_rates, start=1):
    print(f"Day {i}의 오차율: {error_rate:.2f}%")