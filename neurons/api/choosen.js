import Handler from "../lib";

export default async (req, res) => {
  res.send(await Handler("voteReceived"), {choice: req.query.choice});
};
