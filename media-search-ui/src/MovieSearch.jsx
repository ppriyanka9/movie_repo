import axios from "axios";
import { useState } from "react";

function MovieSearch({ token }) {
  const [results, setResults] = useState([]);
  const [filters, setFilters] = useState({ year: "", genre: "", type: "", person_name: "" });

  const handleSearch = async () => {
    const params = new URLSearchParams(filters);
    const res = await axios.get(`http://localhost:5000/movies?${params}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    alert(res);
    setResults(res.data);
  };

  return (
    <div>
      <h2>Search Movies</h2>
      <input placeholder="Year" onChange={e => setFilters({ ...filters, year: e.target.value })} />
      <input placeholder="Genre" onChange={e => setFilters({ ...filters, genre: e.target.value })} />
      <input placeholder="Type" onChange={e => setFilters({ ...filters, type: e.target.value })} />
      <input placeholder="Person Name" onChange={e => setFilters({ ...filters, person_name: e.target.value })} />
      <button onClick={handleSearch}>Search</button>

      <div className="grid">
        {results.map((m, i) => (
          <div key={i} className="card">
            <h3>{m.Title}</h3>
            <p>{m.Type} | {m.Genre} | {m["Year Released"]}</p>
            <p>People: {m["List of People Associated"].join(", ")}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default MovieSearch;