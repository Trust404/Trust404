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

            <div className="result-card">
              <strong>거래 위험도</strong>
              <p>위험 점수: {result.risk_score} / 100</p>
              <p>위험 등급: {result.risk_level}</p>
            </div>

            <h3>위험 신호</h3>

            {result.patterns.length === 0 ? (
              <p>탐지된 위험 신호가 없습니다.</p>
            ) : (
              result.patterns.map((pattern, index) => (
                <div className="result-card" key={index}>
                  <strong>{pattern.label}</strong>
                  <p>근거: {pattern.evidence}</p>
                  <p>
                    신뢰도: {Math.round(pattern.confidence * 100)}%
                  </p>
                </div>
              ))
            )}

            <h3>판매글 · 채팅 불일치</h3>

            {result.inconsistencies.length === 0 ? (
              <p>탐지된 불일치가 없습니다.</p>
            ) : (
              result.inconsistencies.map((item, index) => (
                <div className="result-card" key={index}>
                  <strong>{item.type}</strong>
                  <p>판매글 근거: {item.listing_evidence}</p>
                  <p>채팅 근거: {item.chat_evidence}</p>
                  <p>심각도: {item.severity}</p>
                  <p>이유: {item.reason}</p>
                </div>
              ))
            )}

            <h3>거래 단계</h3>
            <p>{result.trade_stage}</p>

            <h3>분석 요약</h3>
            <p>{result.summary}</p>
<h3>대응 가이드</h3>

<div className="result-card">
  <p>{result.guidance.goal}</p>

  {result.guidance.requires_official_source && (
    <p>
      공식 기관의 신고·피해 대응 절차 확인이 필요한 단계입니다.
    </p>
  )}
</div>
            <h3>확인 체크포인트</h3>

            {result.checkpoints.length === 0 ? (
              <p>추가 확인 사항이 없습니다.</p>
            ) : (
              <div className="result-card">
                <ul>
                  {result.checkpoints.map((checkpoint, index) => (
                    <li key={index}>{checkpoint}</li>
                  ))}
                </ul>
              </div>
            )}
          </section>
        )}
      </main>
    </div>
  )
}

export default App