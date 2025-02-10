import axios from 'axios';

export const apiGetActivities = () => axios.get('/api/activities');
export const apiGetActivity = (activityId) =>
  axios.get(`/api/activities/${activityId}`);
export const createActivity = (activity) =>
  axios.post('/api/apiactivities', activity);
export const updateActivity = (activity) =>
  axios.put(`/api/activities/${activity.id}`, activity);
