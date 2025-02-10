import axios from 'axios';

export const apiGetActivities = () => axios.get('/activities');
export const apiGetActivity = (activityId) =>
  axios.get(`/activities/${activityId}`);
export const createActivity = (activity) => axios.post('/activities', activity);
