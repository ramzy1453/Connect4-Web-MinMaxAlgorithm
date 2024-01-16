import React, { useState } from "react";
import { Grid, Typography, Box, Modal } from "@mui/material";
import { Link } from "react-router-dom";

function Home() {
  const [showModal, setShowModal] = useState(false);

  return (
    <div className="">
      <h1 className="my-8 font-black text-4xl">Connect4 Game</h1>
      <div className="flex justify-center items-center flex-col space-y-8">
        <Link className="btn btn-primary" to="/human-vs-ai">
          Human vs AI
        </Link>
        <Link className="btn btn-primary" to="/ai-vs-human">
          AI vs Human
        </Link>
        <Link className="btn btn-primary" to="/ai-vs-ai">
          AI bot 1 vs AI bot 2
        </Link>
      </div>
    </div>
  );
}

export default Home;
