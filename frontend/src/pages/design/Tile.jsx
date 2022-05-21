import React, { useState } from "react";
import { Box, Typography } from "@mui/material";

export default ({ width, data, onClick, activeTileType }) => {
  const [display, setDisplay] = useState("none");
  // size is number of tiles in each grid dimension
  const { name, color } = data || {};

  const filled = !!data;

  return (
    <Box
      style={{ padding: 2 }}
      sx={{
        width,
        boxSizing: "border-box",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        cursor: "pointer",
        // "&:hover": {
        //   // backgroundColor: "green",
        //   // opacity: [0.9, 0.8, 0.7],
        //   // color: label ? "black" : "rgba(100,100,100,0.5)",
        // },
      }}
      onClick={onClick}
      onMouseEnter={
        filled
          ? undefined
          : (e) => {
              setDisplay("flex");
            }
      }
      onMouseLeave={
        filled
          ? undefined
          : (e) => {
              setDisplay("none");
            }
      }
    >
      {filled ? (
        <div
          style={{
            color: "white",
            fontWeight: 500,
            backgroundColor: color,
            width: "100%",
            height: "100%",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            overflow: "hidden",
          }}
        >
          <Typography variant={"body"} style={{ fontSize: "0.9rem" }}>
            {name || " "}
          </Typography>
        </div>
      ) : (
        <div
          style={{
            color: "rgba(100,100,100,0.5)",
            display,
            border: "1px dashed rgba(100,100,100,0.5)",
            borderRadius: 7,
            margin: "auto",
            width: "100%",
            height: "100%",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <div style={{ textAlign: "center" }}>
            {!isNaN(activeTileType) && activeTileType != null ? "Add" : "Clear"}
          </div>
        </div>
      )}
    </Box>
  );
};
