import { useState } from "react";
import CategoryManager from "./components/CategoryManager";
import TransactionManager from "./components/TransactionManager";
import Summary from "./components/Summary";

const tabs = ["Categories", "Transactions", "Summary"];

export default function App() {
  const [activeTab, setActiveTab] = useState("Categories");
  const [refreshKey, setRefreshKey] = useState(0);

  const triggerRefresh = () => setRefreshKey((k) => k + 1);

  return (
    <div style={{ maxWidth: 800, margin: "40px auto", padding: "0 20px" }}>
      <h1 style={{ marginBottom: 24, fontSize: 28 }}>💸 Clarity - Know your spends</h1>

      <div style={{ display: "flex", gap: 8, marginBottom: 28 }}>
        {tabs.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            style={{
              background: activeTab === tab ? "#222" : "#e2e2e2",
              color: activeTab === tab ? "#fff" : "#222",
              fontWeight: activeTab === tab ? 600 : 400,
            }}
          >
            {tab}
          </button>
        ))}
      </div>

      {activeTab === "Categories" && (
        <CategoryManager onchange={triggerRefresh} />
      )}
      {activeTab === "Transactions" && (
        <TransactionManager refreshKey={refreshKey} />
      )}
      {activeTab === "Summary" && <Summary refreshKey={refreshKey} />}
    </div>
  );
}