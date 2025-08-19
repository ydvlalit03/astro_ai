import { useState } from 'react'

const BirthChartForm = ({ onDataReceived }) => {
  const [formData, setFormData] = useState({
    name: 'Lalit Rao',
    dob: '2001-01-10',
    time: '05:30',
    place: 'Delhi, India'
  })
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const response = await fetch('http://localhost:8000/birth-chart', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      })

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`)
      }

      const data = await response.json()
      setResult(data)
      onDataReceived(data)
    } catch (err) {
      setError(err.message)
      console.error('Error fetching birth chart:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  return (
    <div className="card">
      <h2>🌟 Generate Your Birth Chart</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="grid grid-2">
          <div className="form-group">
            <label htmlFor="name" className="form-label">
              Full Name
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              required
              className="form-input"
              placeholder="Enter your full name"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="place" className="form-label">
              Birth Place
            </label>
            <input
              type="text"
              id="place"
              name="place"
              value={formData.place}
              onChange={handleInputChange}
              required
              className="form-input"
              placeholder="City, Country"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="dob" className="form-label">
              Date of Birth
            </label>
            <input
              type="date"
              id="dob"
              name="dob"
              value={formData.dob}
              onChange={handleInputChange}
              required
              className="form-input"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="time" className="form-label">
              Time of Birth
            </label>
            <input
              type="time"
              id="time"
              name="time"
              value={formData.time}
              onChange={handleInputChange}
              required
              className="form-input"
            />
          </div>
        </div>
        
        <button
          type="submit"
          disabled={loading}
          className="btn btn-primary btn-large"
          style={{width: '100%'}}
        >
          {loading ? (
            <div className="flex items-center gap-2">
              <div className="loading-spinner"></div>
              Generating Chart...
            </div>
          ) : (
            'Generate Birth Chart'
          )}
        </button>
      </form>

      {error && (
        <div className="alert alert-error">
          ❌ {error}
        </div>
      )}

      {result && (
        <div style={{marginTop: '2rem'}}>
          <div className="result-card chart">
            <h3>🌀 Natal Chart</h3>
            <div className="code-display">
              {JSON.stringify(result.chart, null, 2)}
            </div>
          </div>

          {result.horoscope && (
            <div className="result-card horoscope">
              <h3>🌟 Daily Horoscope</h3>
              <p>{result.horoscope}</p>
            </div>
          )}

          {result.interpretation && (
            <div className="result-card interpretation">
              <h3>📖 AI Interpretation</h3>
              <p style={{whiteSpace: 'pre-wrap'}}>{result.interpretation}</p>
            </div>
          )}

          <div style={{fontSize: '0.875rem', color: '#718096', borderTop: '1px solid #e2e8f0', paddingTop: '1rem', marginTop: '1rem'}}>
            <p>Time Zone: {result.timezone} • UTC: {result.utc_time}</p>
            <p>Status: {result.status}</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default BirthChartForm