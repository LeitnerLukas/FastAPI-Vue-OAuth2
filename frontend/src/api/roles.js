import request from "./req";
import axios from "axios";

export const createRole = (data, token) => request("POST", `/roles/role?token=${token}`, data);
export const deleteUserRole = (username, role, token) =>
  request("DELETE", `/roles/role/user?username=${username}&role=${role}&token=${token}`);
export const updateUserRole = (username, role, token) =>
  request(
    "POST",
    `/roles/role/user?username=${username}&role=${role}&token=${token}`
  );
export const getRoles = (token) => request("GET", `/roles/roles?token=${token}`);
