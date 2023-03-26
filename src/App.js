import './App.css';
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "./components/LoginPage";
import CreateMatch from './components/CreateMatch';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };
  // const match = ["piti", "yosef"];

  // const [currentTime, setCurrentTime] = useState(0);

  return (
    <Router>
      {isLoggedIn}
      <Routes>
        <Route
          exac
          path="/"
          exact={true}
          element={<LoginPage onLogin={handleLogin} />}
        />
        <Route path='/players' element={<CreateMatch />} />

      </Routes>
    </Router >

  );
}



export default App;
// {
//   match.map((player) => (


//     <ListGroup>
//       <ListGroup.Item variant='Primary'>{player} </ListGroup.Item>
//     </ListGroup>
//   ))}
// <p>The c