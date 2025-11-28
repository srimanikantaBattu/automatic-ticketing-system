import React, { useState } from 'react';
import { api } from '../services/api';

const TicketForm = ({ onTicketCreated }) => {
  const [formData, setFormData] = useState({
    submitter: '',
    subject: '',
    description: '',
    urgency: 'Medium'
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    try {
      const data = await api.createTicket(formData);
      setMessage({ type: 'success', text: `Ticket created! ID: ${data.ticket_id}` });
      setFormData({ submitter: '', subject: '', description: '', urgency: 'Medium' });
      if (onTicketCreated) onTicketCreated();
    } catch (error) {
      setMessage({ type: 'error', text: error.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>Submit New Ticket</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Email:</label>
          <input
            type="email"
            name="submitter"
            value={formData.submitter}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label>Subject:</label>
          <input
            type="text"
            name="subject"
            value={formData.subject}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label>Urgency:</label>
          <select name="urgency" value={formData.urgency} onChange={handleChange}>
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
            <option value="Critical">Critical</option>
          </select>
        </div>
        <div className="form-group">
          <label>Category (Optional):</label>
          <select name="category" value={formData.category || ''} onChange={handleChange}>
            <option value="">-- Let AI Decide --</option>
            <option value="Hardware">Hardware</option>
            <option value="Software">Software</option>
            <option value="Network">Network</option>
            <option value="Access">Access</option>
            <option value="Security">Security</option>
            <option value="Billing">Billing</option>
            <option value="Other">Other</option>
          </select>
        </div>
        <div className="form-group">
          <label>Description:</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
            rows="4"
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Processing with AI...' : 'Submit Ticket'}
        </button>
      </form>
      {message && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}
    </div>
  );
};

export default TicketForm;
