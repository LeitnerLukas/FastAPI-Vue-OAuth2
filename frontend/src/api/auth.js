import axios from "axios";
import qs from "qs";
import request from "./req";

export const apiLogin = (form) =>
  axios.post("/login", qs.stringify(form), {
    headers: { "content-type": "application/x-www-form-urlencoded" },
  });
export const apiLoginSuperuser = (form) => axios.post(`/superuser-login?api_key=${form}`);
export const apiRefresh = () => axios.post("/refresh");
export const apiLogout = () => axios.post("/logout");
