export interface Provider {
  npi: string
  enumeration_type: string
  first_name?: string
  last_name?: string
  organization_name?: string
  city?: string
  state?: string
  postal_code?: string
  taxonomy?: string
  website?: string
  confidence: number
}

export interface ProviderSearchRequest {
  first_name?: string
  last_name?: string
  organization_name?: string
  city?: string
  state?: string
  postal_code?: string
  taxonomy?: string
  limit?: number
}

export interface ProviderSearchResponse {
  providers: Provider[]
}

