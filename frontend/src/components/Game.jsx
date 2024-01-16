import { useState, useEffect } from "react";
import Board from "./Board";
import { Grid, Box, Typography } from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import { Link } from "react-router-dom";

function Game(props) {
  const [player, setPlayer] = useState(props.player);
  const [timeLeft, setTimeLeft] = useState(30);
  const [Running, setRunning] = useState(false);
  const mode = props.mode;
  const [winner, setWinner] = useState(null);
  const [matchNul, setMatchNul] = useState(false);
  const [response, setResponse] = useState({
    gameState: 0,
    board: Array(6).fill(Array(7).fill(0)),
    returned: false,
  });
  const [showStart, setshowStart] = useState(true);

  useEffect(() => {
    props.socket.on("response", (data) => {
      if (data.Err === 0) {
        const newResponse = {
          gameState: data.GameState,
          board: data.board,
          returned: true,
        };
        setResponse(newResponse);
        console.log("response : " + data);
      } else alert("choose another column");
    });
  }, [props.socket]);

  useEffect(() => {
    if (response.returned) {
      console.log("Updated gameState:", response.gameState);
      if (response.gameState === player) {
        setWinner(player === 1 ? "red" : "blue");
        setMatchNul(false);
        stopTimer();
        return;
      } else if (response.gameState === 2) {
        setMatchNul(true);
        stopTimer();
        return;
      }
      setPlayer(player * -1);
    }
  }, [response]);

  useEffect(() => {
    if (response.returned) {
      console.log(player, "s turn");
      setTimeLeft(30);
    }
  }, [player]);

  useEffect(() => {
    if (response.returned) {
      const newResponse = {
        gameState: response.gameState,
        board: response.board,
        returned: false,
      };
      setResponse(newResponse);
      if ((mode === 2 || (mode === 1 && player === -1)) && Running) {
        handleAiMove();
      }
    }
  }, [timeLeft]);

  const handleMove = (col) => {
    if (mode === 1 && player === 1 && props.socket && Running) {
      console.log("you use board:", response.board);
      props.socket.emit("play_event", {
        board: response.board,
        turn: player, // 1 or -1
        mode: mode, // 1 or 2
        play_col: col, // -1 if AI turn else humen selection
      });
      // if err affichage and return
    }
  };

  const handleAiMove = async () => {
    if (props.socket && Running) {
      await delay(1000);
      console.log("bot use board:", response.board);
      props.socket.emit("play_event", {
        board: response.board,
        turn: player, // 1 or -1
        mode: mode, // 1 or 2
        play_col: -1, // -1 if AI turn else humen selection
      });
    }
  };
  const Start = () => {
    setshowStart(false);
    startTimer();
  };
  const delay = (milliseconds) => {
    return new Promise((resolve) => {
      setTimeout(resolve, milliseconds);
    });
  };
  const restart = () => {
    const newResponse = {
      gameState: 0,
      board: Array(6).fill(Array(7).fill(0)),
      returned: false,
    };
    setResponse(newResponse);
    setPlayer(props.player);
    setTimeLeft(30);
    stopTimer();
    setshowStart(true);
  };
  const stopTimer = () => {
    setRunning(false);
  };
  const startTimer = () => {
    setRunning(true);
  };
  useEffect(() => {
    // Timer inc and time out
    if (Running) {
      if (timeLeft > 0) {
        const timer = setTimeout(() => setTimeLeft((prev) => prev - 1), 1000);
        return () => clearTimeout(timer);
      } else {
        handleTurnEnd();
      }
    }
  }, [Running, timeLeft]);

  useEffect(() => {
    if (Running) {
      if (mode === 2) {
        handleAiMove();
      } else if (player === -1) handleAiMove();
    }
  }, [Running]);

  useEffect(() => {
    if (matchNul) {
      alert("Match Nul");
    } else if (winner && !matchNul) {
      alert("Player {winner} wins!");
    }
  }, [matchNul]);

  const handleTurnEnd = () => {
    alert("Khlas lwa9t");
    if (props.socket) {
      props.socket.emit("timeout_event", {
        board: response.board,
        turn: player,
        mode: mode,
        play_col: -1,
      });
    }
  };
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        width: "100vw",
        height: "100vh",
      }}
    >
      <Box component={Link} to={"/"}>
        <ArrowBackIcon
          sx={{
            position: "absolute",
            top: 5,
            left: 5,
            padding: "10px",
            color: "white",
            "&:hover": {
              transition: "all 0.5s ease-in-out",
              backgroundColor: "rgba(255, 255, 255, 0.2)",
            },
          }}
        />
      </Box>
      <Grid
        container
        spacing={5}
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        {showStart && (
          <Grid item>
            <button className="btn btn-info" onClick={Start}>
              <Typography
                sx={{ fontSize: { xs: "0.6rem", sm: "0.8rem", md: "1rem" } }}
              >
                PLAY
              </Typography>
            </button>
          </Grid>
        )}
        <Grid item>
          <button className="btn btn-info" onClick={restart}>
            <Typography
              sx={{ fontSize: { xs: "0.6rem", sm: "0.8rem", md: "1rem" } }}
            >
              REPLAY
            </Typography>
          </button>
        </Grid>
      </Grid>
      <Board board={response.board} turn={player} onClick={handleMove} />
    </Box>
  );
}

export default Game;
