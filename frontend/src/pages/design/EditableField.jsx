import React, { useState } from "react";
import { TextField } from "@mui/material";

export default ({ label, value, onChange, isEditable = true }) => {
  const [fieldValue, setFieldValue] = useState(value);
  return (
    <div style={{ padding: 5 }}>
      <TextField
        style={{ backgroundColor: "white" }}
        id={label}
        label={label}
        onChange={(event) => {
          setFieldValue(event.target.value);
          onChange(event.target.value);
        }}
        required
        value={fieldValue}
      />
    </div>
  );
};
