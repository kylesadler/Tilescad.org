import React from "react";
import { Box, Card, Typography, Collapse } from "@mui/material";
import EditableField from "./EditableField";

// const PaddedBox = ({ children }) => {
//   return <Box style={{ padding: "15px 0px" }}>{children}</Box>;
// };

// import ColorPicker from "material-ui-color-picker";
import Colors from "./Colors";

// export default ({ title, labels, values, onChange }) => {
export default ({ tileType, onChange, onClick, selected = false }) => {
  const { name, color, coreLength } = tileType || {};
  // values must be primitives
  // labels is {key: label}
  // values is {key: value}

  //   if (!values) return null;

  return tileType ? (
    //   overflow visible so color picker works
    <Card
      style={{
        width: "100%",
        padding: "10px 0px",
        // overflow: "visible",
        border: selected ? "2px solid " + Colors.BLUE : undefined,
      }}
    >
      <div
        style={{
          padding: "0px 15px",
          cursor: "pointer",
        }}
        onClick={onClick}
      >
        <Typography variant={"h5"}>{"Tile " + name}</Typography>
      </div>
      {/* <Collapse in={selected} timeout="auto" unmountOnExit> */}
      <Collapse in={selected} timeout="auto">
        <div
          style={{
            width: "100%",
            display: "flex",
            justifyContent: "center",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <EditableField
            label={"Name"}
            value={name}
            onChange={(newValue) => {
              onChange({ ...tileType, name: newValue });
            }}
          />
          <EditableField
            label={"Core Length"}
            value={coreLength}
            onChange={(newValue) => {
              if (!isNaN(newValue) && newValue != null) {
                onChange({ ...tileType, coreLength: parseInt(newValue) });
              }
            }}
          />
          <EditableField
            label={"Color"}
            value={color}
            onChange={(newValue) => {
              onChange({ ...tileType, color: newValue });
            }}
          />
          {/* <ColorPicker
          name={"Color"}
          defaultValue={color}
          // value={this.state.color} - for controlled component
          onChange={(newValue) => {
            if (!newValue) return;
            console.log(newValue);
            onChange({ ...tileType, color: newValue });
          }}
        /> */}
        </div>
      </Collapse>
    </Card>
  ) : (
    ""
  );
};
