import { useEffect, useState } from "react";
import client from "../api/client";

export default function TransactionManager({ refreshKey }) {
  const [transactions, setTransactions] = useState([]);
  const [categories, setCategories] = useState([]);
  const [form, setForm] = useState({ description: "", amount: "", date: "", category_id: "" });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [filterCategory, setFilterCategory] = useState("");

  const fetchAll = async () => {
    const [txRes, catRes] = await Promise.all([
      client.get("/transactions/", { params: filterCategory ? { category_id: filterCategory } : {} }),
      client.get("/categories/"),
    ]);
    setTransactions(txRes.data);
    setCategories(catRes.data);
  };

  useEffect(() => { fetchAll(); }, [refreshKey, filterCategory]);

  const handleCreate = async () => {
    setError("");
    setSuccess("");
    try {
      await client.post("/transactions/", {
        ...form,
        amount: parseFloat(form.amount),
        category_id: parseInt(form.category_id),
      });
      setForm({ description: "", amount: "", date: "", category_id: "" });
      setSuccess("Transaction added.");
      fetchAll();
    } catch (err) {
      const errors = err.response?.data?.errors;
      const msg = errors
        ? Object.values(errors).flat().join(" ")
        : err.response?.data?.error || "Something went wrong.";
      setError(msg);
    }
  };

  const handleDelete = async (id) => {
    setError("");
    setSuccess("");
    try {
      await client.delete(`/transactions/${id}`);
      setSuccess("Transaction deleted.");
      fetchAll();
    } catch {
      setError("Could not delete transaction.");
    }
  };

  return (
    <div>
      <h2 style={{ marginBottom: 16 }}>Transactions</h2>

      <div style={{ display: "flex", flexDirection: "column", gap: 8, marginBottom: 16, maxWidth: 400 }}>
        <input placeholder="Description" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
        <input type="number" placeholder="Amount" value={form.amount} onChange={(e) => setForm({ ...form, amount: e.target.value })} />
        <input type="date" value={form.date} onChange={(e) => setForm({ ...form, date: e.target.value })} />
        <select value={form.category_id} onChange={(e) => setForm({ ...form, category_id: e.target.value })}>
          <option value="">Select category</option>
          {categories.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
        <button onClick={handleCreate} style={{ background: "#222", color: "#fff" }}>
          Add Transaction
        </button>
        {error && <p className="error">{error}</p>}
        {success && <p className="success">{success}</p>}
      </div>

      <div style={{ marginBottom: 16, maxWidth: 400 }}>
        <select value={filterCategory} onChange={(e) => setFilterCategory(e.target.value)}>
          <option value="">All Categories</option>
          {categories.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
      </div>

      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ borderBottom: "2px solid #ddd", textAlign: "left" }}>
            <th style={{ padding: "8px 0" }}>Description</th>
            <th style={{ padding: "8px 0" }}>Amount</th>
            <th style={{ padding: "8px 0" }}>Date</th>
            <th style={{ padding: "8px 0" }}>Category</th>
            <th style={{ padding: "8px 0" }}>Action</th>
          </tr>
        </thead>
        <tbody>
          {transactions.length === 0 && (
            <tr><td colSpan={5} style={{ padding: "12px 0", color: "#888" }}>No transactions yet.</td></tr>
          )}
          {transactions.map((tx) => (
            <tr key={tx.id} style={{ borderBottom: "1px solid #eee" }}>
              <td style={{ padding: "10px 0" }}>{tx.description}</td>
              <td style={{ padding: "10px 0" }}>₹{tx.amount.toFixed(2)}</td>
              <td style={{ padding: "10px 0" }}>{tx.date}</td>
              <td style={{ padding: "10px 0" }}>{tx.category?.name || "—"}</td>
              <td style={{ padding: "10px 0" }}>
                <button onClick={() => handleDelete(tx.id)} style={{ background: "#fee2e2", color: "#c53030" }}>
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}