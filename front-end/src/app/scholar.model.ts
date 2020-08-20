export interface Scholar {
  doctoral_advisor: string[];
  doctoral_student: string[];
  field: string;
  id: string;
  image_link: string;
  wiki_link: string;
  name: string;
}

export interface ScholarJSON {
  scholars: Scholar[];
}
