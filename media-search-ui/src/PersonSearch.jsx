import { useState } from "react";
import axios from "axios";

function PersonSearch({ token }) {
  const [results, setResults] = useState([]);
  const [filters, setFilters] = useState({ name: "", profession: "", movie_title: "" });

  const handleSearch = async () => {
    const params = new URLSearchParams(filters);
    const res = await axios.get(`http://localhost:5000/people?${params}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    setResults(res.data);
  };

  return (
    <div>
      <h2>Search People</h2>
      <input placeholder="Name" onChange={e => setFilters({ ...filters, name: e.target.value })} />
      <input placeholder="Profession" onChange={e => setFilters({ ...filters, profession: e.target.value })} />
      <input placeholder="Movie Title" onChange={e => setFilters({ ...filters, movie_title: e.target.value })} />
      <button onClick={handleSearch}>Search</button>

      <div className="grid">
        {results.map((p, i) => (
          <div key={i} className="card">
            <h3>{p.Name}</h3>
            <p>Born: {p["Birth Year"]} | {p.Profession}</p>
            <p>Known for: {p["Known for Titles"].join(", ")}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default PersonSearch;