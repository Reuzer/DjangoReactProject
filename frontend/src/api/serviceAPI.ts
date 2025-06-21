import axios, { AxiosResponse } from "axios";
import { Review, PetReport, Breed, PostPetReport, RegisterUser } from "./types";
import api from "./httpClient";


export default class ServiceApi {
    static async getReviews (): Promise<AxiosResponse<Review[]>> {
        const reviews = await axios.get('http://127.0.0.1:8000/api/reviews');
        return reviews;
    }

    static async getReports (): Promise<AxiosResponse<PetReport[]>> {
        const reports = await axios.get('http://127.0.0.1:8000/api/pet_reports');
        return reports;
    }

    static async getFilteredReports(params?: {
        pet_type?: number;
        report_type?: string;
        search?: string;
    }): Promise<AxiosResponse<PetReport[]>> {
        return await api.get('http://127.0.0.1:8000/api/pet-reports/filters/', {
            params: params
        });
    }

    static async getReport (id: number) : Promise<AxiosResponse<PetReport>> {
        const report = await axios.get(`http://127.0.0.1:8000/api/pet_reports/${id}`);
        return report;
    }

    static async postReport (data: PostPetReport) {
        const response = await api.post(`pet_reports/`, data);
        return response;
    }

    static async updateReports (id: number, data: PostPetReport) {
        const response = await api.put(`pet_reports/${id}/`, data);
        return response;
    }

    static async deleteReport(id: number) {
        await api.delete(`http://127.0.0.1:8000/api/pet_reports/${id}/`);
    }

    static async getBreeds(): Promise<AxiosResponse<Breed[]>> {
        const response = await axios.get(`http://127.0.0.1:8000/api/breeds/`);
        return response;
    }

    static async getAvgReviewRating(): Promise<AxiosResponse<{avg_rating: number}>> {
        const response = await axios.get(`http://127.0.0.1:8000/api/reviews/avg_rating`);
        return response;
    }

    static async getReportCount(): Promise<AxiosResponse<{reports_count: number}>> {
        const response = await axios.get(`http://127.0.0.1:8000/api/reports/total_count`);
        return response;
    }

    static async getUserReports(): Promise<AxiosResponse<PetReport[]>> {
        const response = await api.get(`http://127.0.0.1:8000/api/user/pet_reports/`);
        return response
    }
}