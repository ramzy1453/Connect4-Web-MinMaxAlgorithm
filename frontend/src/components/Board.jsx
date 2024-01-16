import React, { useState } from "react";
import { Grid, Paper } from "@mui/material";

function Board(props) {
  const renderCell = (cellValue, colIndex) => {
    const discColor =
      cellValue === 1 ? "red" : cellValue === -1 ? "blue" : "#FFFFFF10";

    return (
      <Paper
        sx={{
          height: { xs: 30, sm: 50, md: 60 },
          width: { xs: 30, sm: 50, md: 60 },
          backgroundColor: discColor,
          margin: "auto",
        }}
      />
    );
  };

  const renderBoard = () => (
    <Grid container spacing={0} justifyContent="center">
      {props.board.map((row, rowIndex) => (
        <Grid key={rowIndex} item container spacing={0} justifyContent="center">
          {row.map((cellValue, colIndex) => (
            <Grid key={colIndex} onClick={() => props.onClick(colIndex)} item>
              {renderCell(cellValue, colIndex)}
            </Grid>
          ))}
        </Grid>
      ))}
    </Grid>
  );

  return <div style={{ padding: "20px" }}>{renderBoard()}</div>;
}

export default Board;
