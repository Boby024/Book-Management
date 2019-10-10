export interface Buch {
  id: number;
  titel: string;
  autor: string;
  verlag: string;
  // erscheinungsjahr: Date;
  erscheinungsjahr: string;
  status: string;
  ausgeliehen_am: string;
}
