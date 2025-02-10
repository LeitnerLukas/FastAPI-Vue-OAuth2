import request from "./req";
import axios from "axios";

export const createRole = (data) => request("POST", "/roles", data);
export const deleteUserRole = (user_id, role_id) =>
  request("DELETE", `/roles/${user_id}/${role_id}`);
export const getRoles = async () => {
  return JSON.stringify([
    {
      id: 1,
      name: "Teacher",
      approvement_permission: false,
      super_approvement_permission: false,
      request_permission: true,
      change_permission: false,
    },
    {
      id: 2,
      name: "Head of Department",
      approvement_permission: true,
      super_approvement_permission: false,
      request_permission: true,
      change_permission: true,
    },
    {
      id: 3,
      name: "Principal",
      approvement_permission: true,
      super_approvement_permission: true,
      request_permission: true,
      change_permission: true,
    },
  ]);
};
