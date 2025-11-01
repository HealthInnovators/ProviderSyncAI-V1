import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { searchProviders } from '../../api/client'
import type { ProviderSearchRequest } from '../../types/provider'
import SearchBar from '../../components/SearchBar'
import ProviderList from '../../components/ProviderList'

export default function SearchPage() {
  const [searchParams, setSearchParams] = useState<ProviderSearchRequest | null>(null)

  const { data, isLoading, error } = useQuery({
    queryKey: ['providers', searchParams],
    queryFn: () => searchProviders(searchParams!),
    enabled: searchParams !== null,
  })

  const handleSearch = (params: ProviderSearchRequest) => {
    setSearchParams(params)
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">ProviderSyncAI</h1>
          <p className="text-gray-600 mt-2">
            Search for healthcare providers using NPPES registry and web enrichment
          </p>
        </div>

        <SearchBar onSearch={handleSearch} isLoading={isLoading} />

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <p className="text-red-800">
              Error: {error instanceof Error ? error.message : 'Failed to search providers'}
            </p>
          </div>
        )}

        {data && <ProviderList providers={data.providers} isLoading={isLoading} />}
      </div>
    </div>
  )
}

