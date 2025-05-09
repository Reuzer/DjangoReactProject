import axios, { AxiosResponse } from "axios";
import { Review, PetReport, Breed, PostPetReport } from "./types";


export default class ServiceApi {
    static async getReviews (): Promise<AxiosResponse<Review[]>> {
        const reviews = await axios.get('http://127.0.0.1:8000/api/reviews');
        return reviews;
    }

    static async getReports (): Promise<AxiosResponse<PetReport[]>> {
        const reports = await axios.get('http://127.0.0.1:8000/api/pet_reports');
        return reports;
    }

    static async getReport (id: number) : Promise<AxiosResponse<PetReport>> {
        const report = await axios.get(`http://127.0.0.1:8000/api/pet_reports/${id}`);
        return report;
    }

    static async postReport (data: PostPetReport) {
        const response = await axios.post(`http://127.0.0.1:8000/api/pet_reports/`, data);
        return response;
    }

    static async updateReports (id: number, data: PostPetReport) {
        const response = await axios.put(`http://127.0.0.1:8000/api/pet_reports/${id}/`, data);
        return response;
    }

    static async deleteReport(id: number) {
        await axios.delete(`http://127.0.0.1:8000/api/pet_reports/${id}/`);
    }

    static async getBreeds(): Promise<AxiosResponse<Breed[]>> {
        const response = await axios.get(`http://127.0.0.1:8000/api/breeds/`);
        return response;
    }

}