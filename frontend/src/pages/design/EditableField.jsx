import React, { useState } from "react";
import { TextField, InputUnstyled } from "@mui/material";

export default ({ label, value, onChange, isEditable = true }) => {
  const [fieldValue, setFieldValue] = useState(value);
  return (
    <div style={{ padding: 5 }}>
      <TextField
        style={{ backgroundColor: "white" }}
        id={label}
        label={label}
        // variant="outlined"
        // disabled={!isEditable}
        onChange={(event) => {
          // only accept number values
          // if (event.target.value.length == 0 || isNaN(event.target.value)) {
          //   setFieldValue("");
          //   onChange(undefined);
          // } else {
          setFieldValue(event.target.value);
          onChange(event.target.value);
          // }
        }}
        required
        // defaultValue={value}
        value={fieldValue}
      />
    </div>
  );
};
