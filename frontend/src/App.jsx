import { useState } from 'react'
import './App.css'

function App() {
  const [listing, setListing] = useState('')
  const [chat, setChat] = useState('')

  const handleAnalyze = () => {
    console.log('판매글:', listing)
    console.log('채팅:', chat)
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
          disabled={!listing.trim() && !chat.trim()}
        >
          분석하기
        </button>
      </main>
    </div>
  )
}

export default App