const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const bodyParser = require("body-parser");
const cookieParser = require("cookie-parser");
const path = require("path");

const app = express();
const db = new sqlite3.Database("./db.sqlite");

// 1) middlewares
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());

app.use(express.static("public"));

// 2) routes
app.get("/", (req, res) => {
  return res.sendFile(path.join(__dirname, "views/index.html"));
});

app.post("/login", (req, res) => {
  const { username, password } = req.body;

  // username SAFE (fixed / validated)
  if (username !== "@dmindex021") {
    return res.send("ACCESS DENIED");
  }

  // password VULNERABLE (intentional SQLi)
  const query = `SELECT * FROM users WHERE username='@dmindex021' AND password='${password}'`;

  db.get(query, (err, row) => {
    if (err) {
      return res.send("ACCESS DENIED");
    }

    if (row) {
      res.cookie("auth", "1", { httpOnly: true });
      return res.redirect("/home");
    }

    return res.send("ACCESS DENIED");
  });
});

// 4) protected route
app.get("/home", (req, res) => {
  if (req.cookies && req.cookies.auth === "1") {
    return res.sendFile(path.join(__dirname, "views/home.html"));
  }
  return res.send("ACCESS DENIED");
});

// 5) listening
const PORT = process.env.PORT || 1596;

app.listen(PORT, () => console.log("Running on " + PORT));
