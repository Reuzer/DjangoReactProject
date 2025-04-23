export interface User {
  first_name: string;
  last_name: string;
  photo: string;
  email: string;
  phone: string;
}

export interface PetType {
  id: number;
  user_id: User
  pet_type_id: string;
  color: string;
  size: string;
  resolved: boolean;
  special_marks: string;
  picture: string;
  public_date: string;
  change_date: string;
  report_type: 'lost' | 'found';
  location: string;
  description: string;
}

export interface Review {
    id: number;
    user_id: User;
    photo: string;
    text: string;
    rating: 1 | 2 | 3 | 4 | 5;
    date: string;
}