import request from "./req";
import axios from "axios";

export const getUsers = async () => {
  return JSON.stringify([
    {
      id: 1,
      email: "fs@gmail.com",
      name: "Fahad",
      role: {
        name: "Teacher",
      },
    },
    {
      id: 2,
      email: "jp@gmail.com",
      name: "Jpid",
      role: {
        name: "Principal",
      },
    },
  ]);
};
export const getRoles = async () => {
  return JSON.stringify([
    { id: 1, name: "Teacher" },
    { id: 2, name: "Head of Department" },
    { id: 3, name: "Principal" },
  ]);
};
export const apiRegister = (data) => axios.post("/users", data);
export const apiGetUserList = () => axios.get("/users");
