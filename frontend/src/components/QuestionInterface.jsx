import { useState } from 'react'

const QuestionInterface = ({ chartContext }) => {
  const [question, setQuestion] = useState('')
  const [conversation, setConversation] = useState([])
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!question.trim()) return

    const userQuestion = question.trim()
    setQuestion('')
    setLoading(true)

    // Add user question to conversation
    const newConversation = [...conversation, { type: 'user', content: userQuestion }]
    setConversation(newConversation)

    try {
      const response = await fetch('http://localhost:8000/ask-question', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: userQuestion,
          context: chartContext
        })
      })

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`)
      }

      const data = await response.json()
      
      // Add AI response to conversation
      setConversation(prev => [...prev, { 
        type: 'ai', 
        content: data.answer,
        status: data.status 
      }])

    } catch (err) {
      setConversation(prev => [...prev, { 
        type: 'ai', 
        content: `Sorry, I encountered an error: ${err.message}`,
        status: 'error'
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setConversation([])
  }

  const hasChartContext = chartContext && chartContext.chart

  return (
    <div className="card">
      <div className="flex space-between items-center" style={{marginBottom: '1.5rem'}}>
        <h2 style={{margin: 0}}>💬 Ask Your Astrology Questions</h2>
        {conversation.length > 0 && (
          <button
            onClick={handleClear}
            className="btn btn-secondary"
            style={{fontSize: '0.75rem', padding: '0.5rem 1rem'}}
          >
            Clear Chat
          </button>
        )}
      </div>

      {hasChartContext && (
        <div className="alert alert-success">
          ✨ I have your birth chart context for {chartContext.name}. 
          Ask me specific questions about your chart!
        </div>
      )}

      {!hasChartContext && (
        <div className="alert alert-info">
          💡 Generate your birth chart first to get personalized answers, or ask general astrology questions.
        </div>
      )}

      {/* Chat History */}
      <div className="chat-container">
        {conversation.length === 0 && (
          <div className="text-center" style={{color: '#718096', padding: '2rem 0'}}>
            <p>Start a conversation by asking any astrology question!</p>
            <div style={{marginTop: '1rem', fontSize: '0.875rem'}}>
              <p>Example questions:</p>
              <ul style={{listStyle: 'disc', listStylePosition: 'inside', marginTop: '0.5rem'}}>
                <li>"What does my sun sign mean?"</li>
                <li>"How do moon phases affect me?"</li>
                <li>"What are the characteristics of my rising sign?"</li>
                {hasChartContext && <li>"Tell me about my planetary positions"</li>}
              </ul>
            </div>
          </div>
        )}
        
        {conversation.map((message, index) => (
          <div key={index} className={`chat-message ${message.type}`}>
            <div className={`chat-bubble ${message.type} ${message.status === 'error' ? 'error' : ''}`}>
              <div className="flex" style={{alignItems: 'flex-start'}}>
                <span style={{marginRight: '0.5rem'}}>
                  {message.type === 'user' ? '🙋‍♀️' : '🔮'}
                </span>
                <div style={{flex: 1}}>
                  <p style={{whiteSpace: 'pre-wrap', margin: 0}}>{message.content}</p>
                </div>
              </div>
            </div>
          </div>
        ))}

        {loading && (
          <div className="chat-message">
            <div className="chat-bubble ai">
              <div className="flex items-center">
                <span style={{marginRight: '0.5rem'}}>🔮</span>
                <div className="flex items-center gap-2">
                  <div className="loading-spinner"></div>
                  <span>Consulting the stars...</span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Question Input */}
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask me anything about astrology..."
          className="form-input"
          style={{flex: 1}}
          disabled={loading}
        />
        <button
          type="submit"
          disabled={loading || !question.trim()}
          className="btn btn-primary"
        >
          Send
        </button>
      </form>
    </div>
  )
}

export default QuestionInterface