import React, { useState } from "react";
import axios from "axios";

function App() {
  const [formData, setFormData] = useState({
    phone_number: "",
    email: "",
    credit_score: "",
    age_group: "18-25",
    family_background: "Single",
    income: "",
    comments: "",
    consent: false,
  });

  const [leadList, setLeadList] = useState([]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.consent) {
      alert("Please provide consent.");
      return;
    }

    try {
      const payload = { ...formData };
      delete payload.consent;

      const res = await axios.post("http://127.0.0.1:8000/score", payload);

      const newLead = {
        ...formData,
        initial_score: res.data.initial_score,
        reranked_score: res.data.reranked_score,
      };

      setLeadList((prev) => [newLead, ...prev]);
    } catch (err) {
      console.error(err);
      alert("Error scoring lead. Check console.");
    }
  };

  const formStyle = {
    background: "#f9f9f9",
    padding: "20px",
    borderRadius: "8px",
    boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
    marginBottom: "20px",
  };

  const inputStyle = {
    width: "100%",
    padding: "10px",
    margin: "8px 0",
    borderRadius: "4px",
    border: "1px solid #ccc",
  };

  const buttonStyle = {
    padding: "12px 20px",
    background: "#4CAF50",
    color: "white",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
  };

  return (
    <div style={{ maxWidth: "700px", margin: "auto", padding: "20px" }}>
      <h1>AI Lead Scoring Dashboard</h1>

      <form onSubmit={handleSubmit} style={formStyle}>
        <input
          type="text"
          name="phone_number"
          placeholder="Phone Number"
          value={formData.phone_number}
          onChange={handleChange}
          required
          style={inputStyle}
        />

        <input
          type="email"
          name="email"
          placeholder="Email Address"
          value={formData.email}
          onChange={handleChange}
          required
          style={inputStyle}
        />

        <input
          type="number"
          name="credit_score"
          placeholder="Credit Score (300–850)"
          value={formData.credit_score}
          onChange={handleChange}
          required
          style={inputStyle}
        />

        <select
          name="age_group"
          value={formData.age_group}
          onChange={handleChange}
          style={inputStyle}
        >
          <option value="18-25">18–25</option>
          <option value="26-35">26–35</option>
          <option value="36-50">36–50</option>
          <option value="51+">51+</option>
        </select>

        <select
          name="family_background"
          value={formData.family_background}
          onChange={handleChange}
          style={inputStyle}
        >
          <option value="Single">Single</option>
          <option value="Married">Married</option>
          <option value="Divorced">Divorced</option>
        </select>

        <input
          type="number"
          name="income"
          placeholder="Income (INR)"
          value={formData.income}
          onChange={handleChange}
          required
          style={inputStyle}
        />

        <textarea
          name="comments"
          placeholder="Comments"
          value={formData.comments}
          onChange={handleChange}
          style={inputStyle}
          rows="3"
        />

        <label>
          <input
            type="checkbox"
            name="consent"
            checked={formData.consent}
            onChange={handleChange}
            style={{ marginRight: "10px" }}
          />
          I consent to data processing
        </label>

        <br />
        <button type="submit" style={{ ...buttonStyle, marginTop: "10px" }}>
          Submit Lead
        </button>
      </form>

      {leadList.length > 0 && (
        <table
          border="1"
          cellPadding="8"
          cellSpacing="0"
          style={{ width: "100%", borderCollapse: "collapse" }}
        >
          <thead style={{ background: "#f0f0f0" }}>
            <tr>
              <th>Email</th>
              <th>Initial Score</th>
              <th>Reranked Score</th>
              <th>Comments</th>
            </tr>
          </thead>
          <tbody>
            {leadList.map((lead, index) => (
              <tr key={index}>
                <td>{lead.email}</td>
                <td>{lead.initial_score}</td>
                <td>{lead.reranked_score}</td>
                <td>{lead.comments}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;
