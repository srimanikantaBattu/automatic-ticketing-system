import React, { useEffect, useState } from 'react';
import { api } from '../services/api';

const Dashboard = ({ refreshTrigger }) => {
  const [tickets, setTickets] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState('All');
  const [filterPriority, setFilterPriority] = useState('All');

  const fetchData = async () => {
    setLoading(true);
    try {
      const [ticketsData, statsData] = await Promise.all([
        api.getTickets(),
        api.getStats()
      ]);

      setTickets(ticketsData);
      setStats(statsData);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [refreshTrigger]);

  const handleOverride = async (ticketId, field, value) => {
    try {
      await api.updateTicket(ticketId, { [field]: value });
      fetchData(); // Refresh data
    } catch (error) {
      console.error("Error updating ticket:", error);
    }
  };

  const filteredTickets = tickets.filter(ticket => {
    if (filterStatus !== 'All' && ticket.status !== filterStatus) return false;
    if (filterPriority !== 'All' && ticket.priority !== filterPriority) return false;
    return true;
  });

  if (loading && tickets.length === 0) return <div>Loading Dashboard...</div>;

  return (
    <div className="dashboard">
      <h2>Live Operations Dashboard</h2>
      
      {stats && (
        <div className="stats-container">
          <div className="stat-card">
            <h3>Total Tickets</h3>
            <p>{stats.total_tickets}</p>
          </div>
          <div className="stat-card">
            <h3>Critical Issues</h3>
            <p className="critical">{stats.priority_breakdown?.Critical || 0}</p>
          </div>
          <div className="stat-card">
            <h3>High Priority</h3>
            <p className="high">{stats.priority_breakdown?.High || 0}</p>
          </div>
        </div>
      )}

      <div className="filters">
        <label>
          Filter Priority:
          <select value={filterPriority} onChange={(e) => setFilterPriority(e.target.value)}>
            <option value="All">All</option>
            <option value="Critical">Critical</option>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>
        </label>
        <label style={{ marginLeft: '1rem' }}>
          Filter Status:
          <select value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)}>
            <option value="All">All</option>
            <option value="new">New</option>
            <option value="in_progress">In Progress</option>
            <option value="resolved">Resolved</option>
          </select>
        </label>
      </div>

      <h3>Recent Tickets</h3>
      <div className="tickets-list">
        {filteredTickets.length === 0 ? (
          <p>No tickets match your filters.</p>
        ) : (
          filteredTickets.slice().reverse().map((ticket) => (
            <div key={ticket.ticket_id} className={`ticket-card priority-${ticket.priority?.toLowerCase() || 'medium'}`}>
              <div className="ticket-header">
                <span className="ticket-id">{ticket.ticket_id}</span>
                <div className="controls">
                    <select 
                        value={ticket.priority} 
                        onChange={(e) => handleOverride(ticket.ticket_id, 'priority', e.target.value)}
                        className={`badge ${ticket.priority?.toLowerCase()}`}
                    >
                        <option value="Low">Low</option>
                        <option value="Medium">Medium</option>
                        <option value="High">High</option>
                        <option value="Critical">Critical</option>
                    </select>
                    <select 
                        value={ticket.category} 
                        onChange={(e) => handleOverride(ticket.ticket_id, 'category', e.target.value)}
                        className="badge category"
                    >
                        <option value={ticket.category}>{ticket.category}</option>
                        <option value="Hardware">Hardware</option>
                        <option value="Software">Software</option>
                        <option value="Network">Network</option>
                        <option value="Access">Access</option>
                        <option value="Security">Security</option>
                    </select>
                </div>
              </div>
              <h4>{ticket.subject}</h4>
              <p className="description">{ticket.description}</p>
              
              <div className="ai-insights">
                <h5>🤖 AI Insights</h5>
                <p><strong>Suggested Team:</strong> {ticket.suggested_team}</p>
                <p><strong>Confidence:</strong> {(ticket.confidence_score * 100).toFixed(1)}%</p>
                {ticket.ai_category && ticket.ai_category !== ticket.category && (
                    <p className="override-notice">
                        <em>Original AI Category: {ticket.ai_category}</em>
                    </p>
                )}
                <details>
                  <summary>View Auto-Response</summary>
                  <p className="auto-response">{ticket.auto_response}</p>
                </details>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Dashboard;
