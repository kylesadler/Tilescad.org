import React, { createRef, useState } from "react";
import Sketch from "react-p5";
import { Form, Button } from "react-bootstrap";
import { uploadDesign } from "../../APIService";

class Tile {
  constructor(x, y, s) {
    this.x = x;
    this.y = y;
    this.s = s;
    this.isClicked = false;
  }

  draw(p5) {
    p5.stroke(10);
    p5.fill(this.isClicked ? 10 : 230);
    p5.rectMode(p5.CENTER);
    p5.square(this.x, this.y, this.s);
  }

  clicked() {
    this.isClicked = !this.isClicked;
  }

  setX(newX) {
    this.x = newX;
  }

  setY(newY) {
    this.y = newY;
  }

  setS(newS) {
    this.s = newS;
  }
}

export default (props) => {
  const canvasSize = 800;
  // let tileDim = 16;

  const [tileDim, setTileDim] = useState(16);

  let tileSize;
  const hiddenForm = createRef();
  const filenameInput = createRef();

  let tiles = []; // tiles[numTiles][numTiles] grid

  const setup = (p5, canvasParentRef) => {
    // use parent to render the canvas in this ref
    // (without that p5 will render the canvas outside of your component)
    p5.createCanvas(canvasSize, canvasSize).parent(canvasParentRef);

    tileSize = canvasSize / tileDim;
    for (let y = tileSize / 2; y < p5.height; y += tileSize) {
      let tileRow = [];
      for (let x = tileSize / 2; x < p5.width; x += tileSize) {
        tileRow.push(new Tile(x, y, tileSize));
      }
      tiles.push(tileRow);
    }
    // console.log(tiles);
  };

  const draw = (p5) => {
    p5.background(255);

    for (let i = 0; i < tiles.length; i++) {
      for (let j = 0; j < tiles[0].length; j++) {
        tiles[i][j].draw(p5);
      }
    }

    // NOTE: Do not use setState in the draw function or in functions that are executed
    // in the draw function...
    // please use normal variables or class properties for these purposes
  };

  const mousePressed = (event) => {
    console.log("mousePressed", event.mouseX, event.mouseY);
    const x = Math.floor(event.mouseX / tileSize);
    const y = Math.floor(event.mouseY / tileSize);
    console.log("x, y", x, y);

    if (x >= 0 && x < tileDim && y >= 0 && y < tileDim) {
      tiles[y][x].clicked();
    }
  };

  return (
    <div class="row">
      <div class="col">
        <h1>SETTINGS</h1>
        <Form>
          <Form.Group className="canvas-type" controlId="formBasic1">
            <Form.Label>Geometric structure</Form.Label>
            <Form.Select
              aria-label="Default select example"
              onChange={(event) => {}}
            >
              <option value="0">Flat Canvas</option>
              <option value="1">Tube</option>
            </Form.Select>
          </Form.Group>
        </Form>
        <Form>
          <Form.Group className="canvas-size" controlId="formBasic2">
            <Form.Label>Canvas size</Form.Label>
            <Form.Select
              aria-label="Default select example"
              onChange={(event) => {
                // tileDim = event.target.value;
                setTileDim(event.target.value);
              }}
            >
              <option value="16">16x16</option>
              <option value="32">32x32</option>
              <option value="48">48x48</option>
            </Form.Select>
          </Form.Group>
          <Form.Group>
            <Form.Label>Lengths of the DNA tiles binding domains</Form.Label>
            <Form.Range min="5" max="25" />
          </Form.Group>
          <Form.Group className="tile-prefix" controlId="formBasic">
            <Form.Label>Tile label prefix</Form.Label>
            <Form.Control
              type="password"
              id="inputPassword5"
              aria-describedby="passwordHelpBlock"
            />
            <Form.Text id="tileLabelPrefix">
              DNA tile label prefix will be appended to the output tiles in the
              scadnano file.
            </Form.Text>
          </Form.Group>
          <Button
            variant="primary"
            type="submit"
            onClick={() => {
              uploadDesign(tiles.map((t) => t.map((x) => x.isClicked))).then(
                (filename) => {
                  console.log(filename);
                  filenameInput.current.setAttribute("value", filename);
                  hiddenForm.current.submit();
                }
              );
            }}
          >
            Submit
          </Button>
        </Form>
      </div>
      <div class="col">
        <Sketch setup={setup} draw={draw} mousePressed={mousePressed} />
      </div>
      {/* <div class="col"> 
        <button
          onClick={() => {
            uploadDesign(tiles.map((t) => t.map((x) => x.isClicked))).then(
              (filename) => {
                console.log(filename);
                filenameInput.current.setAttribute("value", filename);
                hiddenForm.current.submit();
              }
            );
          }}
          type="button"
          class="btn btn-primary"
        >
          Upload data
        </button> */}
      {/* hidden form so user can download scadnano file */}
      {/*<form ref={hiddenForm} action="/api/download-file" method="POST">
          <input
            ref={filenameInput}
            type="hidden"
            name="filename"
            value="null"
          />
        </form>
      </div>*/}
    </div>
  );
};
