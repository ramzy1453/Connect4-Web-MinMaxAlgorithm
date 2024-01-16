import { useState, useEffect } from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Home from "./components/Home";
import Game from "./components/Game";
import io from "socket.io-client";
import "./App.css";

function App() {
  const [ws, setWs] = useState("");

  useEffect(() => {
    const socket = io("http://localhost:5000");
    setWs(socket);

    return () => {
      socket.disconnect();
    };
  }, []);

  const router = createBrowserRouter([
    {
      path: "/",
      element: <Home />,
    },
    {
      path: "/human-vs-ai",
      element: <Game mode={1} socket={ws} player={1} />,
    },
    {
      path: "/ai-vs-human",
      element: <Game mode={1} socket={ws} player={-1} />,
    },
    {
      path: "/ai-vs-ai",
      element: <Game mode={2} socket={ws} player={1} />,
    },
  ]);

  return (
    <div className="App">
      {ws ? <RouterProvider router={router} /> : <div>Loading...</div>}
    </div>
  );
}

export default App;
