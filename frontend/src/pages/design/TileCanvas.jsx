import { Card } from "@mui/material";
import React from "react";
import Tile from "./Tile";

export default ({
  gridData,
  onClick,
  width,
  height,
  tileSize,
  tileTypes,
  activeTileType,
}) => {
  //gridData [[{ lable, color, }]]
  // onClick = (rowNum, colNum) => {}
  // width, height are in terms of tiles

  return (
    <Card
      style={{
        display: "flex",
        padding: 10,
        justifyContent: "space-between",
        flexDirection: "column",
        border: "1px solid #b8b8b8",
      }}
    >
      {gridData.slice(0, height).map((row, i) => {
        return (
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              width: "100%",
              height: tileSize,
              overflow: "hidden",
            }}
          >
            {row.slice(0, width).map((tile, j) => {
              return (
                <Tile
                  width={tileSize}
                  activeTileType={activeTileType}
                  data={!isNaN(tile) ? tileTypes[tile] : null}
                  onClick={() => {
                    onClick(i, j);
                  }}
                />
              );
            })}
          </div>
        );
      })}
    </Card>
  );
};
