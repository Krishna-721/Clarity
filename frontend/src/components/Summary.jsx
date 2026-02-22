import { useEffect, useState } from "react";
import client from "../api/client";

export default function Summary({ refreshKey }) {
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    client.get("/summary/").then((res) => setSummary(res.data));
  }, [refreshKey]);

  if (!summary) return <p>Loading...</p>;

  return (
    <div>
      <h2 style={{ marginBottom: 16 }}>Summary</h2>

      <div style={{
        background: "#222", color: "#fff", borderRadius: 10,
        padding: "20px 24px", marginBottom: 24, maxWidth: 300
      }}>
        <p style={{ fontSize: 14, opacity: 0.7, marginBottom: 4 }}>Total Spent</p>
        <p style={{ fontSize: 32, fontWeight: 700 }}>₹{summary.overall_total.toFixed(2)}</p>
      </div>

      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ borderBottom: "2px solid #ddd", textAlign: "left" }}>
            <th style={{ padding: "8px 0" }}>Category</th>
            <th style={{ padding: "8px 0" }}>Transactions</th>
            <th style={{ padding: "8px 0" }}>Total Spent</th>
          </tr>
        </thead>
        <tbody>
          {summary.breakdown.length === 0 && (
            <tr><td colSpan={3} style={{ padding: "12px 0", color: "#888" }}>No data yet.</td></tr>
          )}
          {summary.breakdown.map((row) => (
            <tr key={row.category_id} style={{ borderBottom: "1px solid #eee" }}>
              <td style={{ padding: "10px 0" }}>{row.category_name}</td>
              <td style={{ padding: "10px 0" }}>{row.transaction_count}</td>
              <td style={{ padding: "10px 0" }}>₹{row.total_spent.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}