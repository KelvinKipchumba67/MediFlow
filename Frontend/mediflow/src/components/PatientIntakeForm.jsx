import { useState } from 'react';

export default function PatientIntakeForm() {
  const [formData, setFormData] = useState({
    patient_id: 'PAT-1042',
    age: 35,
    fever_duration_days: 0,
    cough_duration_days: 0,
    weight_loss_kg: 0.0,
    night_sweats: 0,
    hemoptysis: 0
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    let parsedValue;
    
    // SMART TRANSLATOR: Converts Checkboxes (True/False) to API Integers (1/0)
    if (type === 'checkbox') {
      parsedValue = checked ? 1 : 0;
    } else if (name === 'patient_id') {
      parsedValue = value; 
    } else if (name === 'weight_loss_kg') {
      parsedValue = parseFloat(value) || 0; 
    } else {
      parsedValue = parseInt(value, 10) || 0; 
    }

    setFormData({
      ...formData,
      [name]: parsedValue,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/triage', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        console.error("🚨 API Error Detail:", data);
        alert(`API Error: ${response.status} - Check browser console for details.`);
        setLoading(false);
        return; 
      }

      setResult(data);
    } catch (error) {
      console.error("Failed to fetch from API:", error);
      alert("Network Error: Make sure FastAPI is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-card">
      <h2 className="card-title">Context-Aware Triage System</h2>
      
      <form onSubmit={handleSubmit}>
        
        {/* SECTION 1: Demographics */}
        <h3 style={{ fontSize: '0.9rem', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '1rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>
          1. Patient Profile
        </h3>
        <div className="input-grid-3">
          <div className="input-group">
            <label>Patient ID</label>
            <input type="text" name="patient_id" value={formData.patient_id} onChange={handleChange} />
          </div>
          <div className="input-group">
            <label>Age</label>
            <input type="number" name="age" value={formData.age} onChange={handleChange} />
          </div>
          <div className="input-group">
            <label>Weight Loss (kg)</label>
            <input type="number" step="0.1" name="weight_loss_kg" value={formData.weight_loss_kg} onChange={handleChange} />
          </div>
        </div>

        {/* SECTION 2: Durations */}
        <h3 style={{ fontSize: '0.9rem', color: 'var(--text-muted)', textTransform: 'uppercase', margin: '1.5rem 0 1rem 0', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>
          2. Symptom Progression
        </h3>
        <div className="input-grid-2">
          <div className="input-group">
            <label>Cough Duration (Days)</label>
            <input type="number" name="cough_duration_days" value={formData.cough_duration_days} onChange={handleChange} />
          </div>
          <div className="input-group">
            <label>Fever Duration (Days)</label>
            <input type="number" name="fever_duration_days" value={formData.fever_duration_days} onChange={handleChange} />
          </div>
        </div>

        {/* SECTION 3: Clinical Red Flags (Toggles) */}
        <h3 style={{ fontSize: '0.9rem', color: 'var(--text-muted)', textTransform: 'uppercase', margin: '1.5rem 0 1rem 0', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>
          3. Clinical Red Flags
        </h3>
        <div className="input-grid-2">
          
          {/* Danger Toggle for Hemoptysis */}
          <div className="toggle-wrapper danger-zone">
            <p className="toggle-label" style={{ color: 'var(--danger)' }}>Hemoptysis (Coughing Blood)</p>
            <label className="switch">
              <input 
                type="checkbox" 
                name="hemoptysis" 
                checked={formData.hemoptysis === 1} 
                onChange={handleChange} 
              />
              <span className="slider danger-slider"></span>
            </label>
          </div>

          {/* Standard Toggle for Night Sweats */}
          <div className="toggle-wrapper">
            <p className="toggle-label">Night Sweats</p>
            <label className="switch">
              <input 
                type="checkbox" 
                name="night_sweats" 
                checked={formData.night_sweats === 1} 
                onChange={handleChange} 
              />
              <span className="slider"></span>
            </label>
          </div>

        </div>

        <button type="submit" className="btn-submit" disabled={loading} style={{ marginTop: '2rem' }}>
          {loading ? 'Analyzing Clinical Patterns...' : 'Run Triage Intelligence'}
        </button>
      </form>

      {/* Results Display */}
      {result && (
        <div className={`result-box ${result.triage_result?.includes("HIGH") ? 'high-risk' : 'low-risk'}`}>
          <h3 style={{ margin: 0, color: 'var(--text-main)' }}>Intelligence Report</h3>
          
          <div className="result-header">
            <div>
              <p style={{ margin: 0, fontSize: '0.875rem', color: 'var(--text-muted)' }}>Risk Assessment</p>
              <p className="risk-level">{result.triage_result}</p>
            </div>
            <div>
              <p style={{ margin: 0, fontSize: '0.875rem', color: 'var(--text-muted)' }}>Confidence Score</p>
              <p className="confidence-score">{result.confidence_score}</p>
            </div>
          </div>

          <div className="blockchain-data">
            <p><strong>Methodology:</strong> {result.methodology}</p>
            <p><strong>Blockchain Hash:</strong> {result.blockchain_payload?.prediction_hash || "Pending..."}</p>
          </div>
        </div>
      )}
    </div>
  );
}