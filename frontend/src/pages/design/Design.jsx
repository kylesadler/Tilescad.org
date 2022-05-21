import React, { useState } from "react";
import { Alert, Snackbar, Typography } from "@mui/material";
import TileCanvas from "./TileCanvas";
import useMediaQuery from "@mui/material/useMediaQuery";
import COLORS from "./Colors";
import SidePanel from "./SidePanel";
import { uploadDesign } from "../../APIService";

const defaultTileTypes = [
  {
    name: "A",
    color: Object.values(COLORS.TILE_TYPES)[0],
    // naco: 30,
    // saco: 32,
    coreLength: 10,
  },
  {
    name: "B",
    color: Object.values(COLORS.TILE_TYPES)[1],
    // naco: 31,
    // saco: 33,
    coreLength: 0,
  },
  // { name: "B", color: COLORS.TILE_TYPES.BLUE },
  // { name: "C", color: COLORS.TILE_TYPES.GREEN },
];

defaultTileTypes.forEach((type, i) => {
  type.id = i;
  return type;
});

const defaultGridData = [...Array(16)].map((_, i) => {
  return [
    // defaultTileTypes[1].id,
    // defaultTileTypes[2].id,

    ...[...Array(14)].map((_, i) => {}),
  ];
});

const alphabet = "abcdefghijklmnopqrstuvwxyz".toUpperCase();
const numberToLetter = (i) => {
  return alphabet[i % alphabet.length];
};

const randInt = (max) => {
  return Math.floor(Math.random() * max);
};

const selectRandom = (arr) => {
  return arr[randInt(arr.length)];
};
const defaultActiveTileType = defaultTileTypes[0].id;

const getTileSize = (gridDim) => {
  // want tile canvas to be ~70% screen width
  // console.log("window.innerWidth");
  // console.log(window.innerWidth);

  //  why does this keep increasing??
  // let width = window.innerWidth;

  const width1500 = useMediaQuery("(min-width:1500px)");
  const width1000 = useMediaQuery("(min-width:1000px)");
  const width800 = useMediaQuery("(min-width:800px)");
  const width600 = useMediaQuery("(min-width:600px)");
  const width400 = useMediaQuery("(min-width:400px)");

  let width = 0;

  if (width1500) {
    width = 1500;
  } else if (width1000) {
    width = 1000;
  } else if (width800) {
    width = 800;
  } else if (width600) {
    width = 600;
  } else if (width400) {
    width = 400;
  }

  return Math.min(Math.max(Math.floor((width * 0.4) / gridDim), 50), 100);
};

const isNumber = (x) => {
  return !(isNaN(x) || x == null);
};

const dataIsValid = ({ grid, tileTypes }) => {
  // check diagonals starting on bottom of board
  for (let colIdx = 0; colIdx < grid.length; colIdx++) {
    let i = grid.length - 1;
    let j = colIdx;
    let coreLength = null;
    // currently at location i, j
    // console.log("checking right col", i, j);

    // while on board
    while (j >= 0 && i >= 0) {
      const selfId = grid[i][j];

      // if core length exists and is different, return false
      if (
        isNumber(selfId) &&
        tileTypes[selfId] &&
        isNumber(tileTypes[selfId].coreLength)
      ) {
        if (coreLength == null) {
          coreLength = tileTypes[selfId].coreLength;
          // console.log("core length", coreLength);
        } else if (coreLength != tileTypes[selfId].coreLength) {
          return false;
        }
      }

      // go to northwest neighbor
      i--;
      j--;
    }
  }

  // check diagonals starting on right side of board
  for (let rowIdx = 0; rowIdx < grid.length; rowIdx++) {
    let i = rowIdx;
    let j = grid.length - 1;
    let coreLength = null;

    // currently at location i, j
    // console.log("checking right col", i, j);

    while (j >= 0 && i >= 0) {
      const selfId = grid[i][j];

      // if core length exists and is different, return false
      if (
        isNumber(selfId) &&
        tileTypes[selfId] &&
        isNumber(tileTypes[selfId].coreLength)
      ) {
        if (coreLength == null) {
          coreLength = tileTypes[selfId].coreLength;
          // console.log("core length", coreLength);
        } else if (coreLength != tileTypes[selfId].coreLength) {
          return false;
        }
      }

      // go to northwest neighbor
      i--;
      j--;
    }
  }

  return true;
};

