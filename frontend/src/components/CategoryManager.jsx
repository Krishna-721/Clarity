import { useEffect, useState } from "react";
import client from "../api/client";

export default function CategoryManager({ onchange }) {
  const [categories, setCategories] = useState([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const fetchCategories = async () => {
    const res = await client.get("/categories/");
    setCategories(res.data);
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  const handleCreate = async () => {
    setError("");
    setSuccess("");
    try {
      await client.post("/categories/", { name, description });
      setName("");
      setDescription("");
      setSuccess("Category created.");
      fetchCategories();
      onchange();
    } catch (err) {
      const msg = err.response?.data?.errors?.name?.[0] || err.response?.data?.error || "Something went wrong.";
      setError(msg);
    }
  };

  const handleDelete = async (id) => {
    setError("");
    setSuccess("");
    try {
      await client.delete(`/categories/${id}`);
      setSuccess("Category deleted.");
      fetchCategories();
      onchange();
    } catch (err) {
      const msg = err.response?.data?.error || "Could not delete category.";
      setError(msg);
    }
  };

  return (
    <div>
      <h2 style={{ marginBottom: 16 }}>Categories</h2>

      <div style={{ display: "flex", flexDirection: "column", gap: 8, marginBottom: 16, maxWidth: 400 }}>
        <input placeholder="Category name" value={name} onChange={(e) => setName(e.target.value)} />
        <input placeholder="Description (optional)" value={description} onChange={(e) => setDescription(e.target.value)} />
        <button onClick={handleCreate} style={{ background: "#222", color: "#fff" }}>
          Add Category
        </button>
        {error && <p className="error">{error}</p>}
        {success && <p className="success">{success}</p>}
      </div>

      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ borderBottom: "2px solid #ddd", textAlign: "left" }}>
            <th style={{ padding: "8px 0" }}>Name</th>
            <th style={{ padding: "8px 0" }}>Description</th>
            <th style={{ padding: "8px 0" }}>Action</th>
          </tr>
        </thead>
        <tbody>
          {categories.length === 0 && (
            <tr><td colSpan={3} style={{ padding: "12px 0", color: "#888" }}>No categories yet.</td></tr>
          )}
          {categories.map((cat) => (
            <tr key={cat.id} style={{ borderBottom: "1px solid #eee" }}>
              <td style={{ padding: "10px 0" }}>{cat.name}</td>
              <td style={{ padding: "10px 0", color: "#666" }}>{cat.description || "—"}</td>
              <td style={{ padding: "10px 0" }}>
                <button onClick={() => handleDelete(cat.id)} style={{ background: "#fee2e2", color: "#c53030" }}>
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