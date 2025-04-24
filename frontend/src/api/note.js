import request from './req';

export const getnote = (noteId) => request('GET', `/activities/${noteId}`);
export const createNote = (note) => request('POST', '/notes', note);
export const updateNote = (note) =>
  request('PUT', `/notes/${note.id}`, activity);
