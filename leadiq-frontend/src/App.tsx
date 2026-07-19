import { useState, useEffect } from "react"

const App = () => {
  const [url, setUrl] = useState("")
  const [question, setQuestion] = useState("")
  const [sessionId, setSessionId] = useState(sessionStorage.getItem("sessionId") || "")
  const [messages, setMessages] = useState(JSON.parse(sessionStorage.getItem("messages") || "[]"))
  const [isLoaded, setIsLoaded] = useState(!!sessionStorage.getItem("sessionId"))
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    sessionStorage.setItem("sessionId", sessionId)
    sessionStorage.setItem("messages", JSON.stringify(messages))
  }, [sessionId, messages])

  const handleLoad = async () => {
    setIsLoading(true)
    const response = await fetch("http://localhost:8000/load", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({url: url})
    })
    const data = await response.json()
    setSessionId(data.session_id)
    setIsLoaded(true)
    setIsLoading(false)
  }

  const handleAsk = async () => {
    setIsLoading(true)
    const response = await fetch("http://localhost:8000/ask", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        session_id: sessionId,
        question: question,
        history: messages
      })
    })
    const data = await response.json()
    setMessages([...messages, {question: question, answer: data.answer}])
    setQuestion("")
    setIsLoading(false)
  }

  const handleReset = () => {
    sessionStorage.clear()
    setSessionId("")
    setMessages([])
    setIsLoaded(false)
    setUrl("")
    setQuestion("")
  }

  return (
    <div>
      <h1>LeadIQ</h1>
      <p>Enter a company URL to get started</p>

      {!isLoaded && (
        <div>
          <input
            type="text"
            placeholder="https://company.com"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
          <button onClick={handleLoad}>
            {isLoading ? "Loading..." : "Load Company"}
          </button>
        </div>
      )}

      {isLoaded && (
        <div>
          <p>Company loaded! Ask your questions.</p>
          <button onClick={handleReset}>Reset Chat</button>
          <div>
            {messages.map((msg, index) => (
              <div key={index}>
                <p><strong>You:</strong> {msg.question}</p>
                <p><strong>LeadIQ:</strong> {msg.answer}</p>
              </div>
            ))}
          </div>
          <input
            type="text"
            placeholder="Ask a question..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
          <button onClick={handleAsk}>
            {isLoading ? "Thinking..." : "Ask"}
          </button>
        </div>
      )}
    </div>
  )
}

export default App