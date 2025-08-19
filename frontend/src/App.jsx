import { useState } from 'react'
import BirthChartForm from './components/BirthChartForm'
import QuestionInterface from './components/QuestionInterface'

function App() {
  const [activeTab, setActiveTab] = useState('chart')
  const [birthChartData, setBirthChartData] = useState(null)

  return (
    <div className="app">
      <div className="container">
        {/* Header */}
        <div className="header">
          <h1>✨ Astro AI</h1>
          <p>Your Personal Astrological Assistant</p>
        </div>

        {/* Navigation Tabs */}
        <div className="flex justify-center">
          <div className="tab-nav">
            <button
              onClick={() => setActiveTab('chart')}
              className={`tab-button ${activeTab === 'chart' ? 'active' : ''}`}
            >
              🌟 Birth Chart
            </button>
            <button
              onClick={() => setActiveTab('questions')}
              className={`tab-button ${activeTab === 'questions' ? 'active' : ''}`}
            >
              💬 Ask Questions
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="main-content">
          {activeTab === 'chart' ? (
            <BirthChartForm onDataReceived={setBirthChartData} />
          ) : (
            <QuestionInterface chartContext={birthChartData} />
          )}
        </div>
      </div>
    </div>
  )
}

export default App