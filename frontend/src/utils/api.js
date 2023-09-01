import { API_ENDPOINTS } from "./config";

export async function trainModel(formData) {
    try {
        const response = await fetch(API_ENDPOINTS.TRAIN_MODEL, {
            method: 'POST',
            body: formData
        })
        return await response.json();
    }catch (e) {
        console.error("Error when sending files:", e);
        throw e;
    }
}