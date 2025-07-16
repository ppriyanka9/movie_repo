import React, { useState } from "react";
import MovieSearch from "./MovieSearch";
import PersonSearch from "./PersonSearch";
import axios from "axios";

function App() {
  const [token, setToken] = useState("");
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("password123");
  const [loggedIn, setLoggedIn] = useState(false);

  const handleLogin = async () => {
    try {
      const res = await axios.post("http://localhost:5000/login", {
        username,
        password,
      });
      setToken(res.data.access_token);
      setLoggedIn(true);
    } catch (err) {
      alert("Login failed");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      {!loggedIn ? (
        <div>
          <h2>Login</h2>
          <input
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            placeholder="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button onClick={handleLogin}>Login</button>
        </div>
      ) : (
        <>
          <h1>Media Search App</h1>
          <MovieSearch token={token} />
          <hr />
          <PersonSearch token={token} />
        </>
      )}
    </div>
  );
}

export default App;