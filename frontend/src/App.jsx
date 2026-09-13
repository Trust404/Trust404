import { useState } from 'react'
import './App.css'

function App() {
  const [listing, setListing] = useState('')
  const [chat, setChat] = useState('')

  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleAnalyze = async () => {
    setLoading(true)
    setError('')
    setResult(null)

    try {
      const response = await fetch('/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          listing,
          chat,
        }),
      })

      if (!response.ok) {
        throw new Error('분석 요청에 실패했습니다.')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <header className="header">
        <h1>Trust404</h1>
        <p>AI 기반 중고거래 사기 위험 분석</p>
      </header>

      <main className="form">
        <div className="input-group">
          <label htmlFor="listing">판매글</label>
          <textarea
            id="listing"
            value={listing}
            onChange={(e) => setListing(e.target.value)}
            placeholder="판매글 내용을 입력하세요."
          />
        </div>

        <div className="input-group">
          <label htmlFor="chat">판매자와의 채팅</label>
          <textarea
            id="chat"
            value={chat}
            onChange={(e) => setChat(e.target.value)}
            placeholder="판매자와 나눈 채팅 내용을 입력하세요."
          />
        </div>

        <button
          className="analyze-button"
          onClick={handleAnalyze}
          disabled={(!listing.trim() && !chat.trim()) || loading}
        >
          {loading ? '분석 중...' : '분석하기'}
        </button>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {result && (
          <section className="result-section">
            <h2>분석 결과</h2>

            <h3>위험 신호</h3>

            {result.patterns.length === 0 ? (
              <p>탐지된 위험 신호가 없습니다.</p>
            ) : (
              result.patterns.map((pattern, index) => (
                <div className="result-card" key={index}>
                  <strong>{pattern.label}</strong>
                  <p>근거: {pattern.evidence}</p>
                  <p>신뢰도: {Math.round(pattern.confidence * 100)}%</p>
                </div>
              ))
            )}

            <h3>요약</h3>
            <p>{result.summary}</p>

            <h3>판매글 · 채팅 불일치</h3>

            {result.inconsistencies.length === 0 ? (
              <p>탐지된 불일치가 없습니다.</p>
            ) : (
              result.inconsistencies.map((item, index) => (
                <div className="result-card" key={index}>
                  <strong>{item.type}</strong>
                  <p>{item.reason}</p>
                  <p>심각도: {item.severity}</p>
                </div>
              ))
            )}

            <h3>거래 단계</h3>
            <p>{result.trade_stage}</p>
          </section>
        )}
      </main>
    </div>
  )
}

export default App