import request from "./req";
import axios from "axios";

export const createRole = (data) => request("POST", "/roles", data);
export const deleteUserRole = (user_id, role_id) =>
  request("DELETE", `/roles/${user_id}/${role_id}`);
export const getRoles = () => request('GET', '/roles');
