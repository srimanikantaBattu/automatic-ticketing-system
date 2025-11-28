import React, { useState } from 'react';
import TicketForm from './components/TicketForm';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
  const [refreshDashboard, setRefreshDashboard] = useState(0);

  const handleTicketCreated = () => {
    setRefreshDashboard(prev => prev + 1);
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Smart Ticketing Automation Platform</h1>
        <p>AI-Driven IT Support & Classification</p>
      </header>
      
      <main className="main-content">
        <div className="left-panel">
          <TicketForm onTicketCreated={handleTicketCreated} />
        </div>
        <div className="right-panel">
          <Dashboard refreshTrigger={refreshDashboard} />
        </div>
      </main>
    </div>
  );
}

export default App;
