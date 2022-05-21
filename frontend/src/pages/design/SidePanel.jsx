import React, { createRef } from "react";
import { Button, styled, Typography, Card, Slider } from "@mui/material";
import TileTypeCard from "./TileTypeCard";
// import AddIcon from "@mui/icons-material/Add";

import COLORS from "./Colors";
import EditableField from "./EditableField";

const ColorButton = styled(Button)(({ theme }) => ({
  textTransform: "none",
  color: COLORS.WHITE,
  backgroundColor: COLORS.BLUE,
  "&:hover": {
    backgroundColor: COLORS.PINK,
  },
}));

const PlainButton = styled(Button)(({ theme }) => ({
  color: COLORS.WHITE,
  backgroundColor: COLORS.GRAY,
  "&:hover": {
    backgroundColor: COLORS.LIGHT_GRAY,
  },
}));

export default ({
  onUpload,
  domainLength,
  setDomainLength,
  gridDim,
  setGridDim,
  gridData,
  tileTypes,
  setTileTypes,
  activeTileType,
  setActiveTileType,
  onAdd,
}) => {
  const hiddenForm = createRef();
  const filenameInput = createRef();
  return (
    <div style={{ display: "flex", flexDirection: "column" }}>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          padding: 10,
        }}
      >
        <div
          style={{
            width: "100%",
            paddingBottom: 20,
            display: "flex",
            justifyContent: "center",
          }}
        >
          <ColorButton
            style={{ width: 200, padding: 10 }}
            onClick={() => {
              // todo run validation logic

              onUpload()
                .then((filename) => {
                  if (filename) {
                    // console.log(filename);
                    filenameInput.current.setAttribute("value", filename);
                    hiddenForm.current.submit();
                  }
                })
                .catch((e) => {
                  // todo give error messages
                  console.log(e);
                });
            }}
          >
            <Typography style={{ fontWeight: "bold" }}>
              Export to Scadnano
            </Typography>
          </ColorButton>
        </div>

        <div style={{ width: "100%", display: "flex" }}>
          {/* <Typography style={{ display: "block" }}>Canvas Size</Typography>
          <Slider
            max={20}
            min={5}
            defaultValue={gridDim}
            step={1}
            valueLabelDisplay="auto"
            onChange={(event) => {
              console.log(event);
              setGridDim(event.target.value);
            }}
          /> */}

          <EditableField
            label={"Canvas Size"}
            value={gridDim}
            onChange={setGridDim}
          />
          <EditableField
            label={"Domain Lengths"}
            value={domainLength}
            onChange={setDomainLength}
          />
        </div>
      </div>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          overflow: "scroll",
          //   maxHeight: // 500, for some reason this doesn't work?
        }}
      >
        {tileTypes.map((tileType, i) => {
          return (
            <div style={{ padding: 10, width: "100%" }}>
              <TileTypeCard
                tileType={tileType}
                onClick={() => {
                  if (activeTileType != i) {
                    setActiveTileType(i);
                  } else {
                    setActiveTileType(null);
                  }
                }}
                selected={activeTileType == i}
                onChange={(newValues) => {
                  setTileTypes(
                    tileTypes.map((oldTileType, j) => {
                      if (i == j) {
                        return newValues;
                      } else {
                        return oldTileType;
                      }
                    })
                  );
                }}
              />
            </div>
          );
        })}
      </div>
      <div style={{ padding: "0px 10px", width: "100%" }}>
        <PlainButton style={{ width: "100%" }} onClick={onAdd}>
          <Typography style={{ fontWeight: "bold" }}>Add +</Typography>
        </PlainButton>
      </div>
      {/* hidden form so user can download scadnano file */}
      <form ref={hiddenForm} action="/api/download-file" method="POST">
        <input ref={filenameInput} type="hidden" name="filename" value="null" />
      </form>
    </div>
  );
};