export default ({ defaultGridData, defaultGridDim }) => {
  const [domainLength, setDomainLength] = useState(6);
  // either id (number) or null
  const [activeTileType, setActiveTileType] = useState(defaultActiveTileType);

  const [tileTypes, setTileTypes] = useState(defaultTileTypes);

  const [gridDim, setGridDim] = useState(defaultGridDim || 10);

  const [gridData, setGridData] = useState(
    defaultGridData ||
      [...Array(gridDim)].map((_, i) => {
        return [...Array(gridDim)].map((_, j) => {
          if (0 <= i && i < 2 && 0 <= j && j < 2) return tileTypes[0].id;
        });
      })
  );

  const [error, setError] = useState(false);
  const handleClose = (event, reason) => {
    if (reason === "clickaway") {
      return;
    }

    setError(false);
  };

  const updateGrid = (rowIndex, colIndex) => {
    const newData = gridData.map((row, i) => {
      return row.map((tile, j) => {
        if (i != rowIndex || j != colIndex) {
          return tile;
        } else {
          return activeTileType;
        }
      });
    });
    setGridData(newData);
  };

  // const tileSize = getTileSize();
  const tileSize = getTileSize(gridDim);
  // console.log(tileSize, "tileSize");
  // console.log(tileSize, "tileSize");

  return (
    <div>
      <div
        style={{
          // padding: "20px 0px",
          width: "90%",
          margin: "auto",
          display: "flex",
          flexDirection: "column",
        }}
      >
        {/* <div
          style={{
            display: "flex",
            padding: 20,
            justifyContent: "center",
          }}
        >
          <Typography variant={"h3"}>Tile Assembly Editor</Typography>
        </div> */}
        <div style={{ display: "flex", justifyContent: "center" }}>
          <div style={{ width: gridDim * tileSize, padding: 15 }}>
            <TileCanvas
              gridData={gridData}
              width={gridDim}
              height={gridDim}
              tileSize={tileSize}
              tileTypes={tileTypes}
              activeTileType={activeTileType}
              onClick={(row, col) => {
                // console.log("clicked", row, col);
                updateGrid(row, col);
              }}
            />
          </div>
          <div
            style={{
              padding: 15,
              flexGrow: 1,
              minWidth: 350,
              maxWidth: 400,
            }}
          >
            <SidePanel
              onAdd={() => {
                const numTypes = tileTypes.length;
                const colors = Object.values(COLORS.TILE_TYPES);
                setTileTypes(
                  tileTypes.concat({
                    id: numTypes,
                    name: numberToLetter(numTypes),
                    color: colors[numTypes % colors.length],
                    coreLength: 0,
                  })
                );
                setActiveTileType(numTypes);
              }}
              onUpload={() => {
                // upload data to API, return promise with filename
                const data = {
                  // square grid of tile ids or null
                  grid: gridData.slice(0, gridDim).map((row) => {
                    return row.slice(0, gridDim).map((tileID) => {
                      return isNaN(tileID) || tileID == null
                        ? undefined
                        : tileID;
                    });
                  }),
                  domainLength,
                  tileTypes, // array[id] = tile
                };

                if (dataIsValid(data)) {
                  return uploadDesign(data);
                } else {
                  setError(true);
                  return Promise.reject();
                }
              }}
              domainLength={domainLength}
              setDomainLength={setDomainLength}
              gridDim={gridDim}
              setGridDim={(x) => {
                const value = parseInt(x);
                if (value > 25) return;

                const expansion = value - gridData.length;
                if (expansion > 0) {
                  // expand gridData if needed
                  const newGD = gridData.map((row) => {
                    return row.concat([...Array(expansion)]);
                  });
                  newGD.push(
                    ...[...Array(expansion)].map(() => {
                      return [...Array(value)];
                    })
                  );

                  // console.log(newGD);
                  setGridData(newGD);
                }
                if (value >= 5) setGridDim(value);
              }}
              gridData={gridData}
              tileTypes={tileTypes}
              setTileTypes={setTileTypes}
              activeTileType={activeTileType}
              setActiveTileType={setActiveTileType}
            />
          </div>
        </div>
        <Snackbar open={error} autoHideDuration={6000} onClose={handleClose}>
          <Alert onClose={handleClose} severity="error" sx={{ width: "100%" }}>
            All north east neighbors must have same core length
          </Alert>
        </Snackbar>
      </div>
    </div>
  );
};
