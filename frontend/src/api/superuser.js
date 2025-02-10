import axios from "axios";

export const updateUserRole = (user_id, role_id) => axios.post(`/user/${id}`, role);
export const deleteUser = (id) => axios.post(`/user/${id}`);