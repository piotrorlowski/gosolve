const API_HOST = import.meta.env.VITE_API_HOST || 'localhost'
const API_PORT = import.meta.env.VITE_API_PORT || '8000'

export const API_BASE_URL = `http://${API_HOST}:${API_PORT}`

export const ENDPOINTS = {
    INDEX: (inputValue: string) => `${API_BASE_URL}/index/${inputValue}/`,
}
