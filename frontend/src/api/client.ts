import axios from 'axios'
import type { ProviderSearchRequest, ProviderSearchResponse } from '../types/provider'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

export async function searchProviders(
  params: ProviderSearchRequest
): Promise<ProviderSearchResponse> {
  const response = await apiClient.post<ProviderSearchResponse>('/api/search/providers', params)
  return response.data
}

export async function healthCheck(): Promise<{ status: string }> {
  const response = await apiClient.get<{ status: string }>('/api/health')
  return response.data
}

