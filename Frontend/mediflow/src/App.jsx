import PatientIntakeForm from './components/PatientIntakeForm';

function App() {
  return (
    <div className="app-container">
      <header className="header">
        <h1 className="title">MediFlow</h1>
        <p className="subtitle">Pattern-Recognizing Clinical Intelligence</p>
      </header>
      
      <main>
        <PatientIntakeForm />
      </main>
    </div>
  );
}

export default App;