import axios from "axios";

export const updateUserRole = (role, id) => axios.post(`/user/${id}`, role);
export const deleteUser = (id) => axios.post(`/user/${id}`);