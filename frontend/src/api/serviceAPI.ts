import axios, { AxiosResponse } from "axios";
import { Review } from "./types";


export default class ServiceApi {
    static async getReviews (): Promise<AxiosResponse<Review[]>> {
        const reviews = await axios.get('http://127.0.0.1:8000/api/reviews')
        return reviews;
    }
}