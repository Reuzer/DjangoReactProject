export interface ReadUser {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  middle_name?: string;
  photo?: string;
  phone?: string;
  role: 'admin' | 'user';
}

export interface RegisterUser {
  username: string,
  email: string,
  password: string;
  first_name: string,
  last_name: string,
  middle_name?: string,
  photo?: string,
  phone: string,
}

export interface LoginUser {
  username: string;
  password: string;
}

export interface PetType {
  id: number;
  type_name: string;
}

export interface Breed {
  id: number;
  pet_type_id: PetType;
  breed: string;
}

export interface PetReport {
  id: number;
  user_id: ReadUser;
  breed_id: Breed;
  title: string;
  color: string;
  size: string;
  resolved: boolean;
  special_marks: string;
  picture: string | null;
  thumbnail: string;
  public_date: string;
  change_date: string;
  report_type: 'lost' | 'found';
  location: string;
  description: string;
}

export interface Review {
  id: number;
  user_id: ReadUser;
  photo: string;
  text: string;
  rating: 1 | 2 | 3 | 4 | 5;
  date: string;
}

export interface PostPetReport {
  user_id: number,
  breed_id: number,
  title: string,
  resolved: boolean,
  special_marks: string,
  picture: File | null,
  report_type: 'lost' | 'found' | '',
  location: string,
  description: string;
}