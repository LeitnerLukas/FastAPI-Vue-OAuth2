import request from "./req";
import axios from "axios";

export const getClasses = async () => {
  return JSON.stringify([
    {
      classId: "4ahit",
      girls: 10,
      boys: 20,
    },
    {
      classId: "5ahit",
      girls: 10,
      boys: 20,
    },
  ]);
};
export const createClass = (data) => axios.post("/classes", data);
export const deleteClass = (id) => axios.delete(`/class/${id}`);
