import { createTheme } from "@mui/material/styles";

const theme = createTheme({});

export default {
  //   BLUE: "rgb(0,120,196)",
  BLUE: theme.palette.primary.light,
  PINK: "rgb(246,0,223)",
  WHITE: "#FFF",
  GRAY: "#777",
  LIGHT_GRAY: "#999",
  BACKGROUND_COLOR: "rgb(242,242,242)",
  TILE_TYPES: {
    RED: theme.palette.error.light,
    BLUE: theme.palette.primary.light,
    PURPLE: theme.palette.secondary.light,
    ORANGE: theme.palette.warning.light,
    GREEN: theme.palette.success.light,
  },
};
