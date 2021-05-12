import Handler from "../lib";

export default async (req, res) => {
  res.send(await Handler("playTheSounds", {sound: req.query.sound}));
};
