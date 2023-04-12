
import React from 'react'
import Navbar from "react-bootstrap/Navbar";
import "bootstrap/dist/css/bootstrap.min.css";

export function MyNavbar() {
  return (
    <>
      <Navbar bg="dark" variant="light" fixed="top" className="my-navbar">
        <Navbar.Brand className="title-stuff" bsPrefix="title-stuff">
          <img
            alt="uio-logo"
            src={require("../assets/BW_UiO_logo.png")}
            width="40"
          />{" "}
          IFI emner oversikt (uoffisiell)
        </Navbar.Brand>
      </Navbar>
    </>
  );
}