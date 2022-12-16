const express = require("express");
const bodyParser = require("body-parser");

const app = express();
app.use(bodyParser.json());

const routes = require("./api/routes");
routes(app);

app.listen(3000, () => {
  console.log("Server listening on port 3000");
});
