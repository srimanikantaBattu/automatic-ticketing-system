const API_URL = 'http://localhost:8000';

export const api = {
  async createTicket(ticketData) {
    const response = await fetch(`${API_URL}/tickets/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(ticketData),
    });
    if (!response.ok) throw new Error('Failed to create ticket');
    return response.json();
  },

  async getTickets() {
    const response = await fetch(`${API_URL}/tickets/`);
    if (!response.ok) throw new Error('Failed to fetch tickets');
    return response.json();
  },

  async getTicket(id) {
    const response = await fetch(`${API_URL}/tickets/${id}`);
    if (!response.ok) throw new Error('Failed to fetch ticket');
    return response.json();
  },

  async updateTicket(id, updateData) {
    const response = await fetch(`${API_URL}/tickets/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updateData),
    });
    if (!response.ok) throw new Error('Failed to update ticket');
    return response.json();
  },

  async getStats() {
    const response = await fetch(`${API_URL}/stats/summary`);
    if (!response.ok) throw new Error('Failed to fetch stats');
    return response.json();
  }
};
